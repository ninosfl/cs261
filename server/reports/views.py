from django.shortcuts import render
from django.http import HttpResponse
from calendar import Calendar
import datetime

def years(request):
    now = datetime.datetime.now()
    start_year = 2000
    placeholder_years = [y for y in range(now.year, start_year - 1, -1)]
    context = { "list": placeholder_years }
    return render(request, "reports/years.html", context)

def months(request, year: int):
    # Check for year validity
    now = datetime.datetime.now()
    if year > now.year:
        error_message = f"The year {year} is in the future. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    elif year < 1970:
        error_message = f"The year {year} is too far in the past. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    else:

        # Get valid lists of months (as integers)
        if year == now.year:
            months = [m for m in range(1, min(12, now.month) + 1)]
        else:
            months = [m for m in range(1, 12 + 1)]

        context = {
            "list": months,
            "year": year
        }
        return render(request, "reports/months.html", context)

def days(request, year: int, month: int):
    # Check for year validity
    now = datetime.datetime.now()
    if year > now.year:
        error_message = f"The year {year} is in the future. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    elif year < 1970:
        error_message = f"The year {year} is too far in the past. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    else:

        # Check for month validity
        if month < 1 or month > 12:
            error_message = f"Month values are from 1 to 12. The given month, {month}, is invalid."
            context = { "error_message": error_message }
            return render(request, "errors/errorpage.html", context)
        elif year == now.year and month > now.month:
            error_message = f"The month {month} is in the future. There are no trades listed."
            context = { "error_message": error_message }
            return render(request, "errors/errorpage.html", context)
        else:

            # Get list of valid days for that month
            c = Calendar()
            if year == now.year and month == now.month:
                days = [d for d in c.itermonthdays(year, month) if d != 0 and d <= now.day]
            else:
                days = [d for d in c.itermonthdays(year, month) if d != 0]
            
            context = {
                "list": days,
                "year": year,
                "month": month
            }
            return render(request, "reports/days.html", context)

def report(request, year: int, month: int, day: int):
    # Check for year validity
    now = datetime.datetime.now()
    if year > now.year:
        error_message = f"The year {year} is in the future. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    elif year < 1970:
        error_message = f"The year {year} is too far in the past. There are no trades listed."
        context = { "error_message": error_message }
        return render(request, "errors/errorpage.html", context)
    else:

        # Check for month validity
        if month < 1 or month > 12:
            error_message = f"Month values are from 1 to 12. The given month, {month}, is invalid."
            context = { "error_message": error_message }
            return render(request, "errors/errorpage.html", context)
        elif year == now.year and month > now.month:
            error_message = f"The month {month} is in the future. There are no trades listed."
            context = { "error_message": error_message }
            return render(request, "errors/errorpage.html", context)
        else:

            # Get list of valid days for the month, making sure they don't go
            # into the future.
            c = Calendar()
            if year == now.year and month == now.month:
                days = [d for d in c.itermonthdays(year, month)
                        if d != 0 and d <= now.day]
            else:
                days = [d for d in c.itermonthdays(year, month) if d != 0]

            if day not in days:
                error_message = f"There are no trades listed for {day}/{month}/{year}."
                context = { "error_message": error_message }
                return render(request, "errors/errorpage.html", context)
            else:

                context = {
                    "year": year,
                    "month": month,
                    "day": day
                }
                return render(request, "reports/report.html", context)
