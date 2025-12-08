from django.shortcuts import render, redirect
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def events(request): 
    
    basequery = Event.objects.select_related(
        'category').prefetch_related('participant')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    keyword= request.GET.get('search')
    
    events = basequery.all().distinct()
    
    if start_date and end_date: 
        events = events.filter(date__range = [start_date, end_date]).distinct()
    elif start_date:
        events = events.filter(date__gte = start_date).distinct()
    elif end_date:
        events = events.filter(date__lte = end_date).distinct()
        
    if category_id:
        events = events.filter(category_id = category_id).distinct()
    
    if keyword:
        events = events.filter(Q(name__icontains=keyword) | Q(location__icontains = keyword)).distinct()
    
    user_group = request.user.groups.first()
    group_name = 'No Group'
    if user_group: 
        group_name = user_group.name 
        
    
    if group_name == "Admin": 
        navbar = "admin/admin_navbar.html"
    elif group_name == "Organizer":
        navbar = "organizer/organizer_navbar.html"
    else:
        navbar = "participant/participant_navbar.html"
    
    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories, 
        'navbar': navbar, 
    }
    
    
    return render(request, 'events.html', context)


@login_required
def event_detail(request):
    id = request.GET.get('id', '1')
    event = Event.objects.get(id= id)
    participants = list(event.participant.all().distinct())
    
    user_group = request.user.groups.first()
    group_name = 'No Group'
    if user_group:
        group_name = user_group.name

    if group_name == "Admin":
        navbar = "admin/admin_navbar.html"
    elif group_name == "Organizer":
        navbar = "organizer/organizer_navbar.html"
    else:
        navbar = "participant/participant_navbar.html"
    print(participants)
    context = {
        'event': event, 
        'participants': participants, 
        'navbar': navbar    
    }
    return render(request, 'event_detail.html', context )


@login_required
@permission_required("events.add_event", login_url='no_permission')
def create_event(request):
    form = EventModelForm()
    categoryform = CategoryModelForm()
    categories = Category.objects.all()
    if request.method == "POST" :
        form = EventModelForm(request.POST, request.FILES)
        categoryform = CategoryModelForm(request.POST)
        selected_cat = request.POST.get("category_select")
        if form.is_valid() and categoryform.is_valid():
            category_name = categoryform.cleaned_data.get('category_name')
            category_description = categoryform.cleaned_data.get(
                'category_description')
            if category_name : 
                category, created = Category.objects.get_or_create(
                    category_name=category_name)
                category.category_description = category_description
                category.save()
            else: 
                category = Category.objects.get(id = selected_cat)
            event = form.save(commit=False)
            event.category = category 
            event.save()
            
            # names = request.POST.getlist('participant_name[]')
            # emails = request.POST.getlist('participant_email[]')
            
            # for name, email in zip(names, emails):
            #     participant = User.objects.filter(name = name, email = email).first()
            #     if not participant: 
            #         participant = User.objects.create(name= name, email = email)
            #     event.participant.add(participant)
            
            messages.success(request, "Event Created Successfully")    
            return redirect('create_event')
        
    user_group = request.user.groups.first()
    group_name = 'No Group'
    if user_group:
        group_name = user_group.name

    if group_name == "Admin":
        navbar = "admin/admin_navbar.html"
    elif group_name == "Organizer":
        navbar = "organizer/organizer_navbar.html"
    else:
        navbar = "participant/participant_navbar.html"
            
    context = {'form': form, 'category_form': categoryform, 'navbar': navbar, 'categories': categories}
    return render(request, 'create_event.html',  context)



@login_required
@permission_required("events.change_event", login_url='no_permission')
def update_event(request, id):
    event = Event.objects.get(id= id)
    form = EventModelForm(instance = event)
    category_name = event.category.category_name
    categoryform = CategoryModelForm(instance = event.category)
    # existing_participants = list(event.participant.all())
    categories = Category.objects.all()
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES, instance = event)
        categoryform = CategoryModelForm(request.POST, instance = event.category)
        selected_cat = request.POST.get("category_select")
        if form.is_valid() and categoryform.is_valid():
            category_name = categoryform.cleaned_data.get('category_name')
            category_description = categoryform.cleaned_data.get(
                'category_description')
            if category_name:
                category, created = Category.objects.get_or_create(
                    category_name=category_name)
                category.category_description = category_description
                category.save()
            else:
                category = Category.objects.get(id=selected_cat)
            event = form.save(commit=False)
            event.category = category
            event.save()
            
            # names = request.POST.getlist('participant_name[]')
            # emails = request.POST.getlist('participant_email[]')
            # pairs = set(zip(names, emails))
            # for participant in existing_participants : 
            #     if (participant.name, participant.email) not in pairs: 
            #        event.participant.remove(participant) 

            # for name, email in zip(names, emails):
            #     participant = User.objects.filter(
            #         name=name, email=email).first()
            #     if not participant:
            #         participant = User.objects.create(
            #             name=name, email=email)
            #     event.participant.add(participant)

            messages.success(request, "Event Updated Successfully")
            return redirect('update_event', id = event.id)
    user_group = request.user.groups.first()
    group_name = 'No Group'
    if user_group:
        group_name = user_group.name

    if group_name == "Admin":
        navbar = "admin/admin_navbar.html"
    elif group_name == "Organizer":
        navbar = "organizer/organizer_navbar.html"
    else:
        navbar = "participant/participant_navbar.html"

    context = {'form': form, 'category_form': categoryform, 'navbar': navbar, 'categories': categories, 'category_name': category_name}
    
    return render(request, 'update_event.html',  context)



@login_required
@permission_required("events.delete_event", login_url='no_permission')
def delete_event(request, id):
     if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        
        user_group = request.user.groups.first()
        group_name = 'No Group'
        if user_group:
            group_name = user_group.name
        
        if group_name == "Admin":
            return redirect('admin_dashboard')
        elif group_name == "Organizer": 
            return redirect('organizer_dashboard')
        else:
            return redirect('home')
    