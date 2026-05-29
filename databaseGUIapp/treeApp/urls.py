from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("last-readings/", views.last_readings, name="last_readings"),
    path("reading-date-limits/", views.reading_date_limits, name="reading_date_limits"),
    path("download-readings-csv/", views.download_readings_csv, name="download_readings_csv"),
    path("station-readings/", views.station_readings, name="station_readings"),
    path("download-station-csv/", views.download_station_csv, name="download_station_csv"),
    path("station-date-limits/", views.station_date_limits, name="station_date_limits"),
]