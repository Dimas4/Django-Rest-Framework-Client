from django.urls import path, re_path

from .views import get_companies, get_company, get_employee, get_employee_by_company_id


urlpatterns = [
    path('companies/', get_companies, name='get_companies'),
    re_path('^companies/(?P<id>\d+)$', get_company, name='one_company'),

    re_path('^employees/(?P<id>\d+)$', get_employee, name='one_employee'),

]
