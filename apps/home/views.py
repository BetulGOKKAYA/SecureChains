from django import template
import ast
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.risk_categories.models import Security_Risk_Category
from apps.survey.models import Survey_Questions,Survey_Answers
from apps.questionnaire.models import Risk_Questions, Risk_Assessment, User_Answer
from apps.assessment_results.models import Risk_Result, Control, Main_Risk_Result
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.db.models import Q
import re
import json
import csv
from datetime import datetime



@login_required(login_url="/login/")
def index(request):
    categories = Security_Risk_Category.objects.all()
    user_get = request.user

    risk_data = {}


    for c in categories:
        if(c.name=="q_infra"):
            total_question_number = Risk_Questions.objects.filter(risk_group=c.pk).count()
            user_answer = User_Answer.objects.filter(user=user_get, active_status='ACTIVE',risk_group="Infrastructure Questionnaire").count()
            if user_answer==0:
                risk_data['infra'] = 0
            elif user_answer:
                risk_data['infra'] = int((user_answer/total_question_number)*100)
        if(c.name=="q_hardware"):
            total_question_number_harware = Risk_Questions.objects.filter(risk_group=c.pk).count()
            user_answer_hardware = User_Answer.objects.filter(user=user_get, active_status='ACTIVE', risk_group="Hardware Risk").count()
            if user_answer_hardware==0:
                risk_data['hardware'] = 0
            elif user_answer_hardware and total_question_number_harware!=0:
                risk_data['hardware'] = int((user_answer_hardware/total_question_number_harware)*100)
        if(c.name=="q_software"):
            total_question_number_sw = Risk_Questions.objects.filter(risk_group=c.pk).count()
            user_answer_sw = User_Answer.objects.filter(user=user_get, active_status='ACTIVE', risk_group="Software Risk").count()
            if user_answer_sw==0:
                risk_data['sw'] = 0
            elif user_answer_sw and total_question_number_sw!=0:
                risk_data['sw'] = int((user_answer_sw/total_question_number_sw)*100)
        if(c.name=="q_user"):
            total_question_number_user = Risk_Questions.objects.filter(risk_group=c.pk).count()
            user_answer_user = User_Answer.objects.filter(user=user_get, active_status='ACTIVE', risk_group="User Risk").count()
            if user_answer_user==0:
                risk_data['user'] = 0
            elif user_answer_user and total_question_number_user!=0:
                risk_data['user'] = int((user_answer_user/total_question_number_user)*100)


    context = {
        'categories': categories,
        'risk_data': risk_data,
    }

    return render(request, 'home/index.html', context)


@login_required(login_url="/login/")
def index_data(request):
    '''
    This method counts the values for risk result data in order to display on dasboard (withing graphs)
    '''
    user_get = request.user
    results = Risk_Result.objects.filter(user=user_get, active_status='ACTIVE')



    result_data = {
    'very_high': 0,
    'high': 0,
    'medium': 0,
    'low': 0,
    'very_low': 0
    }

    for r in results:
        if r.qualitative_result == 'Very High':
            result_data['very_high'] += 1
        elif r.qualitative_result == 'High':
            result_data['high'] += 1
        elif r.qualitative_result == 'Medium':
            result_data['medium'] += 1
        elif r.qualitative_result == 'Low':
            result_data['low'] += 1
        elif r.qualitative_result == 'Very Low':
            result_data['very_low'] += 1




    data = []

    risk_results = Main_Risk_Result.objects.filter(user=user_get, active_status='ACTIVE')


    context = {

        'results': list(results.values()),
        'result_data': result_data,
        'jsonData': data,
        'risk_results': list(risk_results.values('name', 'risk_score'))


    }

    return JsonResponse(context)


@login_required(login_url="/login/")
def category_view(request, pk):
    categories = Security_Risk_Category.objects.get(pk=pk)
    return render(request, 'home/risk_questions.html')


