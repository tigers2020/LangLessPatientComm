import json
import logging
import os
import sys
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import make_aware
from tqdm import tqdm

from products.models import Root, MetaInfo, OpenFDA, Results

CHUNK_SIZE = 1000  # Number of rows to process at a time


class Command(BaseCommand):
    help = 'Load drug label data from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            'directory_path',
            type=str,
            help='The path to the directory containing the JSON files.'
        )
        parser.add_argument(
            '--resume_from',
            type=str,
            help='Resume processing from this file',
            default=None
        )

    def handle(self, *args, **options):
        directory_path = options['directory_path']
        resume_from = options['resume_from']

        # Suppress all logging
        logging.getLogger().setLevel(logging.ERROR)

        try:
            # List all JSON files in the directory
            json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

            if resume_from:
                try:
                    start_index = json_files.index(resume_from)
                    json_files = json_files[start_index:]
                except ValueError:
                    self.stderr.write(f"Resuming file {resume_from} not found. Starting from beginning.")

            total_files = len(json_files)
            total_created = 0

            with tqdm(total=total_files, desc="Processing files", unit="file", ncols=100,
                      file=sys.stdout) as file_progress:
                for json_file in json_files:
                    file_path = os.path.join(directory_path, json_file)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        if 'results' not in data:
                            self.stderr.write(f"No 'results' key found in {json_file}")
                            continue

                        batch = []
                        total_rows = len(data['results'])

                        with tqdm(total=total_rows, desc=f"Processing {json_file}", unit="row", ncols=100,
                                  file=sys.stdout) as row_progress:
                            for result in data['results']:
                                try:
                                    root_instance = self._create_root_instance(result)
                                    batch.append(root_instance)
                                except Exception as e:
                                    self.stderr.write(f"Error processing row in {json_file}: {str(e)}")
                                    continue

                                if len(batch) >= CHUNK_SIZE:
                                    created_count = self._bulk_create_roots(batch)
                                    total_created += created_count
                                    batch.clear()
                                    row_progress.set_postfix({"Created": total_created}, refresh=False)

                                row_progress.update(1)

                            if batch:
                                created_count = self._bulk_create_roots(batch)
                                total_created += created_count
                                row_progress.set_postfix({"Created": total_created}, refresh=False)

                    file_progress.update(1)

            self.stdout.write(self.style.SUCCESS(
                f"\nDrug labels loaded successfully. Total files processed: {total_files}, Total created: {total_created}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Directory not found: {directory_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

    def _create_root_instance(self, data):
        meta_data = data.get('meta', {})
        meta_instance = MetaInfo(
            disclaimer=meta_data.get('disclaimer', ''),
            last_updated=self._parse_datetime(meta_data.get('last_updated')),
            license=meta_data.get('license', ''),
            results_limit=meta_data.get('results', {}).get('limit'),
            results_skip=meta_data.get('results', {}).get('skip'),
            results_total=meta_data.get('results', {}).get('total'),
            terms=meta_data.get('terms', '')
        )

        openfda_data = data.get('openfda', {})
        openfda_instance = OpenFDA(
            application_number=openfda_data.get('application_number', []),
            brand_name=openfda_data.get('brand_name', []),
            generic_name=openfda_data.get('generic_name', []),
            manufacturer_name=openfda_data.get('manufacturer_name', []),
            product_ndc=openfda_data.get('product_ndc', []),
            product_type=openfda_data.get('product_type', []),
            route=openfda_data.get('route', []),
            substance_name=openfda_data.get('substance_name', []),
            rxcui=openfda_data.get('rxcui', []),
            spl_id=openfda_data.get('spl_id', []),
            spl_set_id=openfda_data.get('spl_set_id', []),
            package_ndc=openfda_data.get('package_ndc', []),
            nui=openfda_data.get('nui', []),
            pharm_class_epc=openfda_data.get('pharm_class_epc', []),
            pharm_class_cs=openfda_data.get('pharm_class_cs', []),
            pharm_class_pe=openfda_data.get('pharm_class_pe', []),
            pharm_class_moa=openfda_data.get('pharm_class_moa', []),
            upc=openfda_data.get('upc', []),
            unii=openfda_data.get('unii', []),
            # Handle boolean fields carefully
            is_original_packager=self._parse_boolean(openfda_data.get('is_original_packager')),
        )

        results_data = data.get('results', {})
        results_instance = Results(
            effective_time=self._parse_datetime(results_data.get('effective_time')),
            # Add other fields here...
        )

        root_instance = Root(
            meta=meta_instance,
            openfda=openfda_instance,
            results=results_instance
        )

        return root_instance

    def _bulk_create_roots(self, roots):
        try:
            with transaction.atomic():
                created_roots = Root.objects.bulk_create(roots)
            return len(created_roots)
        except Exception as e:
            self.stderr.write(f"Error in bulk create: {e}")
            return 0

    def _parse_datetime(self, dt_string):
        if not dt_string:
            return None
        try:
            naive_dt = datetime.strptime(dt_string, "%Y-%m-%d")
            return make_aware(naive_dt)
        except ValueError:
            return None

    def _parse_boolean(self, value):
        if isinstance(value, list):
            # If it's a list, take the first value
            value = value[0] if value else None
        if isinstance(value, str):
            return value.lower() == 'true'
        return bool(value) if value is not None else None
