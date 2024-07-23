from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views
from .views import SignUpView, LoginView

router = DefaultRouter()
router.register(r'dreams', views.DreamViewSet)
router.register(r'emotions', views.EmotionViewSet)
router.register(r'themes', views.ThemeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add any additional custom routes here
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('suggest-themes/', views.suggest_themes, name='suggest-themes'),
    path('suggest-emotions/', views.suggest_emotions, name='suggest_emotions'),
    path('suggest-title/', views.suggest_title, name='suggest_dreams'),
    path('generate-dream-insight/', views.generate_dream_insight, name='dream_insights'),

    # Simple JWT token URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('dreams/<int:dream_id>/check-insight/', views.check_dream_insight, name='check_dream_insight'),
]
