from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import CreateRobotAPI
from.views import DownloadWeeklyReportView

urlpatterns = [
    path('get_weekly_report', DownloadWeeklyReportView.as_view(), name='weekly_report')
]

router = DefaultRouter()
router.register(r'create_robot', CreateRobotAPI, basename='create_robot')
urlpatterns += router.urls