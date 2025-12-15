from django.shortcuts import render

def home(request):
    
    group = request.user.groups.first()
    
    group_name = "No Group"
    if group: 
        group_name = group.name
    
    if group_name == "Admin": 
        navbar = 'admin/admin_navbar.html'
    elif group_name == "Organizer": 
        navbar = 'organizer/organizer_navbar.html'
    elif group_name =="Participant": 
        navbar = 'participant/participant_navbar.html'
    else: 
        navbar = 'navbar.html'

    
    return render(request, 'home.html', {'navbar': navbar})

def no_permission(request): 
    return render(request, 'no_permission.html') 