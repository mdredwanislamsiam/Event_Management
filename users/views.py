from django.shortcuts import render, redirect
from users.forms import CustomSignUpForm, CustomSignInForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from events.models import Event
from django.db.models import Count, Q
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


User = get_user_model()



""" Supporting Functions """

def is_admin(user): 
    return user.groups.filter(name = 'Admin').exists()

def is_organizer(user): 
    return user.groups.filter(name = 'Organizer').exists()

def is_participant(user): 
    return user.groups.filter(name = 'Participant').exists()

def navbar_test(user): 
    user_group = user.groups.first()
    group_name = 'No Group'
    if user_group:
        group_name = user_group.name
        
    if group_name == "Admin":
        navbar = "admin/admin_navbar.html"
    elif group_name == "Organizer":
        navbar = "organizer/organizer_navbar.html"
    elif group_name == 'Participant':
        navbar = "participant/participant_navbar.html"
    else:
        navbar = "navbar.html"
    return navbar
    
    

""" Main Functions """

def sign_up(request): 
    form = CustomSignUpForm()
    if request.method == "POST": 
        form = CustomSignUpForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
        
            messages.success(request, "A confirmation mail has been sent to your mail!")
            return redirect('sign_in')
        
    return render(request, 'registration/sign_up.html', {'form':form})



def sign_in(request):
    form = CustomSignInForm()
    if request.method == "POST": 
        form = CustomSignInForm(data = request.POST)
        if form.is_valid(): 
            user = form.get_user()
            login(request, user)
            return redirect('home')
    
    return render(request, 'registration/sign_in.html', {'form': form})
            
 
 
@login_required
def sign_out(request): 
    if request.method =="POST": 
        logout(request)
        return redirect('sign_in')
    
    
    
def activate_user(request, user_id, token): 
    try: 
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user, token): 
            user.is_active = True
            user.save()
            return  redirect('sign_in')
        else: 
            return HttpResponse("Invalid ID or Token!")
    except User.DoesNotExist: 
        return HttpResponse("User not Found!")
    

@login_required
@user_passes_test(is_admin, login_url='no_permission')
def user_list(request): 
    users = User.objects.prefetch_related('groups')
    for user in users: 
        if user.groups.exists(): 
            user.group_name = user.groups.first().name
        else: 
            user.group_name = "No Group"
    return render(request, 'admin/user_list.html', {'users': users})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    type = request.GET.get('type', 'today')
    basequery = Event.objects.select_related(
        'category').prefetch_related('participant')

    if type == 'all':
        events = basequery.all().distinct()
        title = "All Events"
    elif type == 'upcoming':
        events = basequery.filter(date__gt=date.today()).distinct()
        title = "Upcoming Events"
    elif type == 'past':
        events = basequery.filter(date__lt=date.today()).distinct()
        title = "Past Events"
    elif type == 'today':
        events = basequery.filter(date=date.today()).distinct()
        title = "Today's Events"

    counts = Event.objects.aggregate(
        total_event=Count('id', distinct=True),
        total_participant=Count('participant', distinct=True),
        upcoming_events=Count('id', filter=Q(
            date__gt=date.today()), distinct=True),
        past_events=Count('id', filter=Q(
            date__lt=date.today()), distinct=True),
        todays_events=Count('id', filter=Q(date=date.today()), distinct=True)
    )
    context = {
        'counts': counts,
        'events': events,
        'title': title
    }
    return render(request, 'admin/admin_dashboard.html', context)



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, user_id): 
    user = User.objects.get(id =user_id)
    form = AssignRoleForm()
    if request.method == "POST": 
        form = AssignRoleForm(request.POST)
        if form.is_valid(): 
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin_dashboard')
        
    return render(request, 'admin/assign_role.html', {'form': form})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def create_group(request): 
    form = CreateGroupForm()
    if request.method =="POST": 
        form = CreateGroupForm(request.POST)
        if form.is_valid(): 
            group = form.save()
            messages.success(
            request, f"Group {group.name} has been Created successfully")
            return redirect('create_group')
    return render(request, 'admin/create_group.html', {'form': form})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def group_list(request): 
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {'groups': groups})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def delete_participant(request, user_id): 
    if request.method == 'POST': 
        participant = User.objects.get(id = user_id)
        participant.delete()
        messages.success(request, 'Participant Deleted Successfully')
        return redirect('user_list')



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def delete_group(request, id): 
    if request.method == "POST": 
        group = Group.objects.get(id = id)
        group.delete()
        messages.success(request, 'Group Deleted Successfully')
        return redirect('group_list')
        
    
    
