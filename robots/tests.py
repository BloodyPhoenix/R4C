import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from robots.models import Robot
from robots.views import DownloadWeeklyReportView
from openpyxl import Workbook


class TestAPIPost(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@testadmin.com', 'testcase')

    def setUp(self):
        self. user = User.objects.get(username='admin')

    def test_api_correct_url(self):
        request = self.client.get('/robots_api/create_robot/')
        self.assertEqual(request.status_code, 200)

    def test_correct_data(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {"model":"R2","version":"D2","created":"2022-12-31 23:59:59"}
        response = client.post('/robots_api/create_robot/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        assert Robot.objects.get(model='R2')

    def test_incorrect_data(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {"model": "R2", "version": "D2"}
        response = client.post('/robots_api/create_robot/', data=data, format='json')
        self.assertEqual(response.status_code, 400)
        try:
            Robot.objects.get(model='R2')
        except ObjectDoesNotExist:
            assert True


class TestWeeklyReport(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Что мы ожидаем с этим набором тестовых данных:
        # В отчёте 2 робота R2-D2, один R2-C3 и один C3-D2, R2-C5 не попадает вообще
        time_data = [
            datetime.datetime.now(),
            datetime.datetime.now(),
            datetime.datetime.now() - datetime.timedelta(days=8),
            datetime.datetime.now() - datetime.timedelta(days=8),
            datetime.datetime.now() - datetime.timedelta(days=7) - datetime.timedelta(hours=1),
            datetime.datetime.now()
        ]
        Robot.objects.create(serial='R2-D2', model='R2', version='D2', created=time_data[0])
        Robot.objects.create(serial='R2-C3', model='R2', version='C3', created=time_data[1]),
        Robot.objects.create(serial='R2-C5', model='R2', version='C5', created=time_data[2]),
        Robot.objects.create(serial='R2-D2', model='R2', version='D2', created=time_data[3])
        Robot.objects.create(serial='R2-D2', model='R2', version='D2', created=time_data[4])
        Robot.objects.create(serial='C3-D2', model='C3', version='D2', created=time_data[5])

    def test_correct_queryset(self):
        robot_1 = Robot.objects.get(serial='R2-C5')
        robot_2 = Robot.objects.get(serial='C3-D2')
        queryset = DownloadWeeklyReportView.get_last_week_production()
        self.assertNotIn(robot_1, queryset)
        self.assertIn(robot_2, queryset)

    def test_correct_data_format(self):
        queryset = DownloadWeeklyReportView.get_last_week_production()
        formatted_data = DownloadWeeklyReportView.format_queryset_data(queryset)
        self.assertEqual(formatted_data['R2']['D2'], 2)
        self.assertEqual(formatted_data['R2']['C3'], 1)
        self.assertEqual(formatted_data['C3']['D2'], 1)

    def test_file_created(self):
        queryset = DownloadWeeklyReportView.get_last_week_production()
        formatted_data = DownloadWeeklyReportView.format_queryset_data(queryset)
        file = DownloadWeeklyReportView.get_excel_file(formatted_data)
        self.assertEqual(type(file), Workbook)
        file.active = file['R2']
        sheet_r2 = file.active
        self.assertEqual(sheet_r2['a2'].value, 'R2')
        self.assertEqual(sheet_r2['b2'].value, 'D2')
        self.assertEqual(sheet_r2['c2'].value, 2)
        file.active = file['C3']
        sheet_c3 = file.active
        self.assertEqual(sheet_c3['a2'].value, 'C3')
        self.assertEqual(sheet_c3['b2'].value, 'D2')
        self.assertEqual(sheet_c3['c2'].value, 1)

    def test_file_created_no_data(self):
        data = dict()
        file = DownloadWeeklyReportView.get_excel_file(data)
        self.assertEqual(type(file), Workbook)
