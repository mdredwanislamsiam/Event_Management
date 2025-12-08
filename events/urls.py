from django.urls import path 
from events.views import events, event_detail, create_event, delete_event, update_event
urlpatterns = [
    path('events/', events, name= "events"), 
    path('event_detail/', event_detail, name="event_detail"), 
    path('create_event/', create_event, name = "create_event"), 
    path('update_event/<int:id>', update_event, name= "update_event"), 
    path('delete_event/<int:id>', delete_event, name= "delete_event")
]
