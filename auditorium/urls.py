from django.urls import path

from auditorium.views import AuditoriumView

urlpatterns = [
    path('read/', AuditoriumView.as_view({"get": "read"})),
    path('<int:auditorium_id>/read/schedule/', AuditoriumView.as_view({"get": "read_schedule"})),
]
