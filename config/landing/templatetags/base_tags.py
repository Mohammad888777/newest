from django import template
from social.models import Notification

register=template.Library()


@register.inclusion_tag("social/show_notifitactions.html",takes_context=True)
def show_notifitactions(context):

    user=context["request"].user

    notifications=Notification.objects.select_related("to_user","from_user","comment").filter(
        to_user=user
    ).exclude(
        user_has_seen=True
    ).distinct()

    return {
        "notifications":notifications
    }