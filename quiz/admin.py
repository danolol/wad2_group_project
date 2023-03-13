from django.contrib import admin
from quiz.models import UserProfile, Quiz, Question, Answer, Review, Outcome

class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(UserProfile)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(Outcome)


# Register your models here.
