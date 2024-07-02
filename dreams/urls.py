from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SignUpView, LoginView

router = DefaultRouter()
router.register(r'dreams', views.DreamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add any additional custom routes here
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
