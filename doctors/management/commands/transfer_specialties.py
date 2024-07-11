import logging
from django.core.management.base import BaseCommand
from doctors.models import Doctor, Specialty


class Command(BaseCommand):
    help = 'Transfer primary_specialty data from Doctor to Specialty model'

    def handle(self, *args, **kwargs):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Get unique primary_specialties from Doctor model
        primary_specialties = Doctor.objects.values_list('primary_specialty', flat=True).distinct()

        # Track inserted specialties
        inserted_specialties = 0

        # Transfer primary_specialties to Specialty model
        for specialty_name in primary_specialties:
            if specialty_name:
                specialty, created = Specialty.objects.get_or_create(name=specialty_name)
                if created:
                    inserted_specialties += 1

        # Log results
        logger.info(f'Transferred {inserted_specialties} unique primary_specialty names to Specialty model')
        self.stdout.write(self.style.SUCCESS(
            f'Successfully transferred {inserted_specialties} unique primary_specialty names to Specialty model'))
