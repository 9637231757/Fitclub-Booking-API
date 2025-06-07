from django.core.management.base import BaseCommand
from booking.models import FitnessClass
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tz = pytz.timezone('Asia/Kolkata')
        FitnessClass.objects.all().delete()
        classes = [
            ("Yoga", 1),
            ("Zumba", 2),
            ("HIIT", 3),
        ]
        for i, (name, day) in enumerate(classes):
            FitnessClass.objects.create(
                name=name,
                datetime=tz.localize(datetime.now() + timedelta(days=day)),
                instructor=f"Instructor {i+1}",
                total_slots=10,
                available_slots=10
            )
        self.stdout.write("Seed data loaded.")
