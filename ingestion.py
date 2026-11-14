# Knowledge Base Ingestion: read a file -> extract text -> clean it -> split it into chunks.

import csv
import io
import re

import docx                    # python-docx, reads .docx files
from pypdf import PdfReader    # reads .pdf files

from config import CHUNK_SIZE, CHUNK_OVERLAP

# Text extraction

def extract_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    pieces = []
    for page_number, page in enumerate(reader.pages, start=1):
        pieces.append({"text": page.extract_text() or "", "page": page_number})
    return pieces


def extract_docx(file_bytes):
    document = docx.Document(io.BytesIO(file_bytes))
    lines = []
    for p in document.paragraphs:
        if not p.text.strip():
            continue
        if p.style.name.startswith("Heading"):
            lines.append(p.text.upper())     # write headings in CAPITALS so they are found later
        else:
            lines.append(p.text)
    # Tables: turn each row into "Header: value | Header: value"
    for table in document.tables:
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        header = rows[0]
        lines.append("TABLE")
        for row in rows[1:]:
            lines.append(" | ".join(f"{h}: {v}" for h, v in zip(header, row)))
    return [{"text": "\n".join(lines), "page": None}]


def extract_txt(file_bytes):
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1")
    return [{"text": text, "page": None}]


def extract_csv(file_bytes, filename):
    text = file_bytes.decode("utf-8", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    header = rows[0]
    table_name = filename.rsplit(".", 1)[0].replace("_", " ").title()
    pieces = []
    for row in rows[1:]:
        if any(cell.strip() for cell in row):
            row_text = " | ".join(f"{h}: {v}" for h, v in zip(header, row) if v.strip())
            pieces.append({"text": f"{table_name}: {row_text}", "page": None})
    return pieces


def extract_text(filename, file_bytes):
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension == "pdf":
        return extract_pdf(file_bytes)
    if extension == "docx":
        return extract_docx(file_bytes)
    if extension == "txt":
        return extract_txt(file_bytes)
    if extension == "csv":
        return extract_csv(file_bytes, filename)
    raise ValueError(f"Unsupported file type: .{extension}")


# Cleaning
def clean_text(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)              # join words broken by "-" at line end
    text = re.sub(r"^\s*Page \d+\s*$", "", text, flags=re.M)   # remove "Page 3" footers
    text = re.sub(r"[ \t]+", " ", text)                        # many spaces -> one space
    text = re.sub(r"\n\s*\n+", "\n", text)                     # remove empty lines
    return text.strip()


#3. Chunking
def is_heading(line):
    """A heading is a short line written in CAPITAL letters, e.g. "3. SICK LEAVE"."""
    letters = [c for c in line if c.isalpha()]
    return len(line) < 80 and len(letters) >= 4 and all(c.isupper() for c in letters)


def split_into_sections(text):
    """Start a new section at every heading, so one chunk never mixes two topics.
    A very short section (e.g. only a title) is joined with the next one."""
    sections = []
    for line in text.split("\n"):
        if not sections or (is_heading(line) and len(sections[-1]) >= 100):
            sections.append(line)
        else:
            sections[-1] += "\n" + line
    return sections


def split_into_sentences(text):
    # Split after . ! ? or at a line break.
    parts = re.split(r"(?<=[.!?])\s+|\n", text)
    return [p.strip() for p in parts if p.strip()]


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Group whole sentences into chunks of at most `chunk_size` characters.
    The last sentences of a chunk (up to `overlap` characters) are repeated at the
    start of the next chunk, so information on a boundary is not lost."""
    chunks = []
    current = []
    for sentence in split_into_sentences(text):
        if current and len(" ".join(current + [sentence])) > chunk_size:
            chunks.append(" ".join(current))
            # keep the last sentences as overlap
            kept = []
            for s in reversed(current):
                if len(" ".join([s] + kept)) > overlap:
                    break
                kept.insert(0, s)
            current = kept
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


# All steps together
def file_to_chunks(filename, file_bytes):
    """Returns a list of chunks: {"text": ..., "page": ...}"""
    chunks = []
    for piece in extract_text(filename, file_bytes):
        text = clean_text(piece["text"])
        for section in split_into_sections(text):
            for chunk_text in split_into_chunks(section):
                chunks.append({"text": chunk_text, "page": piece["page"]})
    return chunks
