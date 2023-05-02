from django.db import models
from apps.risk_categories.models import Security_Risk_Category
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save




ASSET_TYPE_CHOICES = (

    ('COMPANY HARDWARE', 'COMPANY HARDWARE'),
    ('USER ELECTRONICS', 'USER ELECTRONICS'),
    ('IoT', 'IoT'),
    ('THIRD-PARTY SOFTWARE', 'THIRD-PARTY SOFTWARE'),
    ('SOFTWARE HOSTED on ORGANIZATION MACHINES', 'SOFTWARE HOSTED on ORGANIZATION MACHINES'),
    ('INTERNAL USER', 'INTERNAL USER'),
    ('EXTERNAL USER', 'EXTERNAL USER'),
  

)

QUESTION_TYPE_CHOICES = (

    ('LIKELIHOOD', 'LIKELIHOOD'),
    ('IMPACT', 'IMPACT'),
    ('GENERAL', 'GENERAL'),
    ('EXT', 'EXT'),

)

TYPES = (

    ('VULNERABILTY', 'VULNERABILTY'),
    ('THREAT', 'THREAT'),
    ('IMPACT', 'IMPACT'),
    ('ASSET', 'ASSET'),

)

 

ASSESSMENT_STATUS_TYPES = (

    ('ACTIVE', 'ACTIVE'),
    ('PASSIVE', 'PASSIVE'), 

)
 

class Risk_Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_number = models.CharField(max_length=500)
    active_status = models.CharField(max_length=100, choices=ASSESSMENT_STATUS_TYPES)

    def __str__(self):
        return f"{self.user}, {self.assessment_number}, {self.active_status}"

    class Meta:
        verbose_name_plural = 'Security Risk Assessment'

@receiver(post_save, sender=User)
def create_risk_assessments(sender, instance, created, **kwargs):
    if created:
        assessments = [
            {'assessment_number': 'scenario_1', 'active_status': 'ACTIVE'},
            {'assessment_number': 'scenario_2', 'active_status': 'PASSIVE'},
            {'assessment_number': 'scenario_3', 'active_status': 'PASSIVE'},
        ]
        for assessment in assessments:
            Risk_Assessment.objects.create(user=instance, **assessment)

class Risk_Questions(models.Model):
    text = models.CharField(max_length=1500)
    risk_group = models.ForeignKey(Security_Risk_Category, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    question_group = models.CharField(max_length=850)
    value_type = models.CharField(max_length=50, choices=TYPES)
    question_number = models.CharField(max_length=100)
    threat_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=600, blank=True, null=True)
    suggestion = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.asset_type}, {self.threat_type}, {self.question_group}, {self.question_number}"

    class Meta:
        verbose_name_plural = 'Security Risk Questions'





class User_Answer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)
    assessment_number = models.CharField(max_length=500)
    active_status = models.CharField(max_length=100, choices=ASSESSMENT_STATUS_TYPES)
    risk_group = models.CharField(max_length=150)
    asset_type = models.CharField(max_length= 50)
    question_group = models.CharField(max_length=850)
    question_type = models.CharField(max_length=50)
    value_type = models.CharField(max_length=150)
    question_number = models.CharField(max_length=100)
    threat_type = models.CharField(max_length=100, blank=True, null=True)
    user_answer = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}, {self.text},{self.assessment_number}, {self.user_answer}"
    
    class Meta:
        verbose_name_plural = 'User Answers'



 






