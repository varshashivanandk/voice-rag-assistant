import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "sample_docs"

# DOMAIN 1 - HR POLICY

HR_HANDBOOK_TITLE = "Nimbus Technologies - Employee Handbook 2026"
HR_HANDBOOK = [
    ("1. About This Handbook", [
        "This handbook applies to all full-time employees of Nimbus Technologies Pvt. Ltd. working "
        "from the Bengaluru, Pune and Hyderabad offices or remotely within India. Contractors and "
        "interns are governed by their individual agreements unless a section states otherwise.",
        "Policies are reviewed every year by the People Operations team. The latest version is always "
        "available on PeopleHub, the internal HR portal, and supersedes all earlier versions.",
    ]),
    ("2. Working Hours and Attendance", [
        "The standard working week is 40 hours, Monday to Friday. Nimbus follows a flexible schedule "
        "with core collaboration hours from 10:30 AM to 4:30 PM IST, during which employees are "
        "expected to be available for meetings.",
        "Attendance is recorded automatically when employees sign in to PeopleHub. Employees who "
        "forget to sign in must raise an attendance regularisation request within 5 working days.",
        "Employees working in customer-facing support teams follow rotational shifts published two "
        "weeks in advance and receive a shift allowance of Rs 4,000 per month for night shifts.",
    ]),
    ("3. Probation and Confirmation", [
        "New employees serve a probation period of 6 months. The manager completes a confirmation "
        "review in the final month of probation. Probation may be extended once by up to 3 months "
        "if performance expectations are not met.",
        "During probation either party may end employment with 15 days of notice. After confirmation "
        "the notice period is 60 days for individual contributors and 90 days for people managers "
        "(grade M1 and above).",
    ]),
    ("4. Compensation and Payroll", [
        "Salaries are credited on the last working day of every month. Payslips are published on "
        "PeopleHub by the 3rd of the following month.",
        "Business expense reimbursement claims must be submitted on PeopleHub with receipts within "
        "30 days of the expense. Claims submitted later require approval from the Finance Controller.",
        "Employees on hybrid or remote arrangements receive an internet reimbursement of up to "
        "Rs 1,500 per month against a valid bill.",
        "Salary revisions take effect from 1 July each year and are based on the annual performance "
        "rating and market benchmarks.",
    ]),
    ("5. Performance Management", [
        "Performance reviews take place twice a year, in April (annual review) and October "
        "(mid-year check-in). Employees are rated on a five-point scale where 1 is 'Does not meet "
        "expectations' and 5 is 'Role model'.",
        "Employees rated 1 in the annual review are placed on a Performance Improvement Plan (PIP) "
        "lasting 60 days with fortnightly check-ins between the employee, manager and HR business partner.",
    ]),
    ("6. Code of Conduct and Gifts", [
        "Employees must act with integrity, avoid conflicts of interest and protect confidential "
        "information belonging to Nimbus and its clients.",
        "Gifts from vendors or clients with a value up to Rs 2,000 may be accepted. Gifts above this "
        "value must be declared to the Compliance team within 7 days and may need to be returned. "
        "Cash or cash equivalents may never be accepted.",
    ]),
    ("7. Grievance Redressal", [
        "Employees can raise a grievance through the Grievance section on PeopleHub or by emailing "
        "grievance@nimbustech.example. Every grievance is acknowledged within 2 working days and the "
        "committee aims to resolve it within 15 working days.",
        "Complaints of sexual harassment are handled by the Internal Committee constituted under the "
        "POSH Act, 2013, and can be reported confidentially to ic@nimbustech.example.",
    ]),
    ("8. Business Travel", [
        "All domestic travel must be booked through the TravelDesk at least 7 days before the "
        "travel date. Economy class is the default for flights under 6 hours.",
        "The daily allowance (per diem) for domestic travel is Rs 2,500 per day in metro cities and "
        "Rs 1,800 per day in non-metro cities. For international travel the per diem is USD 75 per day.",
        "Hotel stays are booked by TravelDesk within the approved city limits. Employees must submit "
        "the travel expense report within 15 days of returning.",
    ]),
    ("9. Learning and Development", [
        "Every confirmed employee has an annual learning budget of Rs 40,000 that can be used for "
        "courses, conferences and books approved by the manager.",
        "Certification exam fees are reimbursed after the employee passes the exam. If the employee "
        "leaves within 12 months of a reimbursed certification, the amount is recovered from the "
        "final settlement.",
    ]),
    ("10. Separation and Exit", [
        "Resignations are submitted on PeopleHub. The manager and HR schedule an exit interview "
        "during the notice period.",
        "All company assets, including the laptop, ID card and access tokens, must be returned on "
        "or before the last working day. The full and final settlement is processed within 45 days "
        "of the last working day.",
    ]),
]

