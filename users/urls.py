from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list, user_list, delete_participant, delete_group, organizer_dashboard, participant_dashboard, rsvp, ProfileView, PasswordChange, PasswordChangeDone, PasswordReset, PasswordResetConfirm, EditProfileView



urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'), 
    path('sign_in/', sign_in, name='sign_in'), 
    path('sign_out/', sign_out, name='sign_out'), 
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"), 
    path('organizer_dashboard/', organizer_dashboard, name="organizer_dashboard"), 
    path('participant_dashboard/', participant_dashboard, name="participant_dashboard"), 
    path('admin/<int:user_id>/assign_role', assign_role, name="assign_role"), 
    path('create_group/', create_group, name="create_group"), 
    path('delete_group/<int:id>/', delete_group, name="delete_group"),
    path('delete_participant/<int:user_id>/', delete_participant, name="delete_participant"),
    path('group_list/', group_list, name="group_list"), 
    path('user_list/', user_list, name="user_list"), 
    path('rsvp/<int:event_id>/', rsvp, name='rsvp'), 
    path('profile/', ProfileView.as_view(), name = 'profile'), 
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'), 
    path('password_reset/', PasswordReset.as_view(), name='password_reset'), 
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name = 'password_reset_confirm'), 
    path('edit_profile/', EditProfileView.as_view(), name = 'edit_profile')
    
]
