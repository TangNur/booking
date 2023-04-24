from django.urls import path, include

urlpatterns = [
    path('auditorium/', include('auditorium.urls')),
]