HR_LEAVE_TITLE = "Nimbus Technologies - Leave Policy"
HR_LEAVE = [
    ("Purpose", [
        "This policy explains the types of leave available to full-time employees of Nimbus "
        "Technologies, how leave accrues, and how to apply for it. Leave year runs from 1 January "
        "to 31 December.",
    ]),
    ("Earned Leave", [
        "Employees receive 18 days of earned leave (also called privilege leave) per year, accruing "
        "at 1.5 days per month. Unused earned leave can be carried forward up to a maximum balance "
        "of 30 days. At separation, up to 15 days of earned leave balance is encashed at basic salary.",
    ]),
    ("Casual Leave", [
        "Employees receive 8 days of casual leave per year for personal matters. Casual leave cannot "
        "be carried forward to the next year and cannot be taken for more than 3 consecutive days.",
    ]),
    ("Sick Leave", [
        "Employees receive 10 days of sick leave per year. A medical certificate from a registered "
        "medical practitioner is required for sick leave longer than 2 consecutive days. Up to 20 "
        "days of unused sick leave can be carried forward.",
    ]),
    ("Parental Leave", [
        "Birthing mothers are entitled to 26 weeks of paid maternity leave for the first two children "
        "and 12 weeks thereafter. Fathers and non-birthing partners receive 10 working days of "
        "paternity leave, to be taken within 6 months of the child's birth. Employees adopting a child "
        "below 3 months of age receive 12 weeks of adoption leave.",
    ]),
    ("Other Leave", [
        "Bereavement leave of 5 working days is granted on the death of an immediate family member. "
        "Employees who work on a declared company holiday receive a compensatory off that must be "
        "used within 30 days. Leave without pay can be granted for up to 60 days with approval from "
        "the Head of People Operations.",
    ]),
    ("How to Apply for Leave", [
        "1. Log in to PeopleHub and open the Leave section.",
        "2. Select the leave type and dates; the system shows your available balance.",
        "3. Earned leave of more than 3 days must be applied for at least 7 days in advance.",
        "4. Your reporting manager approves or rejects the request within 3 working days.",
        "5. For unplanned absence such as sudden illness, inform your manager the same day and apply "
        "on PeopleHub within 24 hours of returning to work.",
    ]),
]
HR_LEAVE_TABLE = [
    ["Leave type", "Annual quota", "Carry forward", "Encashable"],
    ["Earned leave", "18 days", "Up to 30 days", "Yes, up to 15 days at exit"],
    ["Casual leave", "8 days", "No", "No"],
    ["Sick leave", "10 days", "Up to 20 days", "No"],
    ["Bereavement leave", "5 days per event", "Not applicable", "No"],
]

