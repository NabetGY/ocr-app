from django.shortcuts import render
from PIL import Image
import pytesseract
from .forms import UploadFileForm
from django.template.context_processors import csrf
from django.http import HttpResponse

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Create your views here.
def hello(request):

    context = dict()
    context.update(csrf(request))

    if(request.method == "POST"):
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            image = Image.open(request.FILES['file'])
            image_text = pytesseract.image_to_string(image)
            context.update({'image_text': image_text})

            form = UploadFileForm()

            with open('texto_reconocido.txt', 'w') as f:
                f.write(image_text)

            # Crear una respuesta de descarga para el archivo de texto
            response = HttpResponse(open('texto_reconocido.txt', 'rb'), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="texto_reconocido.txt"'
            return response
        else:
            form = UploadFileForm()

    else:
        form = UploadFileForm()
        context.update({'form': form})

    return render(request,'hello.html', context)