@csrf_exempt
@login_required(login_url="/login/")
def change_active_status(request):
    if request.method == 'POST':
        assessment_number = request.POST.get('assessment_number')

        # Set all other assessments to 'passive'
        Risk_Assessment.objects.filter(user=request.user).update(active_status='PASSIVE')

        # Set the clicked assessment to 'active'
        Risk_Assessment.objects.filter(user=request.user, assessment_number=assessment_number).update(active_status='ACTIVE')

        # Set all other User_Answer instances to 'PASSIVE'
        User_Answer.objects.filter(Q(user=request.user) & ~Q(assessment_number=assessment_number)).update(active_status='PASSIVE')

        # Set the clicked User_Answer instances to 'ACTIVE'
        User_Answer.objects.filter(user=request.user, assessment_number=assessment_number).update(active_status='ACTIVE')

        # Set all other Main_Risk_Result instances to 'PASSIVE'
        Main_Risk_Result.objects.filter(Q(user=request.user) & ~Q(assessment_number=assessment_number)).update(active_status='PASSIVE')

        # Set the clicked Main_Risk_Result instances to 'ACTIVE'
        Main_Risk_Result.objects.filter(user=request.user, assessment_number=assessment_number).update(active_status='ACTIVE')

        # Set all other Risk_Result instances to 'PASSIVE'
        Risk_Result.objects.filter(Q(user=request.user) & ~Q(assessment_number=assessment_number)).update(active_status='PASSIVE')

        # Set the clicked Risk_Result instances to 'ACTIVE'
        Risk_Result.objects.filter(user=request.user, assessment_number=assessment_number).update(active_status='ACTIVE')

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@csrf_exempt
@login_required(login_url="/login/")
def create_new_risk(request):
    if request.method == 'POST':
        # Retrieve the highest assessment number for the current user
        max_assessment_number = Risk_Assessment.objects.filter(user=request.user).aggregate(Max('assessment_number'))['assessment_number__max']

        if max_assessment_number is not None:
            # Extract the number from the string, increment it by 1
            next_assessment_number = int(max_assessment_number.split('_')[1]) + 1
        else:
            next_assessment_number = 1

        # Create the new assessment_number string
        new_assessment_number = f'assessment_{next_assessment_number}'

        # Set all other assessments to 'passive'
        Risk_Assessment.objects.filter(user=request.user).update(active_status='PASSIVE')

        # Create a new risk assessment entry
        new_risk = Risk_Assessment(user=request.user, assessment_number=new_assessment_number, active_status='ACTIVE')
        new_risk.save()

        # Set all User_Answer instances to 'PASSIVE'
        User_Answer.objects.filter(user=request.user).update(active_status='PASSIVE')

        # Set all Main_Risk_Result instances to 'PASSIVE'
        Main_Risk_Result.objects.filter(user=request.user).update(active_status='PASSIVE')

        # Set all Risk_Result instances to 'PASSIVE'
        Risk_Result.objects.filter(user=request.user).update(active_status='PASSIVE')

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url="/login/")
def questions_data_view(request, pk):
    category = Security_Risk_Category.objects.get(pk=pk)
    filtered_questions = Risk_Questions.objects.filter(risk_group=category).order_by('suggestion')
    group= str(category)

    user_answer = []
    asset_list = []
    user_get = request.user
    user_answer = list(User_Answer.objects.filter(user=user_get,  active_status='ACTIVE').values_list('text', flat=True))
    answers = User_Answer.objects.filter(user=user_get,risk_group='Infrastructure Questionnaire', active_status='ACTIVE')

    questions = []
    information = []
    likelihood = ["Very Low", "Low", "Medium", "High", "Very High"]
    impact = ["Very Low", "Low", "Medium", "High", "Very High"]
    general = ["Yes", "No"]


    '''
    Below code eliminates the question based on the user answer which is related to organization assets. For
    example, if user answers 'infrastructure related question' as 'we don't use thrid-part software', then user
    will not see third-party software related questions
    '''

    if answers:
        for a in answers:
            if a.asset_type and a.user_answer=='Yes':
                asset_list.append(a.asset_type )



    if group == 'Infrastructure Questionnaire':
        for q in filtered_questions:
            if(q.question_type=="GENERAL"):
                questions.append({str(q.text): general})
                information.append({str(q.text): str(q.description)})


    for q in filtered_questions:
        if q.asset_type in asset_list:
            if q.question_type == "LIKELIHOOD":
                questions.append({str(q.text): likelihood})
                information.append({str(q.text): str(q.description)})
            elif q.question_type == "IMPACT":
                questions.append({str(q.text): impact})
                information.append({str(q.text): str(q.description)})
            elif group == 'Infrastructure Questionnaire' and q.question_type == "GENERAL":
                questions.append({str(q.text): general})
                information.append({str(q.text): str(q.description)})



    questions = [q for q in questions if next(iter(q)) not in user_answer]


    return JsonResponse({
        'data': questions,
        'metadata': information,
    })

