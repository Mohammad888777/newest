from django.shortcuts import render,redirect,get_object_or_404
from .models import Message, Post,Comment,Profile,Notification, Thread,Image,Tag
from django.views import View
from django.views.generic import ListView
from .forms import PostForm,CommentForm,ThreadForm,MessageForm,ExploreForm
from django.views.generic.edit import UpdateView,DeleteView
from .mixisn import UpdateDeleteostMixin,FieldMixin,UpdateDeleteComment,CheckNotToBeAFollower,PostNotificationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .utils import hadle_paginator
from django.db.models import Q
from accounts.models import User
from django.contrib import messages



class PostView(View):

    def get(self,request,*args,**kwargs):

        posts=Post.objects.select_related("user").all().order_by("-created")

        contex={
            'posts':posts,
            'form':PostForm()
        }
        return render(request,"social/posts.html",contex)

    def post(self,request,*args,**kwargs):

        form=PostForm(self.request.POST,self.request.FILES)
        imges=self.request.FILES.getlist("image")

        if form.is_valid():
            post=form.save(commit=False)
            post.user=self.request.user
            post.save()
            post.create_tags()

            for i in imges:
                img=Image(image=i)
                img.save()
                post.image.add(img)

            post.save()



            return redirect("posts")


class PostDetail(View):

    def get(self,request,pk,*args,**kwargs):

        post=get_object_or_404(Post.objects.prefetch_related("comment_set").select_related("user"),pk=pk)

        comments=post.comment_set.select_related("post","user").all().order_by("-created")

        likes_count=post.likes.all().count()
        dislikes_count=post.dislikes.all().count()


        contex={
            'post':post,
            'form':CommentForm(),
            'comments':comments,
            'likes_count':likes_count,
            'dislikes_count':dislikes_count
        }

        return render(request,"social/post_detail.html",contex)

    def post(self,request,*args,**kwargs):

        post=get_object_or_404(Post,pk=self.kwargs.get("pk"))

        form=CommentForm(self.request.POST)
        imges=self.request.FILES.getlist("image")


        if form.is_valid():
            comment=form.save(commit=False)
            comment.user=self.request.user
            comment.post=post
            comment.save()
            comment.create_tags()
            for i in imges:
                img=Image(image=i)
                img.save()
                comment.image.add(img)
            comment.save()

            if self.request.user !=post.user:
                notification=Notification(
                    from_user=self.request.user,to_user=post.user,post=post,notification_type=2,
                )
                notification.save()

            return redirect(self.request.META.get("HTTP_REFERER"))
        
    
class UpdatePost(LoginRequiredMixin,FieldMixin,UpdateDeleteostMixin,UpdateView):

    model=Post
    template_name: str="social/update_post.html"

    def get_success_url(self) -> str:

        return reverse("post_detail",kwargs={"pk":self.kwargs.get("pk")})
    

class DeletePost(LoginRequiredMixin,FieldMixin,UpdateDeleteostMixin,DeleteView):

    model=Post
    template_name: str="social/delete_post.html"

    def get_success_url(self) -> str:

        return reverse("posts")

class UpdateComment(LoginRequiredMixin,UpdateDeleteComment,UpdateView):
    fields=["comment"]

    model=Comment
    template_name: str="social/update_comment.html"

    def get_success_url(self) -> str:

        return reverse("post_detail",kwargs={"pk":self.object.post.pk})


class DeleteComment(UpdateDeleteComment,LoginRequiredMixin,DeleteView):

    model=Comment
    template_name: str="social/delete_comment.html"

    def get_success_url(self) -> str:

        return reverse("post_detail",kwargs={"pk":self.object.post.pk})

class ProfileView(View):

    def get(self,request,pk,*args,**kwargs):

        profile=get_object_or_404(Profile.objects.select_related("user"),pk=pk)
        posts=profile.user.post_set.select_related("user").prefetch_related("comment_set").all()

        followers=profile.followers.all()
        number_of_followers=followers.count()
        number_of_followngs=profile.followings.all().count()

        is_following=False

        for follower in followers:
            if follower==self.request.user:
                is_following=True
            else:
                is_following=False


        contex={
            'profile':profile,
            'posts':posts,
            'followers':followers,
            'number_of_followers':number_of_followers,
            'number_of_followngs':number_of_followngs,
            'is_following':is_following
        }

        return render(request,"social/profile.html",contex)

