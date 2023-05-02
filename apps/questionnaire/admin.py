from django.contrib import admin
from .models import Risk_Questions, User_Answer, Risk_Assessment


admin.site.register(Risk_Questions)
admin.site.register(Risk_Assessment) 
admin.site.register(User_Answer)


# Register your models here.
