from django.contrib import admin
from quiz.models import UserProfile, Quiz, Question, Answer, Review, Outcome

admin.site.register(UserProfile)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(Outcome)


# Register your models here.
