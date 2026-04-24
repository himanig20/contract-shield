from utils import generate_pdf_report
from rules import analyze_contract
contract = "EMPLOYMENT CONTRACT\n\n1. The employee agrees to work a minimum of 10 hours per day, 6 days a week, with no additional compensation for overtime as deemed fit by management.\n\n2. The company reserves the right to terminate the employee immediately without prior notice and without payment of pending dues.\n\n3. In case of any breach, a penalty of Rs. 5000 per day shall be charged, compounded daily until the amount is recovered in full.\n\n4. The employee waives all rights to legal action against the company for any workplace injury or illness sustained during employment.\n\n5. The employer may deduct from wages any amount as determined by management at sole discretion for damages, losses, or misconduct.\n\n6. The employee shall not engage in or work for any competing business for a period of 3 years after leaving the company, across all of India."
findings = analyze_contract(contract)
pdf_data = generate_pdf_report(findings, 24, "Labor Contract")
if pdf_data:
    print("Success")
else:
    print("Failed")
