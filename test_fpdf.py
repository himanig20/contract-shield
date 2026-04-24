from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', '', 12)
pdf.multi_cell(0, 10, "Smart quotes “hello” and dash –.")
pdf.output()
print("Success")
