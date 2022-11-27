from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment,Profile,Notification
from django.http import Http404


class UpdateDeleteostMixin:

    def dispatch(self,request,pk,*args,**kwargs):
        post=get_object_or_404(Post,pk=pk)
        if self.request.user.is_authenticated:
            if self.request.user == post.user:
                return super().dispatch(request,*args,**kwargs)
            else:
                return redirect("index")
        else:
            return redirect("login_account")
        
class FieldMixin():

    def dispatch(self,request,*args,**kwargs):
        self.fields=["image","body"]
        if self.request.user.is_superuser and self.request.user.is_authenticated:
            self.fields.extend(["user"])
        return super().dispatch(request,*args,**kwargs)


class UpdateDeleteComment:

    def dispatch(self,request,pk,*args,**kwargs):
        
        comment=get_object_or_404(Comment,pk=pk)
        if self.request.user.is_authenticated :
            if self.request.user == comment.user:
                return super().dispatch(request,*args,**kwargs)
            else:
                return redirect("index")
        else:
            return redirect("account_login")
            

class CheckNotToBeAFollower():

    def dispatch(self,request,pk,*args,**kwargs):
        profile=get_object_or_404(Profile,pk=pk)
        if self.request.user.is_authenticated :
            if not self.request.user in profile.followers.all():
                return super().dispatch(request,pk,*args,**kwargs)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")



class PostNotificationMixin:

    
    def dispatch(self,request,post_pk,notification_pk,*args,**kwargs):

        post=get_object_or_404(Post,pk=post_pk)
        notification=get_object_or_404(Notification,pk=notification_pk)

        if self.request.user.is_authenticated:
            if self.request.user==post.user and self.request.user == notification.to_user:
                return super().dispatch(request,post_pk,notification_pk,*args,**kwargs)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")
        


class Inbox():
    pass