class UpdateProfile(LoginRequiredMixin,UpdateView):

    model=Profile
    fields=["name","location","bio","image"]
    template_name: str="social/update_profile.html"

    def get_success_url(self) -> str:
        return reverse("profile",kwargs={"pk":self.object.pk})
    
    def dispatch(self, request,pk, *args, **kwargs) :

        profile=get_object_or_404(Profile,pk=pk)

        if self.request.user.is_authenticated:
            if self.request.user == profile.user:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")


class Follow(LoginRequiredMixin,CheckNotToBeAFollower,View):

    def post(self,request,pk,*args,**kwargs):

        profile=get_object_or_404(Profile,pk=pk)

        profile.followers.add(self.request.user)
        profile.save()

        if profile.user !=self.request.user:
            self.request.user.profile.followings.add(profile.user)
                

            notification=Notification(
                from_user=self.request.user,to_user=profile.user,notification_type=3,
            )
            notification.save()


        return redirect("profile",pk=profile.pk)
        


class UnFollow(LoginRequiredMixin,View):

    def post(self,request,pk,*args,**kwargs):
        profile=get_object_or_404(Profile,pk=pk)

        profile.followers.remove(self.request.user)
        profile.save()
        if profile.user !=profile.user:
            self.request.user.profile.followings.remove(profile.user)
        
        return redirect("profile",pk=profile.pk)

    def dispatch(self, request,pk, *args, **kwargs) :
        profile=get_object_or_404(Profile,pk=pk)
        
        if self.request.user.is_authenticated:
            if self.request.user in profile.followers.all():
                return super().dispatch(request,pk, *args, **kwargs)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")



class LikePost(LoginRequiredMixin,View):
    
    def post(self,request,pk,*args,**kwargs):

        post=get_object_or_404(Post,pk=pk)

        is_dislike=False

        for dislike in post.dislikes.all():
            if dislike==self.request.user:
                is_dislike=True
            else:
                is_dislike=False
        
        
        
        if is_dislike:
            post.dislikes.remove(self.request.user)

        
        is_like=False

        for like in post.likes.all():
            if like ==self.request.user:
                is_like=True
            else:
                is_like=False

        if not is_like:
            post.likes.add(self.request.user)
            if self.request.user != post.user:

                notification=Notification(
                    from_user=self.request.user,to_user=post.user,post=post,notification_type=1,
                )
                notification.save()

        
        if is_like:
            post.likes.remove(self.request.user)

        nex=self.request.POST.get("next","/")
        return HttpResponseRedirect(nex)


class DisLikePost(LoginRequiredMixin,View):  
    
    def post(self,request,pk,*args,**kwargs):

        post=get_object_or_404(Post,pk=pk)

        is_like=False

        for like in post.likes.all():
            if like==self.request.user:
                is_like=True
            else:
                is_like=False
        
        
        
        if is_like:
            post.likes.remove(self.request.user)

        
        is_dislike=False

        for dislike in post.dislikes.all():
            if dislike ==self.request.user:
                is_dislike=True
            else:
                is_dislike=False

        if not is_dislike:
            post.dislikes.add(self.request.user)
            if self.request.user != post.user:

                notification=Notification(
                    from_user=self.request.user,to_user=post.user,post=post,notification_type=1,
                )
                notification.save()
        
        if is_dislike:
            post.dislikes.remove(self.request.user)

        nex=self.request.POST.get("next","/")
        return HttpResponseRedirect(nex)

    
class Search(View):
    
    def get(self,request,*args,**kwargs):

        page=self.request.GET.get("page",1)
        q=self.request.GET.get("q",1)

        profiles=Profile.objects.select_related("user").prefetch_related("followers","followings").filter(
            Q(user__username__icontains=q) | Q(name__icontains=q) 
        )

        result=hadle_paginator(profiles,1,page)

        contex={
            'profiles':result,
            'q':q
        }

        return render(request,"social/search.html",contex)


class Followers(LoginRequiredMixin,ListView):

    template_name: str="social/followers.html"

    def get_queryset(self):
        global profile
        profile=get_object_or_404(Profile,pk=self.kwargs.get("pk"))

        return profile.followers.all()

    def get_context_data(self, **kwargs):

        contex=super().get_context_data(**kwargs)
        contex["profile"]=profile
        return contex
    

class Followings(LoginRequiredMixin,ListView):

    template_name: str="social/followings.html"

    def get_queryset(self) :
        global profile
        profile=get_object_or_404(Profile,pk=self.kwargs.get("pk"))
        return profile.followings.all()

    def get_context_data(self, **kwargs) :

        contex= super().get_context_data(**kwargs)
        contex["profile"]=profile
        return contex
    

    