def normalize_string(s):
    return re.sub(r'\s+', ' ', s.strip())

@login_required(login_url="/login/")
def questions_data_save(request, pk):
    # print(request.POST) # to see the response in command line
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        #print(type(data)) -> type(data) is to see what type the data is in command line
        #result of above line is: <class 'django.http.request.QueryDict'>
        #this is a querydict, and we need to turn that one into regular python dic with below code line
        data_ = dict(data.lists())

        active_risk_assessment = Risk_Assessment.objects.filter(Q(user=request.user) & Q(active_status='ACTIVE')).first()
        active_value =  active_risk_assessment.assessment_number

        data_.pop('csrfmiddlewaretoken')#data value has csrfmiddlewaretoken which we can remove with this code in order to have result data


        for k in data_.keys(): #keys are QUESTION
            question = Risk_Questions.objects.get(text=k) #with (text=k) we can bring all question related with their text
            x = str(question.risk_group)
            riskGroup = x.split(',', 1)[0]
            #riskGroup = x.split(',')[0].split()[0]
            questions.append(question)

        user = request.user
        risk = Security_Risk_Category.objects.get(pk=pk)
        results = []
        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                User_Answer.objects.create(user=user, text=q.text, assessment_number=active_value, active_status='ACTIVE', risk_group = riskGroup, asset_type = q.asset_type, question_group =q.question_group,relative_vul_group=q.relative_vul_group, question_type=q.question_type, value_type=q.value_type, root_risk=q.root_risk, question_number=q.question_number, threat_type=q.threat_type, perceived_threat=q.perceived_threat, user_answer = a_selected)
                save_to_csv("NO", user.username, q.text, a_selected, riskGroup, q.asset_type)


        relative_vul = []
        single_vul = None
        is_Assest = None
        vulnerability_score = None
        rootThreat = None
        rootVul = []
        rootImpact = None

        '''
        The below code snipped calculates the cumulative vulnerability valuse. If we have more than one vulnerability for a specific threat,
        then the code provide overal vulnerability level.
        '''

        answers = User_Answer.objects.filter(user=user,active_status='ACTIVE')

        # Group answers by question_group
        grouped_answers = {}
        for answer in answers:
            if answer.question_group not in grouped_answers:
                grouped_answers[answer.question_group] = {}
            if answer.value_type == "IMPACT":
                grouped_answers[answer.question_group]['IMPACT'] = answer
            elif answer.value_type == "THREAT":
                grouped_answers[answer.question_group]['THREAT'] = answer

        # Process each group
        for question_group, grouped_answer in grouped_answers.items():
            rootVul = []

            impact_answer = grouped_answer.get('IMPACT')
            threat_answer = grouped_answer.get('THREAT')

            if not (impact_answer and threat_answer):
                # If either IMPACT or THREAT answer is missing, skip the group
                continue

            rootImpact = impact_answer.root_risk
            rootThreat = threat_answer.root_risk


            if threat_answer.relative_vul_group:
                relative_vul = [item.strip() for item in threat_answer.relative_vul_group.split(',')]
            else:
                relative_vul = []

            multi_vulnerability_score = []

            for v in answers:
                if v.relative_vul_group in relative_vul and v.value_type == "VULNERABILITY":
                    multi_vulnerability_score.append(v.user_answer)
                    rootVul.append(v.root_risk)



            is_single_vul = len(multi_vulnerability_score) == 1



            # Proceed with your existing logic
            if is_single_vul:
                # If there's effectively one unique vulnerability, use its score directly
                vulnerability_score = multi_vulnerability_score[0]
            else:
                # If there are multiple unique vulnerabilities, aggregate their scores
                multi_vul_value = compute_value(multi_vulnerability_score)
                vulnerability_score = multi_vul_value


            # Calculate event likely for both cases, as it depends on vulnerability_score
            event_likely = get_event_values(threat_answer.user_answer, vulnerability_score)





            multi_vulScore = '; '.join([item for item in multi_vulnerability_score if item.strip()])
            rootVul_string = '; '.join([item for item in rootVul if item.strip()])
            final_result = get_event_values(impact_answer.user_answer, event_likely)

            # Update or create Risk_Result entry
            Risk_Result.objects.update_or_create(
                user=user,
                question_group=question_group,
                active_status='ACTIVE',
                defaults={
                    'risk_group': threat_answer.risk_group,
                    'assessment_number': active_value,
                    'asset_type': threat_answer.asset_type,
                    'multi_vulnerability_score': multi_vulScore,
                    'threat_score': threat_answer.user_answer,
                    'root_threat': rootThreat,
                    'impact_score': impact_answer.user_answer,
                    'root_impact': rootImpact,
                    'vulnerability_score': vulnerability_score,
                    'multi_relative_vul_group': relative_vul,
                    'root_vulnerability': rootVul_string,
                    'event_likelihood': event_likely,
                    'qualitative_result': final_result,
                    'quantitative_result': 'bos',
                    'threat_type': threat_answer.threat_type,
                    'perceived_threat': threat_answer.perceived_threat
                }
            )




        mainRisks = Risk_Result.objects.filter(user=user,active_status='ACTIVE')


        risk_data = {
        'COMPANY HARDWARE': [],
        'USER ELECTRONICS': [],
        'IoT': [],
        'THIRD-PARTY SOFTWARE': [],
        'SOFTWARE HOSTED on ORGANIZATION MACHINES': [],
        'INTERNAL USER': [],
        'EXTERNAL USER': [],
        'Supply Chain RISK': [],
        'Software Risk': [],
        'Hardware Risk': [],
        'User Risk': []

        }

        if mainRisks:
            for m in mainRisks:
                if m.asset_type in risk_data:
                    risk_data[m.asset_type].append(m.qualitative_result)
                    if m.risk_group == 'Software Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)
                    elif m.risk_group == 'Hardware Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)
                    elif m.risk_group == 'User Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)


            for asset_type, qualitative_results in risk_data.items():
                if qualitative_results:
                    # Check if a Main_Risk_Result with the same asset_type already exists
                    existing_main_risk_result = Main_Risk_Result.objects.filter(user=user, name=asset_type, active_status='ACTIVE').first()
                    if existing_main_risk_result:
                        # Update the existing Main_Risk_Result object
                        existing_main_risk_result.risk_score = calculate_aggregate_risk(qualitative_results)
                        existing_main_risk_result.save()
                    else:
                        # Create a new Main_Risk_Result object
                        Main_Risk_Result.objects.create(user=user,
                            name=asset_type, assessment_number=active_value, active_status='ACTIVE', risk_score=calculate_aggregate_risk(qualitative_results)
                        )

    return JsonResponse({
        'editdata': "questions",
    })


