from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Survey_Questions (models.Model):
    text = models.CharField(max_length=500) 
    question_group = models.CharField(max_length=250)
    question_number = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.text}"
   
    def get_questions(self):
        return self.questions_set.all()
       
    class Meta:
        verbose_name_plural = 'Survey Questions'


class Survey_Answers (models.Model):
    text = models.CharField(max_length=500)
    user_name = models.CharField(max_length=250) 
    question_group = models.CharField(max_length=250)
    user_answer = models.CharField(max_length=250)
    question_number = models.CharField(max_length=150)
    user_accept_condition = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.text},{self.user_answer}"
   
    def get_questions(self):
        return self.questions_set.all()
       
    class Meta:
        verbose_name_plural = 'Survey Answers'