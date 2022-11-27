from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone




class Post(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    image=models.ManyToManyField("Image",blank=True)
    likes=models.ManyToManyField(User,related_name="likes",blank=True)
    dislikes=models.ManyToManyField(User,related_name="dislikes",blank=True)
    tags=models.ManyToManyField('Tag',blank=True)

    
    def create_tags(self):

        for word in self.body.split():
            if word[0]=="#":
                tag=Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag=Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    tag.save()



    

    def __str__(self) -> str:
        
        return self.user.username



class Comment(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    comment=models.TextField(null=True,blank=True)
    image=models.ManyToManyField("Image",blank=True)
    likes=models.ManyToManyField(User,related_name="comment_likes",blank=True)
    dislikes=models.ManyToManyField(User,related_name="comment_dislikes",blank=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    tags=models.ManyToManyField('Tag',blank=True)

    @property
    def children(self):

        return Comment.objects.filter(parent=self).order_by("-created").all()
        

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        else:
            return False
    
    def create_tags(self):

        for word in self.comment.split():
            if word[0]=="#":
                tag=Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag=Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    tag.save()



    def __str__(self) -> str:
        return self.user.username
    


class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    name=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    bio=models.CharField(max_length=200,null=True,blank=True)
    bithday=models.DateField(blank=True,null=True)
    image=models.ImageField(upload_to="ProfileIMG",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    followers=models.ManyToManyField(User,related_name="followers",blank=True)
    followings=models.ManyToManyField(User,related_name="followings",blank=True)


    def __str__(self) -> str:
        return self.name


class Notification(models.Model):
    
    # like =1 comment =2 follow=3 DM=4
    notification_type=models.IntegerField()
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notification_to",null=True,blank=True)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notification_from",null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    thread=models.ForeignKey("Thread",on_delete=models.CASCADE,null=True,blank=True,related_name="+")
    date=models.DateTimeField(default=timezone.now)
    user_has_seen=models.BooleanField(default=False)




class Thread(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_sender')
    receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_receiver')

class Message(models.Model):
    
    thread = models.ForeignKey(Thread, related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user_messages')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user_messages')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    video=models.FileField(upload_to="VideosMessages",null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)





class Image(models.Model):

    image=models.ImageField(upload_to="POSTIMG",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])



class Tag(models.Model):

    name=models.CharField(max_length=200,null=True,blank=True)