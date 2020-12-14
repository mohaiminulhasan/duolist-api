from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError

User = get_user_model()

class List(models.Model):
    userone = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_as_primary', null=True, blank=True)
    usertwo = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_as_secondary', null=True, blank=True)

    def __str__(self):
        if (self.userone == None or self.usertwo == None):
            return 'Unassigned List: {}'.format(self.id)
        return 'List of {} and {}'.format(self.userone.username, self.usertwo.username)

    class Meta:
        unique_together = ('userone', 'usertwo')

    def save(self, *args, **kwargs):
        if (self.userone == None or self.usertwo == None):
            pass
        elif (self.userone == self.usertwo):
            raise IntegrityError('A user must share the list with someone else and not himself/herself.')
        elif self.userone_id > self.usertwo_id:
            self.userone, self.usertwo = self.usertwo, self.userone
        super().save(*args, **kwargs)

class ListItem(models.Model):
    parent = models.ForeignKey(List, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        if (len(self.body) > 20):
            return '{}: {}...'.format(self.author.username, self.body[:20])
        return '{}: {}'.format(self.author.username, self.body)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)

class Invite(models.Model):
    sender = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='received_invites')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Invite for {}, sent by {}'.format(self.receiver.username, self.sender.username)

class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, blank=True, null=True, related_name='received_notifications', on_delete=models.CASCADE)
    action = models.CharField(max_length=30)

    def __str__(self):
        if (self.action == 'invite'):
            return '{}: {} sent an invitation to connect.'.format(self.receiver, self.sender)
        return '{} {} {}'.format(self.sender, self.action, self.receiver)

    class Meta:
        ordering = ['-created']
