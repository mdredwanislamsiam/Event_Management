from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Participant, Category
from django.db.models import Count, Q
from datetime import date
from django.contrib import messages

def home(request): 
    return render(request, 'home.html')


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
    
    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories
    }
    return render(request, 'events.html', context)


    


def event_detail(request):
    id = request.GET.get('id', '1')
    event = Event.objects.get(id= id)
    participants = list(event.participant.all().distinct())
    return render(request, 'event_detail.html', {'event': event, 'participants': participants})

def dashboard(request):
    type = request.GET.get('type', 'today')
    basequery = Event.objects.select_related('category').prefetch_related('participant')
    
    if type =='all':
        events = basequery.all().distinct()
        title = "All Events"
    elif type =='upcoming':
        events = basequery.filter(date__gt = date.today()).distinct()
        title = "Upcoming Events"
    elif type =='past':
        events = basequery.filter(date__lt = date.today()).distinct()
        title = "Past Events"
    elif type =='today': 
        events= basequery.filter(date = date.today()).distinct()
        title = "Today's Events"
        
    counts = Event.objects.aggregate(
        total_event = Count('id', distinct=True), 
        total_participant = Count('participant', distinct=True), 
        upcoming_events = Count('id', filter=Q(date__gt = date.today()), distinct=True),
        past_events = Count('id', filter=Q(date__lt = date.today()), distinct= True), 
        todays_events = Count('id', filter=Q(date = date.today()), distinct=True)
    )
    context = {
        'counts': counts, 
        'events':events,    
        'title': title
    }
    return render(request, 'dashboard.html', context)



def create_event(request):
    form = EventModelForm()
    categoryform = CategoryModelForm()
    if request.method == "POST" :
        form = EventModelForm(request.POST, request.FILES)
        categoryform = CategoryModelForm(request.POST)
        if form.is_valid() and categoryform.is_valid():
            category_name = categoryform.cleaned_data.get('category_name')
            category_description = categoryform.cleaned_data.get('category_description')
            category, created=  Category.objects.get_or_create(category_name = category_name, category_description = category_description)
            event  = form.save(commit=False)
            event.category = category 
            event.save()
            names = request.POST.getlist('participant_name[]')
            emails = request.POST.getlist('participant_email[]')
            
            for name, email in zip(names, emails):
                participant = Participant.objects.filter(name = name, email = email).first()
                if not participant: 
                    participant = Participant.objects.create(name= name, email = email)
                event.participant.add(participant)
            
            messages.success(request, "Task Created Successfully")    
            return redirect('create_event')
            
            
    context = {'form': form, 'category_form': categoryform}
    return render(request, 'create_event.html',  context)



def update_event(request, id):
    event = Event.objects.get(id= id)
    form = EventModelForm(instance = event)
    categoryform = CategoryModelForm(instance = event.category)
    existing_participants = list(event.participant.all())
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES, instance = event)
        categoryform = CategoryModelForm(request.POST, instance = event.category)
        if form.is_valid() and categoryform.is_valid():
            category_name = categoryform.cleaned_data.get('category_name')
            category_description = categoryform.cleaned_data.get(
                'category_description')
            category, created = Category.objects.get_or_create(
                category_name=category_name, category_description=category_description)
            event = form.save(commit=False)
            event.category = category
            event.save()
            names = request.POST.getlist('participant_name[]')
            emails = request.POST.getlist('participant_email[]')
            pairs = set(zip(names, emails))
            
            for participant in existing_participants : 
                if (participant.name, participant.email) not in pairs: 
                   event.participant.remove(participant) 

            for name, email in zip(names, emails):
                participant = Participant.objects.filter(
                    name=name, email=email).first()
                if not participant:
                    participant = Participant.objects.create(
                        name=name, email=email)
                event.participant.add(participant)

            messages.success(request, "Task Updated Successfully")
            return redirect('update_event', id = event.id)

    context = {'form': form, 'category_form': categoryform, 'participants': existing_participants}
    return render(request, 'update_event.html',  context)

def delete_event(request, id):
     if request.method == "POST":
         event = Event.objects.get(id = id)
         event.delete()
         messages.success(request, "Task Deleted Successfully")
         return redirect('dashboard')
    