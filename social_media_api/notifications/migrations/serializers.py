from rest_framework import serializers
from .models import Notification
from posts.models import Post,Comment


class NotifyRecipientSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username',read_only=True)
    verb_display = serializers.CharField(source='get_verb_display',read_only=True)
    total_notifications = serializers.SerializerMethodField()
    target_preview = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['id','actor_username','timestamp','is_seen','target_preview','verb_display','text_preview','total_notifications']
    
    def get_total_notifications(self,obj):
        return obj.recipient.recipient_notifications.count()
    def get_target_preview(self,obj):
        #here, we want to present the target object, which can be a comment or post to be serializable
        target = obj.target
        
        if isinstance(target,Post):
            return {"id": target.id, "title": target.title}
        elif isinstance(target,Comment):
            return {"id": target.id, "content": target.content}