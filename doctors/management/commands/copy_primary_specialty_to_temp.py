import logging
from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    help = 'Copy primary_specialty data to temp_primary_specialty field'

    def handle(self, *args, **kwargs):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Get all doctors
        doctors = Doctor.objects.all()

        # Track updates
        updated_doctors = 0

        # Copy primary_specialty to temp_primary_specialty
        for doctor in doctors:
            doctor.temp_primary_specialty = doctor.primary_specialty
            doctor.save()
            updated_doctors += 1

        # Log results
        logger.info(f'Copied primary_specialty data for {updated_doctors} Doctor records to temp_primary_specialty field')
        self.stdout.write(self.style.SUCCESS(f'Successfully copied primary_specialty data for {updated_doctors} Doctor records to temp_primary_specialty field'))