class LikeComment(LoginRequiredMixin,View):

    def post(self,request,pk,*args,**kwargs):

        comment=get_object_or_404(Comment,pk=pk)

        is_dislike=False

        for dislike in comment.dislikes.all():
            if dislike==self.request.user:
                is_dislike=True
            else:
                is_dislike=False
        
        if is_dislike:
            comment.dislikes.remove(self.request.user)


        is_like=False
        for like  in comment.likes.all():
            if like == self.request.user:
                is_like=True
            else:
                is_like=False
        
        if not is_like:
            comment.likes.add(self.request.user)
        if is_like:
            comment.likes.remove(self.request.user)


        next=self.request.POST.get("next","/")
        return HttpResponseRedirect(next)

        

class DisLikeComment(LoginRequiredMixin,View):

    def post(self,request,pk,*args,**kwargs):

        comment=get_object_or_404(Comment,pk=pk)

        is_like=False

        for like in comment.likes.all():
            if like==self.request.user:
                is_like=True
            else:
                is_like=False
        
        if is_like:
            comment.likes.remove(self.request.user)


        is_dislike=False
        for dislike  in comment.dislikes.all():
            if dislike == self.request.user:
                is_dislike=True
            else:
                is_dislike=False
        
        if not is_dislike:
            comment.dislikes.add(self.request.user)
        if is_dislike:
            comment.dislikes.remove(self.request.user)


        next=self.request.POST.get("next","/")
        return HttpResponseRedirect(next)
        



class ReplayComment(LoginRequiredMixin,View):
    
    def post(self,request,post_pk,pk,*args,**kwargs):

        post=get_object_or_404(Post,pk=post_pk)
        comment=get_object_or_404(Comment,pk=pk)
        form=CommentForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.parent=comment
            new_comment.user=self.request.user
            new_comment.post=post
            new_comment.save()
            if self.request.user !=comment.user:
                
                notification=Notification(
                    from_user=self.request.user,to_user=new_comment.user,comment=comment,
                    notification_type=2
                ) 
                notification.save()

            

            return redirect("post_detail",pk=post.pk)




class PostNotification(LoginRequiredMixin,PostNotificationMixin,View):
    
    def get(self,request,post_pk,notification_pk,*args,**kwargs):

        post=get_object_or_404(Post,pk=post_pk)
        notification=get_object_or_404(Notification,pk=notification_pk)

        notification.user_has_seen=True
        notification.save()

        return redirect("post_detail",pk=post.pk)



class FollowNotification(LoginRequiredMixin,View):

    def get(self,request,profile_pk,notification_pk,*args,**kwargs):
        
        profile=get_object_or_404(Profile,pk=profile_pk)
        notification=get_object_or_404(Notification,pk=notification_pk)
        notification.user_has_seen=True
        notification.save()
        return redirect("profile",pk=profile.pk)

    
    def dispatch(self, request,profile_pk,notification_pk, *args, **kwargs) :

        profile=get_object_or_404(Profile,pk=profile_pk)
        notification=get_object_or_404(Notification,pk=notification_pk)

        if self.request.user.is_authenticated:
            if self.request.user == notification.to_user:
                return super().dispatch(request,profile_pk,notification_pk, *args, **kwargs)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("login_account")
    



