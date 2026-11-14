# Retrieval Evaluation Results

Model: all-MiniLM-L6-v2 · 69 chunks · 40 questions · threshold 0.45

## Accuracy by question type

| Type | Questions | Top-1 % | Top-3 % | Top-5 % | MRR |
|---|---|---|---|---|---|
| factual | 16 | 93.8 | 100.0 | 100.0 | 0.969 |
| procedural | 8 | 100.0 | 100.0 | 100.0 | 1.0 |
| comparative | 8 | 100.0 | 100.0 | 100.0 | 1.0 |
| **all answerable** | 32 | **96.9** | **100.0** | **100.0** | **0.984** |
| domain: hr_policy | 16 | 93.8 | 100.0 | 100.0 | 0.969 |
| domain: smart_home_support | 16 | 100.0 | 100.0 | 100.0 | 1.0 |

## Unavailable-information questions

- Correctly rejected (top score below 0.45): 7 of 8
- Answerable questions wrongly rejected: 3 of 32

## Threshold comparison

| Threshold | Unavailable rejected | Answerable kept |
|---|---|---|
| 0.35 | 1 of 8 | 31 of 32 |
| 0.4 | 5 of 8 | 30 of 32 |
| 0.45 | 7 of 8 | 29 of 32 |
| 0.5 | 8 of 8 | 28 of 32 |
| 0.55 | 8 of 8 | 23 of 32 |

## Every question

| ID | Type | Question | Top-1 file | Top score | Result |
|---|---|---|---|---|---|
| HR-F1 | factual | How many days of casual leave do employees get per year? | leave_policy.docx | 0.802 | correct at rank 1 |
| HR-F2 | factual | What are the core collaboration hours? | employee_handbook.pdf | 0.527 | correct at rank 1 |
| HR-F3 | factual | What is the notice period for people managers after confirmation? | employee_handbook.pdf | 0.618 | correct at rank 1 |
| HR-F4 | factual | How much internet reimbursement do remote employees get? | remote_work_it_faq.txt | 0.515 | correct at rank 2 |
| HR-F5 | factual | When is the Diwali holiday this year? | holiday_calendar_2026.csv | 0.683 | correct at rank 1 |
| HR-F6 | factual | um what's the minimum password length | remote_work_it_faq.txt | 0.621 | correct at rank 1 |
| HR-F7 | factual | How long is paternity leave? | leave_policy.docx | 0.722 | correct at rank 1 |
| HR-F8 | factual | What is the annual learning budget per employee? | employee_handbook.pdf | 0.703 | correct at rank 1 |
| HR-P1 | procedural | How do I apply for earned leave? | leave_policy.docx | 0.513 | correct at rank 1 |
| HR-P2 | procedural | What should I do if my laptop is stolen? | remote_work_it_faq.txt | 0.684 | correct at rank 1 |
| HR-P3 | procedural | How can I request to work fully remote? | remote_work_it_faq.txt | 0.689 | correct at rank 1 |
| HR-P4 | procedural | How do I raise a grievance? | employee_handbook.pdf | 0.641 | correct at rank 1 |
| HR-C1 | comparative | What is the difference between casual leave and sick leave? | leave_policy.docx | 0.607 | correct at rank 1 |
| HR-C2 | comparative | Compare the notice period during probation and after confirmation | employee_handbook.pdf | 0.698 | correct at rank 1 |
| HR-C3 | comparative | How does the per diem for metro cities compare with non-metro cities? | employee_handbook.pdf | 0.411 | correct at rank 1, low relevance |
| HR-C4 | comparative | Which gives more days, earned leave or sick leave? | leave_policy.docx | 0.676 | correct at rank 1 |
| HR-U1 | unavailable | What is the employee stock option vesting schedule? | leave_policy.docx | 0.354 | rejected (correct) |
| HR-U2 | unavailable | How much is the gym membership reimbursement? | employee_handbook.pdf | 0.386 | rejected (correct) |
| HR-U3 | unavailable | What is the dress code on Fridays? | employee_handbook.pdf | 0.341 | rejected (correct) |
| HR-U4 | unavailable | How much is the employee referral bonus? | employee_handbook.pdf | 0.361 | rejected (correct) |
| SH-F1 | factual | What Wi-Fi frequency does the T2 thermostat support? | thermostat_t2_user_manual.pdf | 0.608 | correct at rank 1 |
| SH-F2 | factual | What does error code E3 mean? | troubleshooting_guide.docx | 0.346 | correct at rank 1, low relevance |
| SH-F3 | factual | How long is the warranty on the T2 Pro? | warranty_and_returns.txt | 0.592 | correct at rank 1 |
| SH-F4 | factual | What is the price of the AirPure P5? | product_specifications.csv | 0.574 | correct at rank 1 |
| SH-F5 | factual | what are the default eco temperatures | thermostat_t2_user_manual.pdf | 0.574 | correct at rank 1 |
| SH-F6 | factual | How often should I replace the HEPA filter? | troubleshooting_guide.docx | 0.394 | correct at rank 1, low relevance |
| SH-F7 | factual | What is the toll free support number? | troubleshooting_guide.docx | 0.545 | correct at rank 1 |
| SH-F8 | factual | How long do refunds take? | warranty_and_returns.txt | 0.811 | correct at rank 1 |
| SH-P1 | procedural | How do I factory reset the thermostat? | thermostat_t2_user_manual.pdf | 0.766 | correct at rank 1 |
| SH-P2 | procedural | How do I connect the T2 to Wi-Fi? | thermostat_t2_user_manual.pdf | 0.647 | correct at rank 1 |
| SH-P3 | procedural | How do I install the smart thermostat? | thermostat_t2_user_manual.pdf | 0.584 | correct at rank 1 |
| SH-P4 | procedural | How do I claim warranty for a faulty device? | warranty_and_returns.txt | 0.659 | correct at rank 1 |
| SH-C1 | comparative | What is the difference between the T2 and the T2 Pro? | product_specifications.csv | 0.566 | correct at rank 1 |
| SH-C2 | comparative | Which purifier covers a bigger room, AirPure P3 or AirPure P5? | product_specifications.csv | 0.532 | correct at rank 1 |
| SH-C3 | comparative | Compare the warranty of the T1 Lite and the T2 Pro | warranty_and_returns.txt | 0.576 | correct at rank 1 |
| SH-C4 | comparative | Is the T2 Pro or the T1 Lite better for Siri users? | product_specifications.csv | 0.472 | correct at rank 1 |
| SH-U1 | unavailable | What is the battery life of the AeroHome smart lock? | warranty_and_returns.txt | 0.38 | rejected (correct) |
| SH-U2 | unavailable | Does AeroHome sell solar panels? | troubleshooting_guide.docx | 0.4 | rejected (correct) |
| SH-U3 | unavailable | Can I pair the thermostat with a Zigbee hub? | thermostat_t2_user_manual.pdf | 0.49 | NOT rejected (wrong) |
| SH-U4 | unavailable | What is the price of the AeroHome video doorbell? | warranty_and_returns.txt | 0.433 | rejected (correct) |
