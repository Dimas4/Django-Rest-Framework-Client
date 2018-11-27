import requests

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render


def get_company(request, id):
    context = {}
    company = requests.get(f"http://127.0.0.1:8000/api/company/{id}").json()

    employees = requests.get(company['company_employee']).json()
    data = employees['results']

    while employees['next']:
        employees = requests.get(employees['next']).json()
        data.extend(employees['results'])

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    context['employees'] = employees
    context['company'] = company
    return render(request, "company/company.html", context=context)


def get_companies(request):
    context = {}

    companies = requests.get("http://127.0.0.1:8000/api/company/").json()
    data = companies['results']

    while companies['next']:
        companies = requests.get(companies['next']).json()
        data.extend(companies['results'])

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    context['companies'] = companies
    return render(request, "company/companies.html", context=context)


def get_employee_by_company_id(request, id):
    pass


def get_employee(request, id):
    context = {}
    employee = requests.get(f"http://127.0.0.1:8000/api/employee/{id}").json()
    context['employee'] = employee
    return render(request, "employee/employee.html", context=context)

