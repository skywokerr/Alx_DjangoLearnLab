from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
#here we start creating the notification model. An important time to learn

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        (1,'Like'),
        (2,'Comment'),
        (3,'Follow')
    ]
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='recipient_notifications')
    #we get the content_type to allow us to access models installed in the project
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    #we get the id of the object, whether it is a comment,post,or a like
    object_id = models.PositiveIntegerField(verbose_name='name of the object in question')
    #here, the actor acts as the sender
    actor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='actor_sender_notifications')
    #we then get the object we are targeting and pass the content_type
    target = GenericForeignKey("content_type","object_id")
    timestamp = models.DateTimeField(auto_now_add=True)
    verb = models.IntegerField(choices=NOTIFICATION_TYPES) #represents the action
    text_preview = models.CharField(max_length=50,blank=True)
    is_seen = models.BooleanField(default=False)
    
    #django models.Model has a get_verb_display method that allows you get to get a verb which references choices
    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()} {self.target}"
        #here, I want to return something like James liked "this title"
    @property
    def totalrecipientnotifications(self):
        total_notifications = self.recipient_notifications.all().count()
        return str(total_notifications)
