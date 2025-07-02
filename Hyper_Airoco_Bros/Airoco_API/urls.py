from django.urls import path
from .views import Carbon_judge, OneWeekRecordView

urlpatterns = [
    path('carbon-judge/', Carbon_judge.as_view(), name='carbon-judge'),
    path('one-week-record/', OneWeekRecordView.as_view(), name='one-week-record'),
]