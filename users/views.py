from django.shortcuts import render, redirect
from users.forms import CustomSignUpForm, CustomSignInForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from events.models import Event
from django.db.models import Count, Q, Prefetch
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test


# Test for Users
def is_admin(user): 
    return user.groups.filter(name = 'Admin').exists()

def is_organizer(user): 
    return user.groups.filter(name = 'Organizer').exists()

def is_participant(user): 
    return user.groups.filter(name = 'Participant').exists()



#main functions

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

