import logging

from django.core.management.base import BaseCommand

from doctors.models import Doctor, Specialty


class Command(BaseCommand):
    help = 'Transfer primary_specialty data to primary_specialty_v2 ForeignKey field'

    def handle(self, *args, **kwargs):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Get all doctors
        doctors = Doctor.objects.all()

        # Track updates
        updated_doctors = 0

        # Transfer primary_specialty to primary_specialty_v2
        for doctor in doctors:
            if doctor.primary_specialty:
                try:
                    specialty = Specialty.objects.get(name=doctor.primary_specialty)
                    doctor.primary_specialty_v2 = specialty
                    doctor.save()
                    updated_doctors += 1
                except Specialty.DoesNotExist:
                    logger.warning(f'Specialty {doctor.primary_specialty} does not exist for Doctor {doctor.id}')

        # Log results
        logger.info(f'Updated {updated_doctors} Doctor records with primary_specialty_v2 references')
        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {updated_doctors} Doctor records with primary_specialty_v2 references'))
