from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import *

urlpatterns = [
    path('api/v1/signup/', SignUpView.as_view(), name='signup'),
    path('api/v1/signin/', SigninView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/v1/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/v1/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/v1/financial-datas/', CreateFinancialData.as_view(), name='financial-data'),
    path('api/v1/financial-data/<int:pk>/', FinanceData.as_view(), name='update-financial-data'),
    path('api/v1/test/', TestView.as_view(), name='update-financial-data'),
]
