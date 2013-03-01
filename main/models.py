from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) # HTML

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return str(self.name)


class CourseOffering(models.Model):
    class Meta:
        permissions = (('can_apply', 'Can apply for Course Offering'),)

    course = models.ForeignKey(Course)

    date = models.DateField()

    def __repr__(self):
        return "%s %s" % (self.course.name, str(self.date))

    def __unicode__(self):
        return unicode("%s %s" % (self.course.name, str(self.date)))

    def __str__(self):
        return str("%s %s" % (self.course.name, str(self.date)))


class AttachmentType(models.Model):
    name = models.CharField(max_length=100)


class Attachment(models.Model):
    courseOffering = models.ForeignKey(CourseOffering)
    attachmentType = models.ForeignKey(AttachmentType)

    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)

    courses = models.ManyToManyField(CourseOffering, blank=True)
    status = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
