from django.urls import path
from auditorium.views import AuditoriumView, FloorView, BlockView, AuditoriumTypeView, GroupView, InstructorView, \
    BookingRequestStatusView, RequestStatusConfigView

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
    path('common/booking_request_statuses/read/', BookingRequestStatusView.as_view()),

    path('common/request_status_configs/read/', RequestStatusConfigView.as_view({"get": "read_all"})),
    path('common/request_status_configs/change/', RequestStatusConfigView.as_view({"post": "change"})),
]
