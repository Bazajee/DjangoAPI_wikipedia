
from django.contrib import admin
from django.urls import path
from wiki_stats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/wikipedia/<str:title>', views.wikipedia_based),
     
]
