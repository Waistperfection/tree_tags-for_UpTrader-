from django.urls import path
from django.views.generic import TemplateView

from .views import index

urlpatterns = [
    path('', TemplateView.as_view(template_name='menu/index.html')),
    path('<path:path>', index, name='menu'),
]