@login_required(login_url="/login/")
def user_answer(request, pk):

    categories = Security_Risk_Category.objects.get(pk=pk)
    return render(request, 'home/risk_questions_edit.html', {'obj': categories})


@login_required(login_url="/login/")
def user_answer_edit(request, pk):

    categories = Security_Risk_Category.objects.get(pk=pk)
    user_get = request.user
    user_answer = User_Answer.objects.filter(user=user_get, active_status='ACTIVE', risk_group=categories.category)


    questions = []
    answers = []
    likelihood = ["Very Low", "Low", "Medium", "High", "Very High"]
    impact = ["Very Low", "Low", "Medium", "High", "Very High"]
    general = ["Yes", "No"]



    for q in user_answer:
        if(q.question_type=="LIKELIHOOD"):
            questions.append({str(q.text): {'answer': likelihood, 'user_answer': q.user_answer}})
        elif(q.question_type=="IMPACT"):
            questions.append({str(q.text): {'answer': impact, 'user_answer': q.user_answer}})
        elif(q.question_type=="GENERAL"):
            questions.append({str(q.text): {'answer': general, 'user_answer': q.user_answer}})





    return JsonResponse({
        'data': questions
    })


@login_required(login_url="/login/")
def user_new_answer_save(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        answers = []
        data = request.POST
        user_get = request.user
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            answer = User_Answer.objects.filter(user=user_get, text=k, active_status='ACTIVE').first()
            if answer:
                answers.append(answer)

        user = request.user
        risk = Security_Risk_Category.objects.get(pk=pk)

        results = []
        single_vul = None
        resultQualitative = ''

        for q in answers:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                t = User_Answer.objects.filter(user=user_get, text=q.text, active_status='ACTIVE').first()
                if t:
                    t.user_answer = a_selected
                    if (t.value_type == "VULNERABILITY"):
                        risk_all = Risk_Result.objects.filter(user=user_get, active_status='ACTIVE')

                        changed_vulnerability = t.relative_vul_group

                        for r in risk_all:
                            multi_relative_vul_group = ast.literal_eval(r.multi_relative_vul_group)
                            if changed_vulnerability in multi_relative_vul_group:
                                position = multi_relative_vul_group.index(changed_vulnerability)
                                multi_vulnerability_score = r.multi_vulnerability_score.split('; ')
                                if position < len(multi_vulnerability_score):
                                    multi_vulnerability_score[position] = t.user_answer
                                    r.multi_vulnerability_score = '; '.join(multi_vulnerability_score)
                                    new_vul_score = compute_value(multi_vulnerability_score)
                                    r.vulnerability_score = new_vul_score
                                    event_likely = get_event_values(new_vul_score, r.threat_score)
                                    resultQualitative = get_event_values(event_likely, r.impact_score)
                                    r.event_likelihood = event_likely
                                    r.qualitative_result = resultQualitative
                                    r.save()
                                else:
                                    print(f"Index {position} out of range for multi_vulnerability_score")
                    if(t.value_type != "GENERAL" and t.value_type != "VULNERABILITY"):
                        r = Risk_Result.objects.filter(user=user_get, question_group=q.question_group, active_status='ACTIVE').first()
                        if r:
                            if (t.value_type == "IMPACT"):
                                resultQualitative = get_event_values(r.event_likelihood, t.user_answer)
                                r.qualitative_result = resultQualitative
                                r.impact_score = t.user_answer
                            elif (t.value_type == "THREAT"):
                                resultEvent = get_event_values(r.vulnerability_score, t.user_answer)
                                resultQualitative = get_event_values(resultEvent, r.impact_score)
                                r.event_likely = resultEvent
                                r.qualitative_result = resultQualitative
                                r.threat_score = t.user_answer
                    t.save()
                    save_to_csv("YES", user.username, q.text, a_selected, q.risk_group, q.asset_type)
                    r.save()

        mainRisks = Risk_Result.objects.filter(user=user,active_status='ACTIVE')

        risk_data = {
        'COMPANY HARDWARE': [],
        'USER ELECTRONICS': [],
        'IoT': [],
        'THIRD-PARTY SOFTWARE': [],
        'SOFTWARE HOSTED on ORGANIZATION MACHINES': [],
        'INTERNAL USER': [],
        'EXTERNAL USER': [],
        'Supply Chain RISK': [],
        'Software Risk': [],
        'Hardware Risk': [],
        'User Risk': []

        }
        if mainRisks:
            for m in mainRisks:
                if m.asset_type in risk_data:
                    risk_data[m.asset_type].append(m.qualitative_result)
                    if m.risk_group == 'Software Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)
                    elif m.risk_group == 'Hardware Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)
                    elif m.risk_group == 'User Risk':
                        risk_data[m.risk_group].append(m.qualitative_result)
                        risk_data['Supply Chain RISK'].append(m.qualitative_result)



            for asset_type, qualitative_results in risk_data.items():
                if qualitative_results:
                    # Check if a Main_Risk_Result with the same asset_type already exists
                    existing_main_risk_result = Main_Risk_Result.objects.filter(user=user, name=asset_type, active_status='ACTIVE').first()
                    if existing_main_risk_result:
                        # Update the existing Main_Risk_Result object
                        existing_main_risk_result.risk_score = calculate_aggregate_risk(qualitative_results)
                        existing_main_risk_result.save()


    return JsonResponse({
        'editdata': "questions",
    })


@login_required(login_url="/login/")
def risk_result_view(request, data):
    user_get = request.user
    if data=='hardware':
        riskGroup = 'Hardware Risk'
    elif data=='software':
        riskGroup = 'Software Risk'
    elif data=='user':
        riskGroup = 'User Risk'

    results = Risk_Result.objects.filter(user=user_get, active_status='ACTIVE', risk_group=riskGroup)
    for result in results:
        scores = [s.strip() for s in result.multi_vulnerability_score.split(';')]
        vulnerabilities = result.root_vulnerability.split(';')
        result.vulnerability_data = list(zip(scores, vulnerabilities))



    context = {

        'results': results,


    }

    return render(request, 'home/risk-results.html', context)


def save_to_csv(isupdated, username, question_text, answer, riskgroup, a_type):
    csv_path = 'user_answers.csv'

    # Check if the file exists. If not, create it and write the headers.
    try:
        with open(csv_path, 'x', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IsUpdated", "User Name", "Question Text", "User Answer","Risk Group", "Asset Type" "Timestamp"])
            print("New CSV file created.")
    except FileExistsError:
        pass

    # Append the user's answer to the CSV file
    try:
        with open(csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
            writer.writerow([isupdated, username, question_text, answer, riskgroup, a_type, timestamp])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

@login_required(login_url="/login/")
def risk_tree_view(request):


    return render(request, 'home/risk_tree.html')


@login_required(login_url="/login/")
def risk_tree_data(request):
    user_get = request.user
    results = Risk_Result.objects.filter(user=user_get, active_status='ACTIVE')
    hierarchical_data = create_hierarchical_data(request, results)

    context = {

        'results': list(results.values()),
        'hierarchical_data': hierarchical_data

    }

    return JsonResponse(context)

@login_required(login_url="/login/")
def create_hierarchical_data(request, data):
    user_get = request.user
    risk_results = Main_Risk_Result.objects.filter(user=user_get, active_status='ACTIVE')
    risk_score_map = {result.name: result.risk_score for result in risk_results}

    hierarchy = {
        "name": "Supply Chain RISK", "score": risk_score_map.get("Supply Chain RISK"),
        "children": []
    }

    sub_risk_structure = [
        {
            "name": "Hardware Risk", "score": risk_score_map.get("Hardware Risk"),
            "children": [
                {"name": "USER ELECTRONICS", "score": risk_score_map.get("USER ELECTRONICS")},
                {"name": "COMPANY HARDWARE", "score": risk_score_map.get("COMPANY HARDWARE")},
                {"name": "IoT", "score": risk_score_map.get("IoT")},
            ],
        },
        {
            "name": "Software Risk", "score": risk_score_map.get("Software Risk"),
            "children": [
                {"name": "THIRD-PARTY SOFTWARE", "score": risk_score_map.get("THIRD-PARTY SOFTWARE")},
                {"name": "SOFTWARE HOSTED on ORGANIZATION MACHINES", "score": risk_score_map.get("SOFTWARE HOSTED on ORGANIZATION MACHINES")},
            ],
        },
        {
            "name": "User Risk", "score": risk_score_map.get("User Risk"),
            "children": [
                {"name": "EXTERNAL USER", "score": risk_score_map.get("EXTERNAL USER")},
                {"name": "INTERNAL USER", "score": risk_score_map.get("INTERNAL USER")},
            ],
        },
    ]

    sub_risk_map = {}
    for sub_risk in sub_risk_structure:
        sub_risk_map[sub_risk["name"]] = sub_risk

    for item in data:
        risk_group = item.risk_group
        asset_type = item.asset_type
        question_group = item.question_group
        threat_score = item.threat_score
        impact_score = item.impact_score
        vulnerability_score = item.vulnerability_score
        qualitative_result = item.qualitative_result

        if risk_group in sub_risk_map:
            node = {
                "name": f"{question_group} Risk: {qualitative_result}", "value": qualitative_result,
                "children": [
                    {
                        "name": f"Threat: {threat_score}", "value": threat_score,
                    },
                    {
                        "name": f"Cumulative Vulnerability: {vulnerability_score}", "value": vulnerability_score
                    },
                    {
                        "name": f"Impact: {impact_score}", "value": impact_score
                    },
                ],
            }

            for child in sub_risk_map[risk_group]["children"]:
                if child["name"] == asset_type:
                    if "children" not in child:
                        child["children"] = []
                    child["children"].append(node)
                    break

    hierarchy["children"] = sub_risk_structure
    return hierarchy


@login_required(login_url="/login/")
def risk_control_view(request, pk):
    user_get = request.user
    result = Risk_Result.objects.filter(pk=pk).first()
    if not result:
        # You can handle the case when the result is not found here, e.g., show an error message or redirect to another page
        pass

    results = Risk_Result.objects.filter(pk=pk)
    grpup_type = result.question_group
    control = Control.objects.all()


    for result in results:
        scores = [s.strip() for s in result.multi_vulnerability_score.split(';')]
        vulnerabilities = result.root_vulnerability.split(';')
        vul_groups = [vg.replace("'", "").replace("[", "").replace("]", "").strip() for vg in result.multi_relative_vul_group.split(',')]
        result.control_data = list(zip(scores, vulnerabilities, vul_groups))


    context = {
        'controls': control,
        'results': results,
    }

    return render(request, 'home/control-results.html', context)


def qualitative_result(likelihood, impact):
    """
    this method calculates the risk result
    """
    risk_mapping = {
        ("Very Low", "Very Low"): "Very Low",
        ("Very Low", "Low"): "Very Low",
        ("Very Low", "Medium"): "Low",
        ("Very Low", "High"): "Low",
        ("Very Low", "Very High"): "Medium",
        ("Low", "Very Low"): "Very Low",
        ("Low", "Low"): "Low",
        ("Low", "Medium"): "Medium",
        ("Low", "High"): "Medium",
        ("Low", "Very High"): "High",
        ("Medium", "Very Low"): "Low",
        ("Medium", "Low"): "Medium",
        ("Medium", "Medium"): "Medium",
        ("Medium", "High"): "Medium",
        ("Medium", "Very High"): "High",
        ("High", "Very Low"): "Low",
        ("High", "Low"): "Medium",
        ("High", "Medium"): "Medium",
        ("High", "High"): "High",
        ("High", "Very High"): "Very High",
        ("Very High", "Very Low"): "Medium",
        ("Very High", "Low"): "High",
        ("Very High", "Medium"): "High",
        ("Very High", "High"): "Very High",
        ("Very High", "Very High"): "Very High",
    }

    return risk_mapping.get((likelihood, impact), ' ')




def calculate_aggregate_risk(qualitative_values):
    # Filter out empty strings or spaces
    filtered_values = [v for v in qualitative_values if v.strip()]

    # Return early if filtered list is empty or contains a single element
    if not filtered_values:
        return "No valid input"  # or return a default value as appropriate
    if len(filtered_values) == 1:
        return filtered_values[0]

    # Initialize the result with the first value
    result = filtered_values[0]

    # Aggregate the rest of the values
    for i in range(1, len(filtered_values)):
        result = get_event_values(result, filtered_values[i])

    return result


def compute_value(input_list):
    if not input_list:
        return 'No input provided'

    # mapping from strings to integers
    map_to_int = {
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'High': 4,
        'Very High': 5,
    }

    # mapping from integers to strings
    map_to_str = {
        1: 'Very Low',
        2: 'Low',
        3: 'Medium',
        4: 'High',
        5: 'Very High',
    }

    # map the strings in the input list to integers and compute the sum
    total = sum(map_to_int[value] for value in input_list)

    # calculate the average
    avg = total / len(input_list)

    # round the average to the nearest integer using "round half up" method
    #avg_rounded = int(avg + 0.5) if avg % 1 >= 0.5 else int(avg)
    avg_rounded = round(avg)


    # map the rounded average back to a string and return it
    return map_to_str[avg_rounded]


def get_event_values(value_1, value_2):
    event_values_mapping = {
        ("Very Low", "Very Low"): "Very Low",
        ("Very Low", "Low"): "Very Low",
        ("Very Low", "Medium"): "Low",
        ("Very Low", "High"): "Low",
        ("Very Low", "Very High"): "Medium",
        ("Low", "Very Low"): "Very Low",
        ("Low", "Low"): "Low",
        ("Low", "Medium"): "Medium",
        ("Low", "High"): "Medium",
        ("Low", "Very High"): "High",
        ("Medium", "Very Low"): "Low",
        ("Medium", "Low"): "Medium",
        ("Medium", "Medium"): "Medium",
        ("Medium", "High"): "Medium",
        ("Medium", "Very High"): "High",
        ("High", "Very Low"): "Low",
        ("High", "Low"): "Medium",
        ("High", "Medium"): "Medium",
        ("High", "High"): "High",
        ("High", "Very High"): "Very High",
        ("Very High", "Very Low"): "Medium",
        ("Very High", "Low"): "High",
        ("Very High", "Medium"): "High",
        ("Very High", "High"): "Very High",
        ("Very High", "Very High"): "Very High",
    }

    return event_values_mapping.get((value_1, value_2), ' ')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def survey(request):
    return render(request, 'home/survey_questions.html')


@login_required(login_url="/login/")
def survey_data_view(request):
    question_ = Survey_Questions.objects.all()

    user_answer = []
    user_get = request.user
    user_answer = list(Survey_Answers.objects.filter(user_name=user_get).values_list('text', flat=True))

    questions = []
    answers = ["1 (Strongly Disagree)", "1 (Disagree)", "3 (Neutral)", "4 (Agree)", "5 (Strongly Agree)"]



    for q in question_:
        questions.append({str(q.text): answers})

    # Only shows the questions that users haven't answered yet
    if user_answer:
        for ans in user_answer:
            for user_q in questions:
                if(next(iter(user_q)) == str(ans)):
                    questions.remove(user_q)


    return JsonResponse({
        'data': questions,
    })


@login_required(login_url="/login/")
def survey_data_save(request):
    # print(request.POST) # to see the response in command line
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        answers = []
        data = request.POST
        #print(type(data)) -> type(data) is to see what type the data is in command line
        #result of above line is: <class 'django.http.request.QueryDict'>
        #this is a querydict, and we need to turn that one into regular python dic with below code line
        data_ = dict(data.lists())
        user_get = request.user
        user_answer = list(Survey_Answers.objects.filter(user_name=user_get).values_list('text', flat=True))

        data_.pop('csrfmiddlewaretoken')#data value has csrfmiddlewaretoken which we can remove with this code in order to have result data


        for k in data_.keys(): #keys are QUESTION
            question = Survey_Questions.objects.get(text=k) #with (text=k) we can bring all question related with their text
            questions.append(question)

        for k in data_.keys(): #keys are QUESTION
            answer = Survey_Answers.objects.get(text=k) #with (text=k) we can bring all question related with their text
            #print(question)
            answers.append(answer)

        user = request.user
        if not user_answer:
            for q in questions:
                a_selected = request.POST.get(q.text)
                if a_selected != "":
                    Survey_Answers.objects.create(text=q.text, user_name=user, question_group = q.question_group,  user_answer = a_selected, question_number=q.question_number, user_accept_condition='yes')

        if user_answer:
            for q in answers:
                a_selected = request.POST.get(q.text)
                if a_selected != "":
                    t = Survey_Answers.objects.get(text=q.text)
                    t.user_answer = a_selected
                t.save()


    return JsonResponse({
        'editdata': "questions",
    })

@login_required(login_url="/login/")
def survey_answer_edit(request):


    user_get = request.user
    user_answer = Survey_Answers.objects.filter(user_name=user_get)


    questions = []
    answers = ["1 (Strongly Disagree)", "1 (Disagree)", "3 (Neutral)", "4 (Agree)", "5 (Strongly Agree)"]



    for q in user_answer:
        questions.append({str(q.text): {'answer': answers, 'user_answer': q.user_answer}})



    return JsonResponse({
        'data': questions
    })

@login_required(login_url="/login/")
def survey_new_data_save(request):

    # print(request.POST) # to see the response in command line
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        answers = []
        data = request.POST
        #print(type(data)) -> type(data) is to see what type the data is in command line
        #result of above line is: <class 'django.http.request.QueryDict'>
        #this is a querydict, and we need to turn that one into regular python dic with below code line
        data_ = dict(data.lists())


        data_.pop('csrfmiddlewaretoken')#data value has csrfmiddlewaretoken which we can remove with this code in order to have result data


        for k in data_.keys(): #keys are QUESTION
            answer = Survey_Answers.objects.get(text=k) #with (text=k) we can bring all question related with their text
            #print(question)
            answers.append(answer)

        user = request.user
        for q in answers:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                t = Survey_Answers.objects.get(text=q.text)
                t.user_answer = a_selected
            t.save()


    return JsonResponse({
        'editdata': "questions",
    })
