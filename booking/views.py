from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import localtime
from pytz import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer, BookingRequestSerializer

class FitnessClassList(APIView):
    def get(self, request):
        tz = request.GET.get("tz", "Asia/Kolkata")
        classes = FitnessClass.objects.all()
        for cls in classes:
            cls.datetime = cls.datetime.astimezone(timezone(tz))
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)

class BookingView(APIView):
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        class_id = serializer.validated_data["class_id"]
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

        if fitness_class.available_slots <= 0:
            return Response({"error": "No available slots"}, status=400)

        # Booking
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=serializer.validated_data["client_name"],
            client_email=serializer.validated_data["client_email"]
        )
        fitness_class.available_slots -= 1
        fitness_class.save()
        return Response(BookingSerializer(booking).data, status=201)

class BookingList(APIView):
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return Response({"error": "Email parameter required"}, status=400)

        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
