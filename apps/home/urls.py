from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('data/', views.index_data, name='home-data'),
    path('<pk>/', views.category_view, name='dashboard-questions-view'),
    path('<pk>/data/', views.questions_data_view, name='questions-data-view'),
    path('<pk>/save/', views.questions_data_save, name='questions-data-save'),
    path('answer/<pk>/', views.user_answer, name='questions-user-answer'),
    path('answer/<pk>/edit/', views.user_answer_edit, name='questions-user-answer-edit'),
    path('answer/<pk>/save/', views.user_new_answer_save, name='questionsuser-answer-save'),
    path('risk/results/<data>/', views.risk_result_view, name='dashboard-risk-result-view'),
    path('risk/results/hardware/', views.risk_result_view, name='dashboard-hardware-risk-result-view'),
    path('risk/results/software/', views.risk_result_view, name='dashboard-software-risk-result-view'),
    path('risk/results/user/', views.risk_result_view, name='dashboard-user-risk-result-view'),
    path('risk/tree/', views.risk_tree_view, name='dashboard-risk-tree-view'),
    path('risk/tree/data/', views.risk_tree_data, name='dashboard-risk-tree-data'),
    path('riskassessment/controls/<pk>/', views.risk_control_view, name='dashboard-risk-control-view'),
    path('user/survey/', views.survey, name='survey_questions'),
    path('user/survey/data/', views.survey_data_view, name='survey-data-view'),
    path('user/survey/save/', views.survey_data_save, name='survey-data-save'),
    path('user/survey/edit/', views.survey_answer_edit, name='survey_answer_edit'),
    path('user/survey/edit/save/', views.survey_new_data_save, name='survey_answer_save'),
    path('riskassessment/create_new_risk/', views.create_new_risk, name='create_new_risk'),
    path('riskassessment/change_active_status/', views.change_active_status, name='change_active_status'),



    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]


