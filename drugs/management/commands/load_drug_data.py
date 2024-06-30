import json
import logging
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from drugs.models import Drug, Submission, Product
from tqdm import tqdm
import sys
import os

CHUNK_SIZE = 1000  # Number of rows to process at a time

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return None

class Command(BaseCommand):
    help = 'Load drug data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='The path to the JSON file.'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Suppress all logging
        logging.getLogger().setLevel(logging.ERROR)

        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r') as file:
                data = json.load(file)

            results = data.get('results', [])
            total_rows = len(results)

            total_created_drugs = 0
            total_created_submissions = 0
            total_created_products = 0

            with tqdm(total=total_rows, desc="Processing drugs", unit="drug", ncols=100, file=sys.stdout) as progress_bar:
                for i in range(0, total_rows, CHUNK_SIZE):
                    chunk = results[i:i + CHUNK_SIZE]
                    batch_drugs = []
                    drug_mapping = {}

                    for drug_data in chunk:
                        try:
                            drug = Drug(
                                application_number=drug_data.get('application_number'),
                                sponsor_name=drug_data.get('sponsor_name', 'Unknown')
                            )
                            batch_drugs.append(drug)
                        except Exception as e:
                            self.stderr.write(f"Error processing drug: {e}")
                            continue

                    # Save drug instances
                    created_drugs = Drug.objects.bulk_create(batch_drugs)
                    total_created_drugs += len(created_drugs)

                    # Create a mapping from application_number to created drug instance
                    for drug in created_drugs:
                        drug_mapping[drug.application_number] = drug

                    batch_submissions = []
                    batch_products = []

                    for drug_data in chunk:
                        drug = drug_mapping.get(drug_data.get('application_number'))
                        if not drug:
                            continue

                        for submission_data in drug_data.get('submissions', []):
                            try:
                                submission = Submission(
                                    drug=drug,
                                    submission_type=submission_data.get('submission_type', 'Unknown'),
                                    submission_number=submission_data.get('submission_number', 'Unknown'),
                                    submission_status=submission_data.get('submission_status', 'Unknown'),
                                    submission_status_date=parse_date(submission_data.get('submission_status_date', '19000101')),
                                    submission_class_code=submission_data.get('submission_class_code', 'Unknown'),
                                    submission_class_code_description=submission_data.get('submission_class_code_description', 'Unknown')
                                )
                                batch_submissions.append(submission)
                            except Exception as e:
                                self.stderr.write(f"Error processing submission: {e}")
                                continue

                        for product_data in drug_data.get('products', []):
                            try:
                                product = Product(
                                    drug=drug,
                                    product_number=product_data.get('product_number', 'Unknown'),
                                    brand_name=product_data.get('brand_name', 'Unknown'),
                                    dosage_form=product_data.get('dosage_form', 'Unknown'),
                                    route=product_data.get('route', 'Unknown'),
                                    marketing_status=product_data.get('marketing_status', 'Unknown'),
                                    active_ingredients=product_data.get('active_ingredients', [])
                                )
                                batch_products.append(product)
                            except Exception as e:
                                self.stderr.write(f"Error processing product: {e}")
                                continue

                    created_submissions = self._bulk_create_submissions(batch_submissions)
                    total_created_submissions += created_submissions
                    created_products = self._bulk_create_products(batch_products)
                    total_created_products += created_products

                    progress_bar.update(len(chunk))

            self.stdout.write(self.style.SUCCESS(
                f"\nDrugs loaded successfully. Total drugs processed: {total_rows}, Total drugs created: {total_created_drugs}, "
                f"Total submissions created: {total_created_submissions}, Total products created: {total_created_products}"))

        except FileNotFoundError as e:
            self.stderr.write(self.style.ERROR(str(e)))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f"Missing expected key: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

    def _bulk_create_submissions(self, submissions):
        try:
            with transaction.atomic():
                created_submissions = Submission.objects.bulk_create(submissions)
            return len(created_submissions)
        except Exception as e:
            self.stderr.write(f"Error in bulk create (Submissions): {e}")
            return 0

    def _bulk_create_products(self, products):
        try:
            with transaction.atomic():
                created_products = Product.objects.bulk_create(products)
            return len(created_products)
        except Exception as e:
            self.stderr.write(f"Error in bulk create (Products): {e}")
            return 0
