from django.urls import path

from auditorium.views import AuditoriumView, FloorView, BlockView, AuditoriumTypeView


urlpatterns = [
    path('read/', AuditoriumView.as_view({"get": "read"})),
    path('<int:auditorium_id>/read/schedule/', AuditoriumView.as_view({"get": "read_schedule"})),
    path('common/floors/read/', FloorView.as_view()),
    path('common/blocks/read/', BlockView.as_view()),
    path('common/auditorium_types/read/', AuditoriumTypeView.as_view()),
]
