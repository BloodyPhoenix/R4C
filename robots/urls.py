from rest_framework.routers import DefaultRouter
from .api import CreateRobotAPI

router = DefaultRouter()
router.register(r'create_robot', CreateRobotAPI, basename='create_robot')
urlpatterns = router.urls