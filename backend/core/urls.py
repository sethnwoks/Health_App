from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Make sure to import your parse_log view
# from api.views import parse_log 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth Routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App Routes
    path('', include('api.urls')),
    
    # If parse_log is not inside api.urls, keep it here:
    # path('parse-log', parse_log),
]
