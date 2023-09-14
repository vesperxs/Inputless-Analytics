from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Room represent a chat room. It contains an online field for tracking when users connect
# and disconnect from the chat 
class Room(models.Model):
    name = models.CharField(max_length=255)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self,user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        #return f'{self.name} ({self.get_online_count})'
        return f'{self.name}'


# This class represent a message sent to the chat room. We'll use this model to store all the
# messages sent in the chat
    
class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
    
    
    
