from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

class Quiz(models.Model):

    title = models.CharField(max_length = 128)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)
    views = models.IntegerField(default = 0)
    date = models.DateField(default = datetime.date.today)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
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
    index = models.IntegerField("index", default=0)

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
    image = models.ImageField(upload_to='outcome_images', blank=True)
    index = models.IntegerField("index", default = 0)

    def __str__(self):
        return self.name