HR_REMOTE_TXT = """NIMBUS TECHNOLOGIES - REMOTE WORK AND IT SECURITY FAQ

HYBRID WORK MODEL
Hybrid employees work from the office three days a week, on Tuesday, Wednesday and Thursday. Monday and Friday are flexible remote days. Teams may agree on additional office days for planning events.

REQUESTING FULLY REMOTE WORK
Fully remote work is an exception and needs approval from the department Vice President.
To request it:
1. Submit the Remote Work Request form on PeopleHub with the business justification.
2. Your manager reviews the request and adds a recommendation.
3. The HR business partner checks eligibility, including that you have completed probation.
4. The department Vice President gives the final approval.
An approved remote arrangement is valid for 6 months and must be renewed after that.

WORKING FROM ABROAD
Employees may work from outside India for up to 30 days in a calendar year, with manager approval and a tax check by the Payroll team at least 14 days before travel.

HOME OFFICE SETUP
Employees approved for remote work receive a one-time home office allowance of Rs 15,000 for a chair, desk or monitor. Receipts must be submitted within 60 days.

VPN AND MULTI-FACTOR AUTHENTICATION
All access to internal systems from outside the office must go through the GlobalProtect VPN. Multi-factor authentication uses the Microsoft Authenticator app. If you change your phone, raise a ticket with the IT Helpdesk to re-register MFA before resetting the old device.

PASSWORD POLICY
Passwords must be at least 14 characters long and include upper case, lower case, a number and a symbol. Passwords expire every 90 days and the last 5 passwords cannot be reused. Never share your password, including with IT staff.

LOST OR STOLEN LAPTOP
Report a lost or stolen laptop to the IT Security team within 4 hours by emailing security@nimbustech.example and calling the IT Helpdesk on extension 4040. IT will remotely lock and wipe the device. A police report (FIR) copy is required for stolen devices.

PERSONAL DEVICES
Personal phones and tablets may be used for email and Teams only after enrolling them in Microsoft Intune. Company source code and customer data must never be stored on personal devices.

IT HELPDESK
The IT Helpdesk is available 24x7 on extension 4040 or helpdesk@nimbustech.example. Laptop replacement requests are fulfilled within 3 working days.
"""

HR_HOLIDAYS_CSV = [
    ["Date", "Day", "Holiday", "Type", "Applicable locations"],
    ["2026-01-01", "Thursday", "New Year's Day", "Mandatory", "All offices"],
    ["2026-01-14", "Wednesday", "Makar Sankranti / Pongal", "Optional", "Bengaluru, Hyderabad"],
    ["2026-01-26", "Monday", "Republic Day", "Mandatory", "All offices"],
    ["2026-03-04", "Wednesday", "Holi", "Mandatory", "Pune, Hyderabad"],
    ["2026-03-19", "Thursday", "Ugadi / Gudi Padwa", "Mandatory", "All offices"],
    ["2026-03-21", "Saturday", "Eid ul-Fitr", "Optional", "All offices"],
    ["2026-04-03", "Friday", "Good Friday", "Optional", "All offices"],
    ["2026-05-01", "Friday", "Maharashtra Day / May Day", "Mandatory", "Pune, Bengaluru"],
    ["2026-08-15", "Saturday", "Independence Day", "Mandatory", "All offices"],
    ["2026-09-14", "Monday", "Ganesh Chaturthi", "Mandatory", "All offices"],
    ["2026-10-02", "Friday", "Gandhi Jayanti", "Mandatory", "All offices"],
    ["2026-10-20", "Tuesday", "Dussehra", "Mandatory", "All offices"],
    ["2026-11-09", "Monday", "Diwali (Deepavali)", "Mandatory", "All offices"],
    ["2026-11-10", "Tuesday", "Diwali Balipadyami", "Optional", "Bengaluru"],
    ["2026-12-25", "Friday", "Christmas", "Mandatory", "All offices"],
]

