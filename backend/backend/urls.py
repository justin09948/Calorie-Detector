from django.contrib import admin
from django.urls import path
from api.views import PredictCalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('process-image/', PredictCalView.as_view(), name='process_image')
]
