import json
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.http import JsonResponse
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


@require_POST
def contact_submit(request):
    try:
        data = json.loads(request.body)

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '')
        event = data.get('event_type', '')
        date = data.get('event_date', '')
        guests = data.get('guests', '')
        message = data.get('message', '')

        if not name or not email:
            return JsonResponse({'ok': False, 'error': 'Name and email are required.'}, status=400)

        subject = f"New Event Inquiry from {name} — {event or 'Unspecified'}"
        body = f"""
New contact request received from your website.

Name:        {name}
Email:       {email}
Phone:       {phone or '—'}
Event Type:  {event or '—'}
Event Date:  {date or '—'}
Guests:      {guests or '—'}

Message:
{message or '(no message)'}
        """.strip()

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  # sends to yourself
        )

        return JsonResponse({'ok': True})

    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
