from django.urls import path

from .views import GetTokenAPIView, RegistrationAPIView

namespace = 'users'

urlpatterns = [
    path(
        'signup/', RegistrationAPIView.as_view(), name='signup'
    ),
    path(
        'token/', GetTokenAPIView.as_view(), name='get_token'
    )
]