# =====================================================================================
# DOMAIN 2 - SMART HOME PRODUCT SUPPORT
# =====================================================================================
SH_MANUAL_TITLE = "AeroHome Smart Thermostat T2 - User Manual"
SH_MANUAL = [
    ("1. In the Box", [
        "The AeroHome Smart Thermostat T2 package contains the display unit, a base plate with "
        "built-in spirit level, a trim plate, two wall screws and anchors, wire labels and this manual.",
    ]),
    ("2. Compatibility", [
        "The T2 works with most 24V heating and cooling systems, including gas, oil and electric "
        "furnaces, central air conditioners and heat pumps with auxiliary heat.",
        "The T2 is not compatible with line-voltage (120V or 240V) systems such as electric "
        "baseboard heaters. Check the wires on your current thermostat: thick wires connected with "
        "wire nuts usually indicate a line-voltage system.",
        "A common wire (C-wire) is recommended for continuous power. If your system has no C-wire, "
        "install the AeroHome Power Extender Kit (PEK), which is included with the T2 Pro and sold "
        "separately for the T2.",
    ]),
    ("3. Installation", [
        "1. Switch off power to your heating and cooling system at the circuit breaker.",
        "2. Remove the old thermostat cover and take a photo of the existing wiring.",
        "3. Attach the supplied labels to each wire (R, C, W, Y, G) and disconnect them.",
        "4. Mount the T2 base plate on the wall using the built-in level and the supplied screws.",
        "5. Insert each labelled wire into the matching terminal until the button clicks.",
        "6. Attach the display to the base plate and restore power at the breaker.",
        "Installation typically takes about 30 minutes. If you are unsure about your wiring, book a "
        "professional installation through the AeroHome app.",
    ]),
    ("4. Connecting to Wi-Fi", [
        "The T2 connects only to 2.4 GHz Wi-Fi networks; 5 GHz networks are not supported.",
        "To pair the thermostat, open the AeroHome app, tap Add Device, and choose Thermostat T2. "
        "Press and hold the dial for 5 seconds until the LED ring blinks blue, which means the "
        "thermostat is in pairing mode. Then select your home network and enter the password in the app.",
    ]),
    ("5. Schedules and Eco Mode", [
        "You can create up to 8 temperature changes per day in the schedule screen of the app.",
        "Eco mode saves energy when nobody is home. The default Eco temperatures are 16 degrees "
        "Celsius for heating and 28 degrees Celsius for cooling and can be changed in Settings.",
        "Away detection uses phone geofencing: when every household member's phone is more than "
        "500 metres from home, the T2 switches to Eco mode automatically.",
        "A monthly energy report showing heating and cooling hours is sent in the app on the 1st "
        "of every month.",
    ]),
    ("6. Factory Reset", [
        "A factory reset erases schedules, Wi-Fi details and account pairing. To reset from the "
        "device, open Settings > Reset > Factory reset on the thermostat menu. Alternatively, press and "
        "hold the dial for 15 seconds until the LED ring turns red, then release it. The thermostat "
        "restarts in about one minute.",
    ]),
    ("7. Firmware Updates", [
        "Firmware updates are installed automatically between 2 AM and 4 AM local time when the "
        "thermostat is connected to Wi-Fi. Heating and cooling continue to work during an update.",
    ]),
    ("8. Technical Specifications", [
        "Display: 2.4 inch colour LCD. Temperature control range: 5 to 35 degrees Celsius. Accuracy: "
        "plus or minus 0.5 degrees Celsius. Wireless: Wi-Fi 802.11 b/g/n (2.4 GHz) and Bluetooth "
        "Low Energy 5.0. Smart-home standards: Matter certified; works with Google Home and Amazon "
        "Alexa. Power: 24V AC via C-wire or Power Extender Kit. Built-in backup battery keeps the "
        "clock and settings for 2 hours during a power cut.",
    ]),
    ("9. Safety Information", [
        "Do not install the thermostat near heat sources such as lamps, direct sunlight or kitchen "
        "appliances, as this affects temperature readings. The thermostat is intended for indoor use only.",
    ]),
]

