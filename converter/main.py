import os
import platform
import fitz  # Import the PyMuPDF library
import subprocess
from io import BytesIO
from fpdf import FPDF
from docx2pdf import convert as convert_docx_to_pdf
from PIL import Image

def get_extension(filename):
    return filename.split('.')[-1].lower()

def convert_to_pdf(file):
    extension = get_extension(file.name)
    content = file.read()  # Read the content of the uploaded file

   

    if extension in ('jpg', 'jpeg', 'png'):
        # Convert image to PDF using fpdf
        pdf = FPDF()
        pdf.add_page()
        img = Image.open(BytesIO(content))
        width, height = img.size
        aspect_ratio = height / width
        pdf.image(BytesIO(content), w=210, h=210 * aspect_ratio)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output.read()

    elif extension in ('doc', 'docx'):
        # Convert DOC and DOCX files to PDF using docx2pdf
        pdf_content = convert_docx_to_pdf(content)
        return pdf_content
    
    elif extension == 'txt':
    # Convert text file to PDF using fpdf
       pdf = FPDF()
       pdf.add_page()
       pdf.set_font("Arial", size=12)
    
       pdf.multi_cell(0, 10, content.decode('utf-8'))
       pdf_output = BytesIO()
       pdf.output(pdf_output)
       pdf_output.seek(0)
       return pdf_output.read()

    else:
        # Use unoconv to convert the file to PDF
        temp_file_path = os.path.join(os.path.dirname(__file__), 'temp_input' + '.' + extension)
        pdf_file_path = os.path.join(os.path.dirname(__file__), 'temp_output.pdf')

        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(content)

        try:
            subprocess.run(['unoconv', '--output', os.path.dirname(__file__), '--format', 'pdf', temp_file_path])
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            os.remove(pdf_file_path)
        except Exception as e:
            pdf = FPDF()
            pdf.add_page()
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            pdf_content = pdf_output.read()

        os.remove(temp_file_path)
        return pdf_content

if __name__ == '__main__':
    print("This Is The Main Backend Module!")
