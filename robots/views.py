import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from django.views import View
from .models import Robot


class DownloadWeeklyReportView(View):

    @staticmethod
    def get_last_week_production():
        # Немного шаманства, чтобы считались все данные за день неделю назад, а не только те, что были получены
        # строго за последние 168 часов
        # Не знаю, нужно ли исключать текущий день. В этой версии кода он не исключается из выдачи
        today_date = datetime.date.today()
        time = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
        today_full_date = datetime.datetime.combine(today_date, time)
        week_ago = today_full_date - datetime.timedelta(days=7)
        queryset = Robot.objects.filter(created__gte=week_ago)
        return queryset

    @staticmethod
    def format_queryset_data(queryset):
        # Сортируем и преобразовываем данные по произведённым роботам для дальнейшей записи в файл
        formatted_data = dict()
        for robot in queryset:
            model = robot.model
            version = robot.version
            if model in formatted_data:
                if version in formatted_data[model]:
                    formatted_data[model][version] += 1
                else:
                    formatted_data[model][version] = 1
            else:
                formatted_data[model] = {version: 1}
        return formatted_data