class Inbox(LoginRequiredMixin,ListView):

    template_name: str="social/inbox.html"

    def get_queryset(self) :

        global profile

        profile=get_object_or_404(Profile,pk=self.kwargs.get("pk"))

        return profile
    
    def get_context_data(self, **kwargs):
        contex= super().get_context_data(**kwargs)

        contex["sender"]=profile.user.thread_sender.all()
        contex["receiver"]=profile.user.thread_receiver.all()


        return contex
    
    def dispatch(self, request,pk, *args, **kwargs) :

        profile=get_object_or_404(Profile,pk=pk)

        if self.request.user.is_authenticated:
            if self.request.user==profile.user:
                return super().dispatch(request,pk, *args, **kwargs)
            else:
                return redirect('profile',pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")
    
        

class CreateThread(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        form=ThreadForm()
        contex={
            'form':form
        }

        return render(request,"social/create_thread.html",contex)
    
    def post(self,request,*args,**kwargs):

        username=self.request.POST.get("username")
        form=ThreadForm(self.request.POST)

        try:
            receiver=User.objects.get(username=username)

        except User.DoesNotExist:

            messages.error(request,"not user found")
            return redirect(self.request.META.get("HTTP_REFERER"))

        threadOne=Thread.objects.filter(user=self.request.user,receiver=receiver)
        threadTwo=Thread.objects.filter(user=receiver,receiver=self.request.user)

        if threadOne.exists():
            thread=threadOne
            return redirect("thread",pk=threadOne.pk)

        elif threadTwo.exists():
            thread=threadTwo
            return redirect("thread",pk=thread.pk)
        else:
            if form.is_valid():
                thread=Thread(
                    user=self.request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect("thread",pk=thread.pk)



class ThreadView(LoginRequiredMixin,View):

    def get(self,request,pk,*args,**kwargs) :

        thread=get_object_or_404(Thread,pk=pk)
        messages=None

        if thread:
            messages=Message.objects.filter(thread=thread)
        
        contex={

            'message_list':messages,
            'form':MessageForm(),
            'thread':thread

        }

        return render(request,"social/thread.html",contex)

    def dispatch(self, request,pk, *args, **kwargs):
        thread=get_object_or_404(Thread,pk=pk)

        if self.request.user.is_authenticated:
            if self.request.user == thread.user or self.request.user == thread.receiver:
                
                return super().dispatch(request,pk, *args, **kwargs)
            else:
                return redirect("profile",pk=self.request.user.pk)
        else:
            return redirect("account_login")


class CreateMessage(LoginRequiredMixin,View):

    def post(self,request,pk,*args,**kwargs):

        thread=get_object_or_404(Thread,pk=pk)

        form=MessageForm(self.request.POST,self.request.FILES)

        if thread.receiver ==self.request.user:
            receiver=thread.user
        else:
            receiver=thread.receiver
        if form.is_valid():
            message=form.save(commit=False)
            message.thread=thread
            message.sender_user=self.request.user
            message.receiver_user=receiver
            message.save()

            if self.request.user !=message.receiver_user:

                notification=Notification(
                    notification_type=4,to_user=message.receiver_user,from_user=self.request.user,thread=thread
                )
                notification.save()

            return redirect("thread",pk=thread.pk)

    def dispatch(self, request, *args,pk, **kwargs) :
        thread=get_object_or_404(Thread,pk=pk)

        if self.request.user.is_authenticated:
            if str(thread.user) == str(self.request.user) or str(thread.receiver)==str(self.request.user):
                return super().dispatch(request,pk, *args, **kwargs)
            return redirect("profile",pk=self.request.user.profile.pk)
        return redirect("account_login")

    


class ThreadNotification(LoginRequiredMixin,View):
    
    def get(self,reqeust,thread_pk,notification_pk,*args,**kwargs):

        thread=get_object_or_404(Thread,pk=thread_pk)
        notification=get_object_or_404(Notification,pk=notification_pk,thread=thread)
        notification.user_has_seen=True
        notification.save()
        return redirect("thread",pk=thread.pk)
    
    def dispatch(self, request,thread_pk,notification_pk, *args, **kwargs) :

        thread=get_object_or_404(Thread,pk=thread_pk)
        notification=get_object_or_404(Notification,pk=notification_pk)

        if self.request.user.is_authenticated:
            if self.request.user == notification.to_user:
                if self.request.user == thread.user or self.request.user==thread.receiver:

                    return super().dispatch(request, *args, **kwargs)
                else:
                    return redirect("profile",pk=self.request.user.profile.pk)
            else:
                return redirect("profile",pk=self.request.user.profile.pk)
        else:
            return redirect("account_login")
        
            

        



class Explore(View):

    def get(self,request,*args,**kwargs):

        form=ExploreForm()
        q=self.request.GET.get("q")
        tag=Tag.objects.filter(name=q).first()

        # posts=None

        if tag:
            posts=Post.objects.select_related("user").prefetch_related("image","likes","dislikes","tags").filter(
               Q( tags__in=[tag])|Q(comment__tags__in=[tag])
            )
        else:
            posts=Post.objects.select_related("user").prefetch_related("image","likes","dislikes","tags").all()


        contex={
            'form':form,
            'posts':posts,
            'tag':tag
        }

        return render(request,"social/explore.html",contex)

    def post(self,request,*args,**kwargs):

        form=ExploreForm(self.request.POST)
        if form.is_valid():
            q=form.cleaned_data["q"]
            tag=Tag.objects.filter(name=q).exists()
            if tag:
                return HttpResponseRedirect(f"/social/explore/q={str(q)}")
        #     else:
        #         messages.error(request,"tag doesnot exisi")
        #         return HttpResponseRedirect("/social/explore/")
        # return HttpResponseRedirect("/social/explore")
        









    



