from django.shortcuts import render, redirect
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from users.views import navbar_test

User = get_user_model()

""" ---- Function Based Views ---- """

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
def event_detail(request, id):
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
    # print(participants)
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
    categoryform = CategoryModelForm()
    # existing_participants = list(event.participant.all())
    categories = Category.objects.all()
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES, instance = event)
        categoryform = CategoryModelForm(request.POST)
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
    
    
""" ---- Class Based Views ---- """
    
    
class EventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'

    def get_queryset(self):
        basequery = Event.objects.select_related(
            'category').prefetch_related('participant')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        category_id = self.request.GET.get('category')
        keyword = self.request.GET.get('search')
        events = basequery.all().distinct()
        if start_date and end_date:
            events = events.filter(
                date__range=[start_date, end_date]).distinct()
        elif start_date:
            events = events.filter(date__gte=start_date).distinct()
        elif end_date:
            events = events.filter(date__lte=end_date).distinct()

        if category_id:
            events = events.filter(category_id=category_id).distinct()

        if keyword:
            events = events.filter(Q(name__icontains=keyword) | Q(
                location__icontains=keyword)).distinct()

        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['navbar'] = navbar_test(self.request.user)
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context["participants"] = list(event.participant.all().distinct())
        context['navbar'] = navbar_test(self.request.user)
        return context


class CreateEventView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'events.add_event'
    login_url = 'no_permission'
    model = Event
    form_class = EventModelForm
    context_object_name = 'form'
    template_name = 'create_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = CategoryModelForm()
        context['categories'] = Category.objects.all()
        context['navbar'] = navbar_test(self.request.user)
        return context

    def form_valid(self, form):
        category_form = CategoryModelForm(self.request.POST)

        # Validate category form
        if category_form.is_valid():
            category_name = category_form.cleaned_data.get('category_name')
            category_description = category_form.cleaned_data.get(
                'category_description')
        else:
            category_name = None
            category_description = None

        selected_cat = self.request.POST.get('category_select')

        # If no category selected and no new category entered, show error
        if not selected_cat and not category_name:
            messages.error(
                self.request, "Please select a category or fill the new category form.")
            return self.form_invalid(form)

        # Use new category if entered
        if category_name:
            category, created = Category.objects.get_or_create(
                category_name=category_name)
            category.category_description = category_description
            category.save()
        else:
            # Make sure selected_cat is valid
            try:
                category = Category.objects.get(id=int(selected_cat))
            except (ValueError, Category.DoesNotExist):
                messages.error(self.request, "Please select a valid category.")
                return self.form_invalid(form)

        # Save event
        event = form.save(commit=False)
        event.category = category
        event.save()
        messages.success(self.request, "Event Created Successfully")
        return redirect('create_event')


class UpdateEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'events.change_event'
    login_url = 'no_permission'

    model = Event
    form_class = EventModelForm
    template_name = 'update_event.html'
    context_object_name = 'form'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = navbar_test(self.request.user)
        return context

    def form_valid(self, form):
        event = form.save()
        messages.success(self.request, "Event Updated Successfully")
        return redirect('update_event', id=event.id)


class DeleteEventView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'events.delete_event'
    login_url = 'no_permission'
    
    model = Event 
    context_object_name = 'event'
    pk_url_kwarg = 'id'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event Deleted Successfully")
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        user_group = self.request.user.groups.first()
        group_name = 'No Group'
        if user_group:
            group_name = user_group.name

        if group_name == "Admin":
            return reverse('admin_dashboard')
        elif group_name == "Organizer":
            return reverse('organizer_dashboard')
        elif group_name == 'Participant':
            return reverse('participant_dashboard')
        else: 
            return reverse('home')


