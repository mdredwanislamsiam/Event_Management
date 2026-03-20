from django.urls import path 
from events.views import events, event_detail, create_event, delete_event, update_event, EventsView, CreateEventView, UpdateEventView, EventDetailView, DeleteEventView
urlpatterns = [
    path('events/', EventsView.as_view(), name= "events"), 
    path('event_detail/<int:id>', EventDetailView.as_view(), name="event_detail"), 
    path('create_event/', CreateEventView.as_view(), name = "create_event"), 
    path('update_event/<int:id>', UpdateEventView.as_view(), name= "update_event"), 
    path('delete_event/<int:id>', DeleteEventView.as_view(), name= "delete_event"),
]
