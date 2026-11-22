# Milestone 2 Evaluation Results

## 1. Query Understanding Agent: classification

**Accuracy: 41 of 41 (100.0%)**

| Expected \ Predicted | factual | procedural | comparative | ambiguous |
|---|---|---|---|---|
| **factual** | 13 | 0 | 0 | 0 |
| **procedural** | 0 | 10 | 0 | 0 |
| **comparative** | 0 | 0 | 10 | 0 |
| **ambiguous** | 0 | 0 | 0 | 8 |

| Query | Expected | Predicted | Confidence | Method | Route | |
|---|---|---|---|---|---|---|
| How many days of casual leave do employees get per year? | factual | factual | 0.85 | rules | single_search | ✔ |
| What are the core collaboration hours? | factual | factual | 0.8 | rules | single_search | ✔ |
| When is the Diwali holiday? | factual | factual | 0.8 | rules | single_search | ✔ |
| What is the notice period during probation? | factual | factual | 0.8 | rules | single_search | ✔ |
| Is there a shift allowance for night shifts? | factual | factual | 0.8 | rules | single_search | ✔ |
| um what's the minimum password length | factual | factual | 0.8 | rules | single_search | ✔ |
| Who approves fully remote work? | factual | factual | 0.8 | rules | single_search | ✔ |
| What does error code E3 mean? | factual | factual | 0.8 | rules | single_search | ✔ |
| What is the price of the AirPure P5? | factual | factual | 0.8 | rules | single_search | ✔ |
| How often should I replace the HEPA filter? | factual | factual | 0.85 | rules | single_search | ✔ |
| Does the T2 work with 5 GHz Wi-Fi? | factual | factual | 0.8 | rules | single_search | ✔ |
| What is the toll free support number? | factual | factual | 0.8 | rules | single_search | ✔ |
| Warranty period of the T2 Pro | factual | factual | 0.5 | rules | single_search | ✔ |
| How do I apply for earned leave? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| What should I do if my laptop is stolen? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How can I request to work fully remote? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How do I raise a grievance? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| Steps to submit a reimbursement claim | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How do I factory reset the thermostat? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How do I connect the T2 to Wi-Fi? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How to install the smart thermostat | procedural | procedural | 0.85 | rules | single_search | ✔ |
| What is the process to claim warranty for a faulty device? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| How should I reset the filter indicator after replacing the filter? | procedural | procedural | 0.85 | rules | single_search | ✔ |
| What is the difference between casual leave and sick leave? | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Compare the notice period during probation and after confirmation | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Which gives more days, earned leave or sick leave? | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Metro vs non-metro per diem | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Is maternity leave longer than adoption leave? | comparative | comparative | 0.9 | rules | single_search | ✔ |
| What is the difference between the T2 and the T2 Pro? | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Which purifier covers a bigger room, AirPure P3 or AirPure P5? | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Compare the warranty of the T1 Lite and the T2 Pro | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| Is the T2 Pro better than the T1 Lite for Siri users? | comparative | comparative | 0.9 | rules | single_search | ✔ |
| AirPure P3 versus AirPure P5 noise level | comparative | comparative | 0.9 | rules | multi_search | ✔ |
| leave | ambiguous | ambiguous | 0.8 | rules | clarification | ✔ |
| What about it? | ambiguous | ambiguous | 0.95 | rules | clarification | ✔ |
| policy | ambiguous | ambiguous | 0.8 | rules | clarification | ✔ |
| tell me more | ambiguous | ambiguous | 0.95 | rules | clarification | ✔ |
| warranty | ambiguous | ambiguous | 0.8 | rules | clarification | ✔ |
| and that one? | ambiguous | ambiguous | 0.9 | rules | clarification | ✔ |
| help | ambiguous | ambiguous | 0.8 | rules | clarification | ✔ |
| How about this? | ambiguous | ambiguous | 0.95 | rules | clarification | ✔ |

## 2. Retrieval Agent: retrieval quality

Top-5 search (more for comparative queries), ranked by score, chunks below 0.45 filtered out.

| Query type | Correct | Meaning of correct |
|---|---|---|
| factual | 14 of 16 (87.5%) | a relevant chunk is kept |
| procedural | 8 of 8 (100.0%) | a relevant chunk is kept |
| comparative | 7 of 8 (87.5%) | a relevant chunk is kept |
| unavailable | 7 of 8 (87.5%) | no chunk kept (handled as 'not found') |

