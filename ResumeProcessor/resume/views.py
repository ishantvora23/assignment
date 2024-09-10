from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pdfplumber
import os
import re

@api_view(['POST'])
def extract_resume(request):
    if 'resume' not in request.FILES:
        return Response({"error": "No resume file provided."}, status=status.HTTP_400_BAD_REQUEST)

    resume_file = request.FILES['resume']
    if not resume_file.name.endswith('.pdf'):
        return Response({"error": "Invalid file format. Only PDF documents are accepted."}, status=status.HTTP_400_BAD_REQUEST)

    # Save the uploaded file to a temporary location
    file_path = os.path.join('temp', resume_file.name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as temp_file:
        for chunk in resume_file.chunks():
            temp_file.write(chunk)

    try:
        # Extract text from PDF using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

        # Basic extraction logic (This will vary based on resume formatting)
        first_name = None
        email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        mobile_number = re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

        # Simple name extraction (improve as needed)
        if text:
            lines = text.split('\n')
            if lines:
                first_name = lines[0].split()[0]

        # Prepare the response data
        extracted_data = {
            "first_name": first_name,
            "email": email.group() if email else '',
            "mobile_number": mobile_number.group() if mobile_number else ''
        }

        # Clean up the temporary file
        os.remove(file_path)

        return Response(extracted_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any errors that occur during parsing
        os.remove(file_path)  # Clean up the temporary file
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
