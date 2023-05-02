from django.db import models
from django.contrib.auth.models import User


TYPE_CHOICES = (

    ('GREY', 'GREY'),
    ('ACADEMIC', 'ACADEMIC'),

)


STATUS_TYPES = (

    ('ACTIVE', 'ACTIVE'),
    ('PASSIVE', 'PASSIVE'), 

)


class Controls(models.Model):
    text = models.CharField(max_length=1800)
    risk_group = models.CharField(max_length=500)
    risk_type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name_plural = 'Controls'       




class Main_Risk_Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=450)
    assessment_number = models.CharField(max_length=500)
    active_status = models.CharField(max_length=100, choices=STATUS_TYPES)
    risk_score = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}, {self.risk_score}"
    
    class Meta:
        verbose_name_plural = 'Main Risk Results'


class Risk_Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    risk_group =  models.CharField(max_length=200)
    assessment_number = models.CharField(max_length=500)
    active_status = models.CharField(max_length=100, choices=STATUS_TYPES)
    asset_type =  models.CharField(max_length=100)
    question_group = models.CharField(max_length=1000)
    threat_score = models.CharField(max_length=50)
    impact_score = models.CharField(max_length=50)
    vulnerability_score = models.CharField(max_length=50)
    even_likelihood = models.CharField(max_length=50)
    qualitative_result =  models.CharField(max_length=50)
    quantitative_result = models.CharField(max_length=50)
    title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}, {self.assessment_number}, {self.active_status}, {self.qualitative_result},{self.question_group} "

    def get_controls(self):
        return self.controls_set.all()
    
    class Meta:
        verbose_name_plural = 'Risk Results'


