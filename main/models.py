from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Course(models.Model):
    name = models.CharField(max_length=100)
    short_summary = models.TextField(max_length=100)
    description = models.TextField()
    organisation = models.CharField(max_length=100)
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


class Feedback(models.Model):
    body = models.TextField()

    def __repr__(self):
        return self.body

    def __unicode__(self):
        return "feedback %s" % self.body


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __repr__(self):
        return self.user

    def __unicode__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
