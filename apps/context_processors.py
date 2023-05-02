from django.conf import settings
from apps.questionnaire.models import Risk_Assessment

def cfg_assets_root(request):

    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }

 
def risk_assessments(request):
    if request.user.is_authenticated:
        risk_assessments = Risk_Assessment.objects.filter(user=request.user)
    else:
        risk_assessments = []
    return {'risk_assessments': risk_assessments}

def current_assessment(request):
    if request.user.is_authenticated:
        active_risk_assessment = Risk_Assessment.objects.filter(user=request.user, active_status='ACTIVE').first()
        if active_risk_assessment:
            return {'current_assessment': active_risk_assessment.assessment_number}
    return {}
