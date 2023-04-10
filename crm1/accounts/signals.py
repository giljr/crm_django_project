from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from accounts.models import Customer

from django.dispatch import receiver

# from accounts/views.py


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(user=instance, name=instance.username,)
        print('****************')
        print('Customer created!')
        print('****************')


# post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created is False:
        instance.customer.email = instance.email
        name = instance.first_name + ' ' + instance.last_name
        instance.customer.name = name
        instance.customer.save()
        print('****************')
        print('Customer Updated!')
        print('****************')


# post_save.connect(update_profile, sender=User)
