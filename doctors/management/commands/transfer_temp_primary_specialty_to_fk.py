import logging
from django.core.management.base import BaseCommand
from your_app.models import Doctor, Specialty

class Command(BaseCommand):
    help = 'Transfer temp_primary_specialty data to primary_specialty ForeignKey field'

    def handle(self, *args, **kwargs):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Get all doctors
        doctors = Doctor.objects.all()

        # Track updates
        updated_doctors = 0

        # Transfer temp_primary_specialty to primary_specialty
        for doctor in doctors:
            if doctor.temp_primary_specialty:
                try:
                    specialty = Specialty.objects.get(name=doctor.temp_primary_specialty)
                    doctor.primary_specialty = specialty
                    doctor.save()
                    updated_doctors += 1
                except Specialty.DoesNotExist:
                    logger.warning(f'Specialty {doctor.temp_primary_specialty} does not exist for Doctor {doctor.id}')

        # Log results
        logger.info(f'Updated {updated_doctors} Doctor records with Specialty references')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_doctors} Doctor records with Specialty references'))
