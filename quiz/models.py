from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    title = models.CharField(max_length = 128)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length = 255)

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

    def __str__(self):
        return self.description

class Review(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comments = models.CharField(max_length = 255)

    def __str__(self):
        return self.comments

class Outcome(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    imagePath = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
