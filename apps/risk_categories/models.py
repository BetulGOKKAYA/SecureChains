from django.db import models
from django.contrib.auth.models import User


RISK_CATEGORY_CHOICES = (

    ('Infrastructure Questionnaire', 'Infrastructure Questionnaire'),
    ('Hardware Risk', 'Hardware Risk'),
    ('Software Risk', 'Software Risk'),
    ('User Risk', 'User Risk'),
    ('Assessment Result', 'Assessment Result'),

)


class Security_Risk_Category (models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=100, choices=RISK_CATEGORY_CHOICES)
    total_number_of_questions = models.CharField(max_length=30, blank=True) 



    def __str__(self):
        return f"{self.category}"
   
    def get_questions(self):
        return self.questions_set.all()
       
    class Meta:
        verbose_name_plural = 'Categories'
 
