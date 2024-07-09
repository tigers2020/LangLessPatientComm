# ocr_app/views.py
import json
import logging
import os
import re

import easyocr
import torch
from django.http import HttpResponseServerError
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import TemplateView
from gtts import gTTS

from .forms import ImageUploadForm
from .models import ImageUpload

logger = logging.getLogger(__name__)


class ImageUploadView(CreateView):
    model = ImageUpload
    form_class = ImageUploadForm
    template_name = 'components/pages/ocr_app/upload_image.html'

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': reverse('extract_text')})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('extract_text')


class ExtractTextView(TemplateView):
    template_name = 'components/pages/ocr_app/extract_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            latest_image = ImageUpload.objects.latest('uploaded_at')
            img_path = latest_image.image.path

            # Initialize EasyOCR with GPU support
            reader = easyocr.Reader(['en'], gpu=True)

            # Verify GPU usage
            if torch.cuda.is_available():
                logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                logger.warning("GPU not available. Using CPU.")

            result = reader.readtext(img_path)
            text = ' '.join([item[1] for item in result])

            context['text'] = text
            context['prescription_info'] = self.extract_prescription(text)
        except Exception as e:
            logger.error(f"Error in ExtractTextView: {str(e)}")
            return HttpResponseServerError("An error occurred while processing the image.")

        return context

    @staticmethod
    def extract_prescription(text):
        # Define regex patterns for each category
        patterns = {
            "pharmacy_info": {
                "name": re.compile(r'Pharmacy name\s*&\s*address\s*(.*?)\s*Patient', re.IGNORECASE),
                "address": re.compile(r'address\s*(.*?)\s*Patient', re.IGNORECASE),
                "phone_number": re.compile(r'Pharmacy phone number\s*(.*?)\s*Date', re.IGNORECASE)
            },
            "patient_info": {
                "name": re.compile(r'Patient name\s*&\s*address\s*(.*?)\s*Name & strength', re.IGNORECASE),
                "address": re.compile(r'address\s*(.*?)\s*Name & strength', re.IGNORECASE)
            },
            "prescription_info": {
                "rx_number": re.compile(
                    r'Number used by pharmacy to identify your prescription\s*Rx\s*:\s*(.*?)\s*Refill', re.IGNORECASE),
                "refill_number": re.compile(r'Refill\s*:\s*(\d+)', re.IGNORECASE),
                "doctor_name": re.compile(r'Your doctor\'s name\s*(.*?)\s*Pharmacy phone number', re.IGNORECASE),
                "date_prescription_written": re.compile(r'Date prescription was written\s*(.*?)\s*Date drug was filled',
                                                        re.IGNORECASE),
                "date_filled": re.compile(r'Date drug was filled by pharmacy\s*(.*?)\s*Pharmacist in charge',
                                          re.IGNORECASE),
                "pharmacist": re.compile(r'Pharmacist in charge\s*(.*?)\s*Discard After', re.IGNORECASE),
                "location": re.compile(r'LOCATION\s*:\s*(.*?)\s*Filled On', re.IGNORECASE),
                "discard_after": re.compile(r'Discard After\s*:\s*(.*?)\s*CAUTION', re.IGNORECASE),
                "qty_filled": re.compile(r'Qty Filled\s*:\s*(.*?)\s*Number of pills in bottle', re.IGNORECASE),
                "reorder_after": re.compile(r'Reorder After\s*:\s*(.*?)\s*Qty Filled', re.IGNORECASE)
            },
            "drug_info": {
                "name": re.compile(r'Dispensed\s*:\s*(.*?)\s*instructions', re.IGNORECASE),
                "instructions": re.compile(r'instructions\s*(.*?)\s*Pill Markings', re.IGNORECASE),
                "pill_markings": re.compile(r'Pill Markings\s*:\s*(.*?)\s*Physical description', re.IGNORECASE),
                "manufacturer": re.compile(r'MFR\s*:\s*(.*?)\s*NDCIUPC', re.IGNORECASE),
                "ndc_upc": re.compile(r'NDCIUPC\s*:\s*(.*?)\s*LOCATION', re.IGNORECASE)
            },
            "caution": {
                "federal_law": re.compile(
                    r'CAUTION\s*:\s*(FEDERAL LAW PROHIBITS TRANSFER OF THIS DRUG TO ANY PERSON OTHER THAN THE PATIENT FOR WHOM PRESCRIBED)',
                    re.IGNORECASE),
                "do_not_use_after": re.compile(r'Discard After\s*:\s*(.*?)\s*CAUTION', re.IGNORECASE)
            }
        }

        prescription_data = {}

        for category, fields in patterns.items():
            prescription_data[category] = {}
            for field, pattern in fields.items():
                match = pattern.search(text)
                if match:
                    prescription_data[category][field] = match.group(1).strip()

        return prescription_data


def text_to_speech(request):
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
