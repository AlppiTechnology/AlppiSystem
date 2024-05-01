from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.register.campus import view as campus_view
from apps.register.employee import view as employee_view
from apps.register.student import view as student_view
from apps.register.groups import view as groups_view
from apps.register.city import view as city_viewset
# from apps.register.federative_unit import viewsets as federativeunitviewstes



urlpatterns = [
    path('campus/<int:pk>/', campus_view.CampusView.as_view(), name='select_edit_delete_campus'),
    path('campus/<int:pk>/update/', campus_view.UpdateCampusView.as_view(), name='select_edit_delete_campus'),
    path('campus/<int:pk>/delete/', campus_view.DeleteCampusView.as_view(), name='select_edit_delete_campus'),
    path('campus/list/', campus_view.ListCampusView.as_view(), name='list_campus'),
    path('campus/create/', campus_view.CreateCampusView.as_view(), name='create_campus'),

    path('employee/<int:pk>/', employee_view.EmployeeView.as_view(), name='select_employee'),
    path('employee/<int:pk>/update/', employee_view.UpdateEmployeeView.as_view(), name='update_employee'),
    path('employee/<int:pk>/delete/', employee_view.DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employee/<int:pk>/changestatus/', employee_view.ChangeStatusEmployeeView.as_view(), name='change_employee_status'),
    path('employee/list/', employee_view.ListEmployeeView.as_view(), name='list_employee'),
    path('employee/create/', employee_view.CreateEmployeeView.as_view(), name='create_employee'),

    path('student/<int:pk>/', student_view.StudentView.as_view(), name='select_student'),
    path('student/<int:pk>/update/', student_view.UpdateStudentView.as_view(), name='update_student'),
    path('student/<int:pk>/delete/', student_view.DeleteStudentView.as_view(), name='delete_student'),
    path('student/<int:pk>/changestatus/', student_view.ChangeStatusStudentView.as_view(), name='change_student_status'),
    path('student/list/', student_view.ListStudentView.as_view(), name='list_student'),
    path('student/create/', student_view.CreateStudentView.as_view(), name='create_student'),


    path('groups/', groups_view.GroupsView.as_view(), name='select_edit_delete_group'),
    path('groups/create/', groups_view.CreateGroupsView.as_view(), name='create_groups'),


    path('city/', city_viewset.SerachCityView.as_view(), name='search_city'),

    # path('uf/all/', federativeunitviewstes.FederativeUnitAllViewSet.as_view(), name='list_all_uf'),
    # path('uf/search/', federativeunitviewstes.FederativeUnitSearchViewSet.as_view(), name='search_uf'),
]



urlpatterns = format_suffix_patterns(urlpatterns)
