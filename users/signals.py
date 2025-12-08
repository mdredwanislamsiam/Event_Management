from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from events.models import Event


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs): 
    if created: 
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        subject = 'Activate Your Account'
        message = f"Hi {instance.username}, \n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You"
        recipient = [instance.email]
        
        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs): 
    if created: 
        user_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(user_group)
        instance.save()
        
        
        
@receiver(m2m_changed, sender=Event.participant.through)
def send_rsvp_confirmation_email(sender, instance, action, **kwargs): 
    if action == "post_add": 
        user = instance.participant.last()
        subject = "New Event Added"
        confirmation_email = f"Hello {user.first_name} {user.last_name}, \n\nYou are  now engaged in the {instance.name} which will take place at {instance.location}, at {instance.date}, {instance.time}.\n\nThank You \nOrganizer\nGood-Day Event Management System"
        recipient = [user.email]
        
        try:
            send_mail(subject, confirmation_email,
                      settings.EMAIL_HOST_USER, recipient)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")
