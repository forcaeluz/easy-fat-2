from django.conf.urls import url

from .views import BuildingsIndexView, NewBuildingView, NewRoomGroupView, NewRoomView


app_name = 'buildings'
urlpatterns = [
    url(r'^index$', BuildingsIndexView.as_view(), name='index'),
    url(r'^new_building$', NewBuildingView.as_view(), name='new_building'),
    url(r'^new_room_group$', NewRoomGroupView.as_view(), name='new_room_group'),
    url(r'^new_room$', NewRoomView.as_view(), name='new_room'),
]
