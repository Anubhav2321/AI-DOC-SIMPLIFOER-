from fpdf import FPDF

# PDF class creation
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sample Rental Agreement (Legal Draft)', 0, 1, 'C')
        self.ln(10)

# create PDF instance
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Difficult legal text (for testing AI)
complex_text = """
This LEASE AGREEMENT (hereinafter referred to as the "Agreement") is made and entered into this 12th day of January, 2026, by and between the Landlord and the Tenant.

WHEREAS, the Landlord is the legal owner of the premises described below; and
WHEREAS, the Tenant desires to lease the premises under the terms and conditions set forth herein;

NOW, THEREFORE, in consideration of the mutual covenants and promises herein contained, the parties agree as follows:

1. INDEMNIFICATION: The Tenant agrees to indemnify, defend, and hold harmless the Landlord from and against any and all claims, actions, suits, judgments, damages, costs, and expenses (including reasonable attorney's fees) arising out of or resulting from the Tenant's use or occupancy of the Premises.

2. FORCE MAJEURE: Neither party shall be liable for any failure or delay in performing their obligations where such failure or delay results from any cause that is beyond the reasonable control of that party. Such causes include, but are not limited to, power outages, internet service provider failures, riots, insurrections, civil unrest, fires, floods, storms, earthquakes, acts of God, or other events of "Force Majeure."

3. TERMINATION CLAUSE: In the event of a material breach of this Agreement by the Tenant, the Landlord shall have the right to terminate this Agreement immediately upon providing written notice to the Tenant. Upon such termination, the Tenant shall vacate the premises within 72 hours.
"""

# add the text to PDF
pdf.multi_cell(0, 10, complex_text)

# save the pdf with name .pdf
pdf.output("test_document.pdf")

print("✅ PDF created successfully! Check your folder for 'test_document.pdf'.")