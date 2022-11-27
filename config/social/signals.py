from django.db.models.signals import post_delete,post_save
from .models import Profile
from accounts.models import User


def autoCreate(sender,created,instance,**kwargs):

    if created:
        profile=Profile(
            user=instance
        )
        profile.save()

post_save.connect(autoCreate,sender=User)