from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
import os
from .forms import UploadFileForm
from .main import convert_to_pdf

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="converted.pdf"'

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            if file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = Image(file, width=500, height=600)
                elements.append(img)
            else:
                pdf_content = convert_to_pdf(file)
                elements.append(pdf_content)

            doc.build(elements)

            pdf = buffer.getvalue()
            buffer.close()

            response.write(pdf)
            return response
    else:
        form = UploadFileForm()

    return render(request, 'indexx.html', {'form': form})
