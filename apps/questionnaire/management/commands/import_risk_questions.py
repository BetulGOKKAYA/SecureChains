import csv
from django.core.management.base import BaseCommand
from apps.risk_categories.models import Security_Risk_Category
from apps.questionnaire.models import Risk_Questions
from django.db import IntegrityError

# Modified code snippet to use the `suggestion` field for order preservation with padded zeros

class Command(BaseCommand):
    help = 'Import Risk Questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        # Expected fields in the Risk_Questions model
        expected_fields = [
            'text', 'risk_group', 'asset_type', 'question_type',
            'question_group', 'relative_vul_group', 'value_type',
            'question_number', 'root_risk', 'threat_type',
            'perceived_threat', 'description', 'control_nist', 'suggestion'
        ]

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for index, row in enumerate(reader, start=1):  # Use enumerate to get the order (row number)
                # Skip the row if the 'text' cell is empty
                if not row['text']:
                    continue

                # Remove any double quotes from the 'text' field
                row['text'] = row['text'].replace('"', '')

                # Set the order in the `suggestion` field with padding
                row['suggestion'] = str(index).zfill(4)  # Pad with zeros to ensure proper string-based ordering

                # Remove unexpected columns
                for key in list(row.keys()):
                    if key not in expected_fields:
                        del row[key]

                # Try to get the risk_group instance using the name from the CSV file
                risk_group = Security_Risk_Category.objects.filter(category__iexact=row['risk_group'].strip()).first()

                # If a matching risk_group is found, save the Risk_Questions instance
                if risk_group:
                    row['risk_group'] = risk_group

                    try:
                        risk_question = Risk_Questions(**row)
                        risk_question.save()
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Error saving question: {row['text']} - Error: {str(e)}"))
                        self.stdout.write(self.style.WARNING(f"Problematic row: {row}"))
                        continue
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped question due to missing risk group: {row['text']}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported Risk Questions in order using padded suggestion field'))

# Note: Incorporate these changes in your Django environment and run the command.
