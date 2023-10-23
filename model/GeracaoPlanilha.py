class geracaoPlanilha:
    def __init__(self):
        self.name = ""
        self.email = ""

    def set_data(self, name, email):
        self.name = name
        self.email = email

    def generate_pdf(self):
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_pdf.name, pagesize=landscape(letter))
        c.drawString(100, 500, f"Nome: {self.name}")
        c.drawString(100, 450, f"Email: {self.email}")
        c.showPage()
        c.save()
        return temp_pdf.name