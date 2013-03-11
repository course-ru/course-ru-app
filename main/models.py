# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Course(models.Model):
    name = models.CharField(max_length=40)
    short_summary = models.TextField(max_length=200)
    description = models.TextField()
    organisation = models.CharField(max_length=30)
    logo = models.FileField(upload_to='logos')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        permissions = (('can_apply', 'Can apply for Course'),)

    def __repr__(self):
        return "%s %s" % (self.name, str(self.start_date))

    def __unicode__(self):
        return unicode("%s %s" % (self.name, str(self.start_date)))


class Lecture(models.Model):
    name = models.CharField(max_length=100)
    youtube_video_id = models.CharField(max_length=32)
    order = models.IntegerField(unique=True)
    date = models.DateField()
    course = models.ForeignKey(Course)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

class Document(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, blank=True)
    doc = models.FileField(upload_to='docs')
    upload_date = models.DateTimeField()
    appear_date = models.DateTimeField()

class Feedback(models.Model):
    body = models.TextField()

    def __repr__(self):
        return self.body

    def __unicode__(self):
        return "feedback %s" % self.body


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    courses = models.ManyToManyField(Course, blank=True)

    def is_student(self):
        return True if (len(self.user.groups.filter(name='students')) > 0) else False

    def is_instructor(self):
        return True if (len(self.user.groups.filter(name='instructors')) > 0) else False

    def __repr__(self):
        return str(self.user)

    def __unicode__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