SH_TROUBLE_TITLE = "AeroHome Troubleshooting Guide"
SH_TROUBLE = [
    ("Before You Start", [
        "Most issues can be resolved by restarting the device and confirming that your home Wi-Fi "
        "is working. Keep your device serial number ready before contacting support; it starts with "
        "AH- and is printed on the back of the display or the base of the purifier.",
    ]),
    ("Thermostat Shows Offline in the App", [
        "1. Check that your router is broadcasting a 2.4 GHz network.",
        "2. Move the router closer or add a Wi-Fi extender if signal strength in the app is below two bars.",
        "3. Restart the thermostat by removing the display from the base plate for 10 seconds.",
        "4. If the router password changed, repeat Wi-Fi pairing from the app.",
    ]),
    ("Heating or Cooling Does Not Start", [
        "Make sure the system mode is set to Heat or Cool, not Off. The T2 has a built-in compressor "
        "protection delay of 5 minutes between cooling cycles, so cooling may not start immediately.",
        "If error code E5 appears, the HVAC system did not respond within 15 minutes. Check that the "
        "furnace or AC breaker is on and that the W or Y wire is firmly inserted.",
    ]),
    ("Thermostat Error Codes", [
        "The table below lists error codes shown on the T2 and T2 Pro display.",
    ]),
    ("AirPure Purifier: Filter and Light Indicators", [
        "The filter indicator on AirPure purifiers turns red when the HEPA filter needs replacing, "
        "which is typically every 6 months of daily use. After installing a new filter, press and "
        "hold the Filter button for 3 seconds to reset the indicator.",
        "If the air quality light stays red for more than an hour, close windows, check that the "
        "filter plastic wrap has been removed, and run the purifier on Turbo mode.",
        "A rattling noise usually means the filter is not seated correctly. Turn the purifier off, "
        "reseat the filter and close the cover until it clicks.",
    ]),
    ("Contacting Support", [
        "Chat support is available in the AeroHome app from 8 AM to 10 PM IST every day. Phone support "
        "is available on 1800-200-4455 (toll free) from 9 AM to 7 PM IST, Monday to Saturday.",
    ]),
]
SH_ERROR_TABLE = [
    ["Code", "Meaning", "What to do"],
    ["E1", "No power on the R wire", "Check the HVAC breaker and the R wire connection"],
    ["E2", "C-wire not detected", "Connect a C-wire or install the Power Extender Kit"],
    ["E3", "Wi-Fi authentication failed", "Re-enter the Wi-Fi password in the AeroHome app"],
    ["E4", "Temperature sensor fault", "Restart the thermostat; contact support if it persists"],
    ["E5", "HVAC system not responding", "Check the furnace/AC breaker and the W or Y wire"],
]

SH_WARRANTY_TXT = """AEROHOME WARRANTY AND RETURNS POLICY

WARRANTY COVERAGE
AeroHome products come with a limited warranty against manufacturing defects from the date of delivery:
- Smart Thermostat T1 Lite: 1 year
- Smart Thermostat T2: 2 years
- Smart Thermostat T2 Pro: 3 years
- AirPure P3 and AirPure P5 air purifiers: 1 year (HEPA filters are consumables and are not covered)
- SmartPlug S1 and Remote Sensor RS1: 1 year
The warranty does not cover damage from incorrect wiring, power surges, liquid damage, or repairs by unauthorised persons.

HOW TO CLAIM WARRANTY
1. Go to support.aerohome.example and choose Warranty Claim.
2. Enter the device serial number (starts with AH-) and upload the invoice or order confirmation.
3. Describe the issue and attach a photo or video if possible.
4. A support specialist reviews the claim within 2 business days and may run remote diagnostics.
5. If the claim is approved, a replacement unit is shipped within 5 business days and a prepaid return label is emailed for the faulty unit.

RETURNS
Products bought from the AeroHome online store can be returned within 30 days of delivery for any reason. Items must include all accessories and the original packaging. A restocking fee of 10 percent applies to opened products that are not defective. Products bought from other retailers follow that retailer's return policy.

REFUNDS
Refunds are issued to the original payment method within 7 to 10 business days after the returned item passes inspection at our warehouse.

AEROCARE+ EXTENDED PROTECTION
AeroCare+ costs Rs 1,499 per year per device and adds accidental damage protection and priority phone support. It must be purchased within 60 days of the original purchase.
"""