| ID | Type | Query | Kept | Filtered out | Top score | Result |
|---|---|---|---|---|---|---|
| HR-F1 | factual | How many days of casual leave do employees get per year? | 5 | 0 | 0.802 | relevant chunk at rank 1 |
| HR-F2 | factual | What are the core collaboration hours? | 1 | 4 | 0.527 | relevant chunk at rank 1 |
| HR-F3 | factual | What is the notice period for people managers after confirmation? | 2 | 3 | 0.618 | relevant chunk at rank 1 |
| HR-F4 | factual | How much internet reimbursement do remote employees get? | 2 | 3 | 0.515 | relevant chunk at rank 2 |
| HR-F5 | factual | When is the Diwali holiday this year? | 5 | 0 | 0.683 | relevant chunk at rank 1 |
| HR-F6 | factual | um what's the minimum password length | 1 | 4 | 0.629 | relevant chunk at rank 1 |
| HR-F7 | factual | How long is paternity leave? | 1 | 4 | 0.722 | relevant chunk at rank 1 |
| HR-F8 | factual | What is the annual learning budget per employee? | 1 | 4 | 0.703 | relevant chunk at rank 1 |
| HR-P1 | procedural | How do I apply for earned leave? | 2 | 3 | 0.513 | relevant chunk at rank 1 |
| HR-P2 | procedural | What should I do if my laptop is stolen? | 1 | 4 | 0.684 | relevant chunk at rank 1 |
| HR-P3 | procedural | How can I request to work fully remote? | 1 | 4 | 0.689 | relevant chunk at rank 1 |
| HR-P4 | procedural | How do I raise a grievance? | 1 | 4 | 0.641 | relevant chunk at rank 1 |
| HR-C1 | comparative | What is the difference between casual leave and sick leave? | 3 | 4 | 0.655 | relevant chunk at rank 1 |
| HR-C2 | comparative | Compare the notice period during probation and after confirmation | 1 | 6 | 0.724 | relevant chunk at rank 1 |
| HR-C3 | comparative | How does the per diem for metro cities compare with non-metro cities? | 0 | 5 | 0.411 | MISSED |
| HR-C4 | comparative | Which gives more days, earned leave or sick leave? | 5 | 1 | 0.676 | relevant chunk at rank 1 |
| HR-U1 | unavailable | What is the employee stock option vesting schedule? | 0 | 5 | 0.354 | no results (correct) |
| HR-U2 | unavailable | How much is the gym membership reimbursement? | 0 | 5 | 0.386 | no results (correct) |
| HR-U3 | unavailable | What is the dress code on Fridays? | 0 | 5 | 0.341 | no results (correct) |
| HR-U4 | unavailable | How much is the employee referral bonus? | 0 | 5 | 0.361 | no results (correct) |
| SH-F1 | factual | What Wi-Fi frequency does the T2 thermostat support? | 5 | 0 | 0.608 | relevant chunk at rank 1 |
| SH-F2 | factual | What does error code E3 mean? | 0 | 5 | 0.346 | MISSED |
| SH-F3 | factual | How long is the warranty on the T2 Pro? | 4 | 1 | 0.592 | relevant chunk at rank 1 |
| SH-F4 | factual | What is the price of the AirPure P5? | 3 | 2 | 0.574 | relevant chunk at rank 1 |
| SH-F5 | factual | what are the default eco temperatures | 1 | 4 | 0.574 | relevant chunk at rank 1 |
| SH-F6 | factual | How often should I replace the HEPA filter? | 0 | 5 | 0.394 | MISSED |
| SH-F7 | factual | What is the toll free support number? | 1 | 4 | 0.545 | relevant chunk at rank 1 |
| SH-F8 | factual | How long do refunds take? | 2 | 3 | 0.811 | relevant chunk at rank 1 |
| SH-P1 | procedural | How do I factory reset the thermostat? | 2 | 3 | 0.766 | relevant chunk at rank 1 |
| SH-P2 | procedural | How do I connect the T2 to Wi-Fi? | 1 | 4 | 0.647 | relevant chunk at rank 1 |
| SH-P3 | procedural | How do I install the smart thermostat? | 2 | 3 | 0.584 | relevant chunk at rank 1 |
| SH-P4 | procedural | How do I claim warranty for a faulty device? | 2 | 3 | 0.659 | relevant chunk at rank 1 |
| SH-C1 | comparative | What is the difference between the T2 and the T2 Pro? | 5 | 1 | 0.596 | relevant chunk at rank 1 |
| SH-C2 | comparative | Which purifier covers a bigger room, AirPure P3 or AirPure P5? | 2 | 5 | 0.608 | relevant chunk at rank 1 |
| SH-C3 | comparative | Compare the warranty of the T1 Lite and the T2 Pro | 6 | 1 | 0.596 | relevant chunk at rank 2 |
| SH-C4 | comparative | Is the T2 Pro or the T1 Lite better for Siri users? | 3 | 4 | 0.596 | relevant chunk at rank 1 |
| SH-U1 | unavailable | What is the battery life of the AeroHome smart lock? | 0 | 5 | 0.38 | no results (correct) |
| SH-U2 | unavailable | Does AeroHome sell solar panels? | 0 | 5 | 0.4 | no results (correct) |
| SH-U3 | unavailable | Can I pair the thermostat with a Zigbee hub? | 1 | 4 | 0.49 | 1 chunk(s) kept (wrong) |
| SH-U4 | unavailable | What is the price of the AeroHome video doorbell? | 0 | 5 | 0.433 | no results (correct) |

