
def stuff(doc, content):
    doc.append(content)

def build(doc, filename):
    doc.generate_pdf(filename, clean_tex=False)

