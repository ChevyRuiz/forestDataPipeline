from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
import csv


def index(request):
    return render(request, "treeApp/index.html")


def last_readings(request):
    stationcode = request.GET.get("stationcode")
    sensornumber = request.GET.get("sensornumber")
    sensortype = request.GET.get("sensortype")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT measured_at, value, unit, fieldname
            FROM measurement
            WHERE stationcode = %s
              AND sensornumber = %s
              AND sensortype = %s
              AND measured_at >= NOW() - INTERVAL '1 month'
            ORDER BY measured_at ASC
            """,
            [stationcode, sensornumber, sensortype],
        )
        rows = cursor.fetchall()

    data = [
        {
            "measured_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "value": row[1],
            "unit": row[2],
            "fieldname": row[3],
        }
        for row in rows
    ]

    return JsonResponse({"readings": data})


def reading_date_limits(request):
    stationcode = request.GET.get("stationcode")
    sensornumber = request.GET.get("sensornumber")
    sensortype = request.GET.get("sensortype")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT MIN(measured_at), MAX(measured_at)
            FROM measurement
            WHERE stationcode = %s
              AND sensornumber = %s
              AND sensortype = %s
            """,
            [stationcode, sensornumber, sensortype],
        )
        row = cursor.fetchone()

    if row is None or row[0] is None or row[1] is None:
        return JsonResponse({"has_data": False})

    return JsonResponse({
        "has_data": True,
        "min_date": row[0].strftime("%Y-%m-%d"),
        "max_date": row[1].strftime("%Y-%m-%d"),
    })


def download_readings_csv(request):
    stationcode = request.GET.get("stationcode")
    sensornumber = request.GET.get("sensornumber")
    sensortype = request.GET.get("sensortype")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{stationcode}_{sensornumber}_{sensortype}_{start_date}_to_{end_date}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "measured_at",
        "value",
        "unit",
    ])

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                measured_at,
                value,
                unit
            FROM measurement
            WHERE stationcode = %s
              AND sensornumber = %s
              AND sensortype = %s
              AND measured_at::date >= %s
              AND measured_at::date <= %s
            ORDER BY measured_at ASC
            """,
            [stationcode, sensornumber, sensortype, start_date, end_date],
        )

        for row in cursor.fetchall():
            writer.writerow(row)

    return response

def station_readings(request):
    stationcode = request.GET.get("stationcode")
    sensortype = request.GET.get("sensortype")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT measured_at, sensornumber, value, unit
            FROM measurement
            WHERE stationcode = %s
              AND sensortype = %s
              AND measured_at >= NOW() - INTERVAL '1 month'
            ORDER BY measured_at ASC
            """,
            [stationcode, sensortype],
        )
        rows = cursor.fetchall()

    data = [
        {
            "measured_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "sensornumber": row[1],
            "value": row[2],
            "unit": row[3],
        }
        for row in rows
    ]

    return JsonResponse({"readings": data})

def download_station_csv(request):
    stationcode = request.GET.get("stationcode")
    sensortype = request.GET.get("sensortype")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{stationcode}_{sensortype}_{start_date}_to_{end_date}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["measured_at", "sensornumber", "value", "unit"])

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT measured_at, sensornumber, value, unit
            FROM measurement
            WHERE stationcode = %s
              AND sensortype = %s
              AND measured_at::date >= %s
              AND measured_at::date <= %s
            ORDER BY measured_at ASC
            """,
            [stationcode, sensortype, start_date, end_date],
        )

        for row in cursor.fetchall():
            writer.writerow(row)

    return response

def station_date_limits(request):
    stationcode = request.GET.get("stationcode")
    sensortype = request.GET.get("sensortype")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT MIN(measured_at), MAX(measured_at)
            FROM measurement
            WHERE stationcode = %s
              AND sensortype = %s
            """,
            [stationcode, sensortype],
        )
        row = cursor.fetchone()

    if row is None or row[0] is None or row[1] is None:
        return JsonResponse({"has_data": False})

    return JsonResponse({
        "has_data": True,
        "min_date": row[0].strftime("%Y-%m-%d"),
        "max_date": row[1].strftime("%Y-%m-%d"),
    })