from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import APIView, permission_classes
from .create_pdf import create_pdf
from rest_framework.permissions import AllowAny
from .model_mapping import MODEL_MAPPING

# Create your views here.

@permission_classes([AllowAny])
class Get_Pdf(APIView):

    def get(self, request, route):

        # user = request.user
        # print(user, 'user')

        # create_pdf(user, user.id)

        # # Open the PDF file
        # with open('wagubumbuzi.pdf', 'rb') as pdf_file:
        #     response = FileResponse(pdf_file, content_type='application/pdf')
        #     response['Content-Disposition'] = 'attachment; filename="wagubumbuzi.pdf"'
        #     return response

        # pick route from url
        # route = request.GET.get('route')
        user = request.GET.get('user')
        model_class = MODEL_MAPPING.get(route.lower())  # Get model class from route
        if not model_class:
            return HttpResponse(f"Invalid route parameter: {route}", status=400)

        buffer = create_pdf(model_class, user)

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=f'{route}.pdf', content_type='application/pdf')

       

