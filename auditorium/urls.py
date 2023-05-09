from django.urls import path
from auditorium.views import AuditoriumView, FloorView, BlockView, AuditoriumTypeView, GroupView, InstructorView

urlpatterns = [
    path('read/', AuditoriumView.as_view({"get": "read"})),
    path('<int:auditorium_id>/read/schedule/', AuditoriumView.as_view({"get": "read_schedule"})),
    path('<int:auditorium_id>/request/', AuditoriumView.as_view({"post": "request"})),

    path('requests/', AuditoriumView.as_view({"get": "read_reqeust_for_user"})),
    path('request/approve/', AuditoriumView.as_view({"post": "approve"})),

    path('common/floors/read/', FloorView.as_view()),
    path('common/blocks/read/', BlockView.as_view()),
    path('common/auditorium_types/read/', AuditoriumTypeView.as_view()),
    path('common/groups/read/', GroupView.as_view()),
    path('common/instructors/read/', InstructorView.as_view()),
]
