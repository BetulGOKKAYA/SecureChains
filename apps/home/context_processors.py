from apps.questionnaire.models import Risk_Assessment_Number



 
def risk_assessments(request):
    if request.user.is_authenticated:
        risk_assessments = Risk_Assessment_Number.objects.filter(user=request.user)
    else:
        risk_assessments = []
    return {'risk_assessments': risk_assessments}
