import csv
from django.core.management.base import BaseCommand
from apps.risk_categories.models import Security_Risk_Category
from apps.questionnaire.models import Risk_Questions


class Command(BaseCommand):
    help = 'Import Risk Questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Get the risk_group instance using the name from the CSV file
                risk_group = Security_Risk_Category.objects.get(category=row['risk_group'])

                # Replace the risk_group value in the row with the actual risk_group instance
                row['risk_group'] = risk_group

                # Convert the row to a dictionary and pass it as keyword arguments to create a Risk_Questions instance
                risk_question = Risk_Questions(**row)
                risk_question.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported Risk Questions'))
