import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from doctors.models import Doctor
from tqdm import tqdm
import sys

CHUNK_SIZE = 1000  # Number of rows to process at a time


class Command(BaseCommand):
    help = 'Load doctors data from DAC.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='The path to the CSV file.'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Suppress all logging
        logging.getLogger().setLevel(logging.ERROR)

        try:
            # Count total rows for progress bar
            total_rows = sum(1 for _ in open(file_path, encoding='utf-8')) - 1  # Subtract 1 for header

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Validate CSV file headers
                required_headers = {'NPI', 'Ind_PAC_ID', 'Ind_enrl_ID', 'Provider Last Name', 'Provider First Name',
                                    'Provider Middle Name', 'suff', 'gndr', 'Cred', 'Med_sch', 'Grd_yr', 'pri_spec',
                                    'sec_spec_all', 'Telehlth', 'Facility Name', 'org_pac_id', 'num_org_mem',
                                    'adr_ln_1',
                                    'adr_ln_2', 'City/Town', 'State', 'ZIP Code', 'Telephone Number', 'ind_assgn',
                                    'grp_assgn', 'adrs_id'}
                if not required_headers.issubset(reader.fieldnames):
                    raise KeyError(f"Missing expected columns: {required_headers - set(reader.fieldnames)}")

                batch = []
                total_created = 0

                with tqdm(total=total_rows, desc="Processing rows", unit="row", ncols=100,
                          file=sys.stdout) as progress_bar:
                    for row in reader:
                        try:
                            doctor = Doctor(
                                npi=row['NPI'][:10],
                                ind_pac_id=row.get('Ind_PAC_ID', '')[:20],
                                ind_enrl_id=row.get('Ind_enrl_ID', '')[:20],
                                provider_last_name=row.get('Provider Last Name', '')[:50],
                                provider_first_name=row.get('Provider First Name', '')[:50],
                                provider_middle_name=row.get('Provider Middle Name', '')[:50],
                                suffix=row.get('suff', '')[:10],
                                gender=row.get('gndr', '')[:1],
                                credential=row.get('Cred', '')[:20],
                                med_school=row.get('Med_sch', '')[:100],
                                grad_year=row.get('Grd_yr', '')[:4],
                                primary_specialty=row.get('pri_spec', '')[:100],
                                secondary_specialty=row.get('sec_spec_all', '')[:100],
                                telehealth=row.get('Telehlth', '')[:3],
                                facility_name=row.get('Facility Name', '')[:100],
                                org_pac_id=row.get('org_pac_id', '')[:20],
                                num_org_members=row.get('num_org_mem', '')[:5],
                                address_line_1=row.get('adr_ln_1', '')[:100],
                                address_line_2=row.get('adr_ln_2', '')[:100],
                                city=row.get('City/Town', '')[:50],
                                state=row.get('State', '')[:2],
                                zip_code=row.get('ZIP Code', '')[:10],
                                telephone_number=row.get('Telephone Number', '')[:15],
                                individual_assignment=row.get('ind_assgn', '')[:1],
                                group_assignment=row.get('grp_assgn', '')[:1],
                                address_id=row.get('adrs_id', '')[:20],
                            )
                            batch.append(doctor)
                        except Exception as e:
                            self.stderr.write(f"Error processing row: {e}")
                            continue

                        if len(batch) >= CHUNK_SIZE:
                            created_count = self._bulk_create_doctors(batch)
                            total_created += created_count
                            batch.clear()
                            progress_bar.set_postfix({"Created": total_created}, refresh=False)

                        progress_bar.update(1)

                    if batch:
                        created_count = self._bulk_create_doctors(batch)
                        total_created += created_count
                        progress_bar.set_postfix({"Created": total_created}, refresh=False)

            self.stdout.write(self.style.SUCCESS(
                f"\nDoctors loaded successfully. Total rows processed: {total_rows}, Total created: {total_created}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f"Missing expected column: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

    def _bulk_create_doctors(self, doctors):
        try:
            with transaction.atomic():
                existing_npis = set(
                    Doctor.objects.filter(npi__in=[doctor.npi for doctor in doctors]).values_list('npi', flat=True))
                new_doctors = [doctor for doctor in doctors if doctor.npi not in existing_npis]
                created_doctors = Doctor.objects.bulk_create(new_doctors)

            return len(created_doctors)
        except Exception as e:
            self.stderr.write(f"Error in bulk create: {e}")
            return 0