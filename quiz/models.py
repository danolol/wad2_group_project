from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, upload_to='profile_pictures', default="default.png", blank=True)

    def __str__(self):
        return self.user.username
    

    def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfile(user=instance)
            user_profile.save()
            
    post_save.connect(create_profile, sender=User)


class Quiz(models.Model):

    title = models.CharField(max_length = 128)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)
    views = models.IntegerField(default = 0)
    date = models.DateField(default = datetime.date.today)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + " " + str(self.creator.user.id))
        super(Quiz, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.description
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)
    index = models.IntegerField("index")

    def __str__(self):
        return self.description

class Review(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comments = models.CharField(max_length = 255)
    date = models.DateField()

    def __str__(self):
        return self.comments

class Outcome(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    image = models.ImageField(upload_to='outcome_images')
    index = models.IntegerField("index")

    def __str__(self):
        return self.name
