from django.contrib import admin
from .models import Post,Comment,Profile,Notification,Thread,Image,Tag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Thread)
admin.site.register(Image)
admin.site.register(Tag)