## 3. End-to-end: Response Generation Agent through the orchestrator

**Passed: 12 of 14** (status as expected, answer contains the key fact, expected document cited; unavailable questions must return 'not found')

| Question | Type | Status | Confidence | Sources | Words | Pass | Answer |
|---|---|---|---|---|---|---|---|
| How many days of casual leave do employees get per year? | factual | answered | High | 2 | 10 | ✔ | Employees receive 8 days of casual leave per year. [1][4] |
| When is the Diwali holiday? | factual | answered | High | 1 | 16 | ✔ | The Diwali holiday is on Monday, 2026‑11‑09, and it is a mandatory holiday for all offices[1]. |
| What does error code E3 mean? | factual | not_found | None | 0 | 24 | ✘ | Sorry, I couldn't find enough information in the knowledge base to answer this. Try rephrasing the question or upload a document that covers it. |
| What is the price of the AirPure P5? | factual | answered | Medium | 1 | 8 | ✔ | The AirPure P5 is priced at ₹18,999 [1]. |
| How do I apply for earned leave? | procedural | answered | Low | 1 | 67 | ✔ | 1. Log in to PeopleHub and open the Leave section.[1]   2. Select “Earned Leave” as the leave type and choose the desired dates.[1]   3. Review the available earned‑leave balance shown by the system.[1]   4. If the leave exceeds 3 days, submit the request at least 7 days before the start date.[1]   5. Submit the request; your reporting manager will approve or reject it within 3 working days.[1] |
| What should I do if my laptop is stolen? | procedural | answered | High | 1 | 39 | ✔ | 1. Email security@nimbustech.example within 4 hours to report the stolen laptop. [1]   2. Call the IT Helpdesk on extension 4040 to report the theft. [1]   3. Provide a copy of the police FIR (report) for the stolen device. [1] |
| How do I factory reset the thermostat? | procedural | answered | High | 1 | 33 | ✔ | 1. Press and hold the thermostat’s dial for 15 seconds until the LED ring turns red. [1]   2. Release the dial. [1]   3. Wait about one minute for the thermostat to restart. [1] |
| How do I claim warranty for a faulty device? | procedural | answered | High | 1 | 83 | ✔ | 1. Go to support.aerohome.example and choose “Warranty Claim.” [1]   2. Enter the device serial number (starts with AH‑) and upload the invoice or order confirmation. [1]   3. Describe the issue and attach a photo or video if possible. [1]   4. A support specialist reviews the claim within 2 business days and may run remote diagnostics. [1]   5. If the claim is approved, a replacement unit is shipped within 5 business days and a prepaid return label is emailed for the faulty unit. [1] |
| What is the difference between casual leave and sick leave? | comparative | answered | High | 3 | 130 | ✔ | - **Annual quota**: Casual leave = 8 days per year; Sick leave = 10 days per year[1][2].   - **Carry‑forward**: Casual leave cannot be carried forward; Sick leave can carry forward up to 20 days[1][2].   - **Maximum consecutive days**: Casual leave cannot exceed 3 consecutive days; Sick leave requires a medical certificate only after 2 consecutive days (no explicit limit on length)[1][2].   - **Medical documentation**: No certificate needed for casual leave; a certificate from a registered medical practitioner is required for sick leave longer than 2 consecutive days[2].   - **Encashability**: Neither casual nor sick leave is encashable[3].    **Main difference**: Casual leave offers fewer days, cannot be carried forward, and has a strict three‑day consecutive limit, whereas sick leave provides more days, allows carry‑forward, and requires a medical certificate for longer absences. |
| Which purifier covers a bigger room, AirPure P3 or AirPure P5? | comparative | answered | Medium | 2 | 35 | ✔ | - **AirPure P3** – Room coverage: up to 30 square metres[2]   - **AirPure P5** – Room coverage: up to 55 square metres[1]  **Summary:** The AirPure P5 can cover a larger room than the AirPure P3. |
| What is the dress code on Fridays? | factual | not_found | None | 0 | 24 | ✔ | Sorry, I couldn't find enough information in the knowledge base to answer this. Try rephrasing the question or upload a document that covers it. |
| How much is the gym membership reimbursement? | factual | not_found | None | 0 | 24 | ✔ | Sorry, I couldn't find enough information in the knowledge base to answer this. Try rephrasing the question or upload a document that covers it. |
| Does AeroHome sell solar panels? | factual | not_found | None | 0 | 24 | ✔ | Sorry, I couldn't find enough information in the knowledge base to answer this. Try rephrasing the question or upload a document that covers it. |
| Can I pair the thermostat with a Zigbee hub? | factual | answered | Low | 1 | 20 | ✘ | No. The thermostat pairs only via 2.4 GHz Wi‑Fi using the AeroHome app; it does not support Zigbee connections. [1] |
