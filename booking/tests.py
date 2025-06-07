from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import FitnessClass, Booking
from django.urls import reverse

class BookingTestCase(TestCase):
    def setUp(self):
        self.cls = FitnessClass.objects.create(
            name="Test Class",
            datetime="2025-06-10T10:00:00+05:30",
            instructor="Test Instructor",
            total_slots=5,
            available_slots=5
        )

    def test_class_list(self):
        response = self.client.get("/classes/")
        self.assertEqual(response.status_code, 200)

    def test_booking_success(self):
        response = self.client.post("/book/", {
            "class_id": self.cls.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_booking_full(self):
        self.cls.available_slots = 0
        self.cls.save()
        response = self.client.post("/book/", {
            "class_id": self.cls.id,
            "client_name": "Jane Doe",
            "client_email": "jane@example.com"
        })
        self.assertEqual(response.status_code, 400)
