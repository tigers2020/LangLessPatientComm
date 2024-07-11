# Import necessary libraries
import json
import logging
import os

import easyocr
import spacy  # Import spaCy library for Named Entity Recognition
import torch
from django.http import HttpResponseServerError, JsonResponse, HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from gtts import gTTS

from .forms import ImageUploadForm  # importing the ImageUploadForm from forms
from .models import ImageUpload  # importing the ImageUpload model from models

# Creating logger for capturing log messages
logger = logging.getLogger(__name__)

# Loading spaCy model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")


# This class represents a view to handle the image upload request. Inherits from CreateView in Django
class ImageUploadView(CreateView):
    model = ImageUpload  # assign model to use
    form_class = ImageUploadForm  # assign form to use
    template_name = 'components/pages/ocr_app/upload_image.html'  # assign html page to use

    # Method to handle valid form submission

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('extract_text')})
        return super().form_valid(form)

    # Method to redirect to success url
    def get_success_url(self):
        return reverse('extract_text')


# This class is responsible for extracting text from the uploaded image. Inherits from TemplateView in Django
class ExtractTextView(TemplateView):
    template_name = 'components/pages/ocr_app/extract_text.html'  # assign html page to use

    # Method to generate context data for rendering in the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            latest_image = ImageUpload.objects.latest('uploaded_at')
            img_path = latest_image.image.path
            # Initialize EasyOCR with GPU
            reader = easyocr.Reader(['en'], gpu=True)
            # Check whether GPU or CPU is used
            if torch.cuda.is_available():
                logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                logger.warning("GPU not available. Using CPU.")
            result = reader.readtext(img_path)
            text = ' '.join([item[1] for item in result])
            context['text'] = text
            context['prescription_info'] = self.extract_information(text)
        except Exception as e:
            logger.error(f"Error in ExtractTextView: {str(e)}")
            return HttpResponseServerError("An error occurred while processing the image.")
        return context

    # This method is used to extract informational entities from the text using spaCy's NER
    @staticmethod
    def extract_information(text):
        doc = nlp(text)
        extracted_data = {
            "entities": []
        }
        for ent in doc.ents:
            extracted_data["entities"].append({
                "text": ent.text,
                "label": ent.label_
            })
        return extracted_data


# This function is used to convert text to speech, the speech file is then streamed back to the client
def text_to_speech(request):
    global tts_file
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            if not text:
                return JsonResponse({'error': 'No text provided for TTS'}, status=400)
            tts = gTTS(text)
            tts_file = 'tts_output.mp3'
            tts.save(tts_file)
            with open(tts_file, 'rb') as audio:
                response = HttpResponse(audio.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{tts_file}"'
                return response
        except Exception as e:
            logger.error(f"Error in text_to_speech: {str(e)}")
            return HttpResponseServerError("An error occurred while generating the TTS.")
        finally:
            if os.path.exists(tts_file):
                os.remove(tts_file)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
