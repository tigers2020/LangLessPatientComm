import pandas as pd
from django.core.management.base import BaseCommand
from doctors.models import Doctor, Specialty

class Command(BaseCommand):
    help = 'Update primary_specialty for Doctor model using DAC.csv data'

    def handle(self, *args, **kwargs):
        # Adjust the file path to the correct location
        file_path = 'C:/Users/hyper/PycharmProjects/LangLessPatientComm/theme/static/data/DAC.csv'
        data = pd.read_csv(file_path)

        # Track updates
        updated_doctors = 0
        missing_specialties = set()

        for index, row in data.iterrows():
            try:
                doctors = Doctor.objects.filter(npi=row['NPI'])
                specialty_name = row['pri_spec']

                if specialty_name:
                    try:
                        specialty = Specialty.objects.get(name=specialty_name)
                        for doctor in doctors:
                            doctor.primary_specialty = specialty
                            doctor.save()
                            updated_doctors += 1
                    except Specialty.DoesNotExist:
                        missing_specialties.add(specialty_name)
                        self.stdout.write(self.style.WARNING(f"Specialty '{specialty_name}' not found for Doctor NPI: {row['NPI']}"))

            except Doctor.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Doctor with NPI '{row['NPI']}' not found"))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated primary_specialty for {updated_doctors} Doctor records'))
        if missing_specialties:
            self.stdout.write(self.style.WARNING(f'Missing specialties: {", ".join(missing_specialties)}'))
