from pdfquery import PDFQuery

pdf = PDFQuery('pdf/G10-2.pdf')
pdf.load()

# Use CSS-like selectors to locate the elements
text_elements = pdf.pq('LTTextLineHorizontal')

# Extract the text from the elements
text = [t.text for t in text_elements]

text_string = ""
for i in text:
    text_string += i

with open("G10-2.txt", "w", encoding="utf-8") as f:
    f.write(text_string)