@login_required
@user_passes_test(is_organizer, login_url='no_permission')   
def organizer_dashboard(request): 
    type = request.GET.get('type', 'today')
    basequery = Event.objects.select_related(
        'category').prefetch_related('participant')

    if type == 'all':
        events = basequery.all().distinct()
        title = "All Events"
    elif type == 'upcoming':
        events = basequery.filter(date__gt=date.today()).distinct()
        title = "Upcoming Events"
    elif type == 'past':
        events = basequery.filter(date__lt=date.today()).distinct()
        title = "Past Events"
    elif type == 'today':
        events = basequery.filter(date=date.today()).distinct()
        title = "Today's Events"

    counts = Event.objects.aggregate(
        total_event=Count('id', distinct=True),
        total_participant=Count('participant', distinct=True),
        upcoming_events=Count('id', filter=Q(
            date__gt=date.today()), distinct=True),
        past_events=Count('id', filter=Q(
            date__lt=date.today()), distinct=True),
        todays_events=Count('id', filter=Q(date=date.today()), distinct=True)
    )
    context = {
        'counts': counts,
        'events': events,
        'title': title
    }
    return render(request, 'organizer/organizer_dashboard.html', context)



@login_required
@user_passes_test(is_participant, login_url='no_permission')
def participant_dashboard(request):
    type = request.GET.get('type', 'today')
    basequery = Event.objects.select_related(
        'category').prefetch_related('participant').filter(participant = request.user)

    if type == 'all':
        events = basequery.all().distinct()
        title = "All Events"
    elif type == 'upcoming':
        events = basequery.filter(date__gt=date.today()).distinct()
        title = "Upcoming Events"
    elif type == 'past':
        events = basequery.filter(date__lt=date.today()).distinct()
        title = "Past Events"
    elif type == 'today':
        events = basequery.filter(date=date.today()).distinct()
        title = "Today's Events"

    counts = basequery.aggregate(
        total_event=Count('id', distinct=True),
        upcoming_events=Count('id', filter=Q(
            date__gt=date.today()), distinct=True),
        past_events=Count('id', filter=Q(
            date__lt=date.today()), distinct=True),
        todays_events=Count('id', filter=Q(date=date.today()), distinct=True)
    )
    context = {
        'counts': counts,
        'events': events,
        'title': title
    }
    return render(request, 'participant/participant_dashboard.html', context)


@login_required

@user_passes_test(is_participant, login_url='no_permission')
def rsvp(request, event_id): 
    if request.method == "POST": 
        event = Event.objects.get(id = event_id)
        if request.user in event.participant.all(): 
            messages.warning(request, f"You are already engaged in  [{event.name}] event")
        else: 
            participant = request.user
            event.participant.add(participant)
            event.save()
            messages.success(
                request, f"You have successfully engaged in the [{event.name}] event")
            
        return redirect('events')
        
    return redirect('events')



""" Class Based Views """

class ProfileView(LoginRequiredMixin, TemplateView): 
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        group = self.request.user.groups.first()
        group_name = "No Group"
        if group:
            group_name = group.name
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['profile_image'] = user.profile_image
        context['bio'] = user.bio
        context['phone_number'] = user.phone_number
        context['address'] = user.address
        context['designation'] = group_name
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['navbar'] = navbar_test(self.request.user)
        return context
    
    
class PasswordChange(LoginRequiredMixin, PasswordChangeView): 
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['navbar'] = navbar_test(self.request.user)
        return context


class PasswordChangeDone(PasswordChangeDoneView): 
    template_name = 'accounts/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group = self.request.user.groups.first()
        group_name = 'No Group'
        if user_group:
            group_name = user_group.name

        if group_name == "Admin":
            navbar = "admin/admin_navbar.html"
        elif group_name == "Organizer":
            navbar = "organizer/organizer_navbar.html"
        else:
            navbar = "participant/participant_navbar.html"
        context['navbar'] = navbar
        messages.success(self.request, "Your Password Was changed Successfully!")
        return context


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('sign_in')
    html_email_template_name = 'accounts/reset_email.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure else 'http'
        context['domain'] = self.request.get_host()
        context['navbar'] = navbar_test(self.request.user)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'A reset email is sent to your email')
        return super().form_valid(form)
    

class PasswordResetConfirm(PasswordResetConfirmView): 
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = navbar_test(self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password reset Successfull!')
        return super().form_valid(form)


class EditProfileView(LoginRequiredMixin, UpdateView): 
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html' 
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = navbar_test(self.request.user)
        return context
    
    def form_valid(self, form): 
        form.save()
        return redirect('profile')