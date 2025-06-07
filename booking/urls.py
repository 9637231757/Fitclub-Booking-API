from django.urls import path
from .views import FitnessClassList, BookingView, BookingList

urlpatterns = [
    path('classes/', FitnessClassList.as_view()),
    path('book/', BookingView.as_view()),
    path('bookings/', BookingList.as_view()),
]