SH_SPECS_CSV = [
    ["Model", "Category", "Price (INR)", "Display", "Connectivity", "Matter support",
     "Voice assistants", "Warranty", "Key features", "Room coverage"],
    ["T1 Lite", "Smart thermostat", "8999", "Segment LED", "Wi-Fi 2.4 GHz", "No",
     "Alexa", "1 year", "Basic scheduling; no geofencing; requires C-wire", "Not applicable"],
    ["T2", "Smart thermostat", "14999", "2.4 inch colour LCD", "Wi-Fi 2.4 GHz, Bluetooth LE 5.0",
     "Yes", "Alexa, Google Assistant", "2 years",
     "Geofencing away mode; energy reports; Power Extender Kit sold separately", "Not applicable"],
    ["T2 Pro", "Smart thermostat", "21999", "3.5 inch colour touchscreen",
     "Wi-Fi 2.4/5 GHz, Bluetooth LE 5.0, Thread", "Yes", "Alexa, Google Assistant, Siri",
     "3 years", "Includes one Remote Sensor RS1 and Power Extender Kit; humidity sensor; air quality alerts",
     "Not applicable"],
    ["AirPure P3", "Air purifier", "11499", "LED ring", "Wi-Fi 2.4 GHz", "No",
     "Alexa, Google Assistant", "1 year", "True HEPA H13 filter; CADR 250 m3/h; noise 24 dB in sleep mode",
     "Up to 30 square metres"],
    ["AirPure P5", "Air purifier", "18999", "PM2.5 digital display", "Wi-Fi 2.4 GHz", "Yes",
     "Alexa, Google Assistant", "1 year",
     "True HEPA H13 plus activated carbon filter; CADR 450 m3/h; auto mode with PM2.5 sensor",
     "Up to 55 square metres"],
    ["SmartPlug S1", "Smart plug", "1299", "None", "Wi-Fi 2.4 GHz", "Yes",
     "Alexa, Google Assistant", "1 year", "16A rating; energy monitoring; schedules", "Not applicable"],
    ["Remote Sensor RS1", "Accessory", "2999", "None", "Bluetooth LE 5.0", "No", "None", "1 year",
     "Temperature and occupancy sensing for T2 and T2 Pro; battery life up to 2 years",
     "Not applicable"],
]


# =====================================================================================
# Writing the files
# =====================================================================================
def make_pdf(path: Path, title: str, sections) -> None:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(path), pagesize=A4, title=title, author="Sample KB generator",
                            leftMargin=2.2 * cm, rightMargin=2.2 * cm)

    def footer(canvas, d):
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {d.page}")

    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]
    for heading, paras in sections:
        story.append(Paragraph(heading.upper(), styles["Heading2"]))
        for p in paras:
            story.append(Paragraph(p, styles["BodyText"]))
            story.append(Spacer(1, 4))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def make_docx(path: Path, title: str, sections, table=None, table_after: str | None = None) -> None:
    import docx

    d = docx.Document()
    d.core_properties.title = title
    d.add_heading(title, level=0)
    for heading, paras in sections:
        d.add_heading(heading, level=1)
        for p in paras:
            if p[:2].rstrip(".").isdigit() and p[1:3].startswith("."):
                d.add_paragraph(p[3:].strip(), style="List Number")
            else:
                d.add_paragraph(p)
        if table and heading == table_after:
            t = d.add_table(rows=0, cols=len(table[0]))
            t.style = "Table Grid"
            for row in table:
                cells = t.add_row().cells
                for c, v in zip(cells, row):
                    c.text = v
    d.save(str(path))


def make_csv(path: Path, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> None:
    hr, sh = ROOT / "hr_policy", ROOT / "smart_home_support"
    hr.mkdir(parents=True, exist_ok=True)
    sh.mkdir(parents=True, exist_ok=True)

    make_pdf(hr / "employee_handbook.pdf", HR_HANDBOOK_TITLE, HR_HANDBOOK)
    make_docx(hr / "leave_policy.docx", HR_LEAVE_TITLE, HR_LEAVE, HR_LEAVE_TABLE, "Other Leave")
    (hr / "remote_work_it_faq.txt").write_text(HR_REMOTE_TXT, encoding="utf-8")
    make_csv(hr / "holiday_calendar_2026.csv", HR_HOLIDAYS_CSV)

    make_pdf(sh / "thermostat_t2_user_manual.pdf", SH_MANUAL_TITLE, SH_MANUAL)
    make_docx(sh / "troubleshooting_guide.docx", SH_TROUBLE_TITLE, SH_TROUBLE,
              SH_ERROR_TABLE, "Thermostat Error Codes")
    (sh / "warranty_and_returns.txt").write_text(SH_WARRANTY_TXT, encoding="utf-8")
    make_csv(sh / "product_specifications.csv", SH_SPECS_CSV)

    for p in sorted(ROOT.rglob("*.*")):
        print(f"{p.relative_to(ROOT)}  ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
