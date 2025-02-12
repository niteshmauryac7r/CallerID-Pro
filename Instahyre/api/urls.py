


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SpamViewSet, LoginView  # Import the LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'spam', SpamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),  # Add this for the login endpoint
]
