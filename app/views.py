import requests

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.conf import settings


def get_json(url):
    return requests.get(url).json()


def get_all_data(data):
    result = data['results']
    while data['next']:
        dat_json = get_json(data['next'])
        result.extend(dat_json['results'])
    return result


def get_actual_page(data, page, row_per_page=5):
    paginator = Paginator(data, row_per_page)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    return employees


def get_company(request, id):
    context = {}
    company = get_json(f"{settings.BASE_API_URL}api/company/{id}")

    employees = get_json(company['company_employee'])
    data = get_all_data(employees)
    page = request.GET.get('page', 1)
    employees = get_actual_page(data, page)

    context['employees'] = employees
    context['company'] = company
    return render(request, "company/company.html", context=context)


def get_companies(request):
    context = {}

    companies = get_json(f"{settings.BASE_API_URL}api/company/")
    data = get_all_data(companies)

    page = request.GET.get('page', 1)
    companies = get_actual_page(data, page, 10)

    context['companies'] = companies
    return render(request, "company/companies.html", context=context)


def get_employee(request, id):
    context = {}
    employee = get_json(f"{settings.BASE_API_URL}api/employee/{id}")

    salaries = get_json(f"{settings.BASE_API_URL}api/salary/{id}")
    data = get_all_data(salaries)

    page = request.GET.get('page', 1)
    salaries = get_actual_page(data, page)

    context['employee'] = employee
    context['salaries'] = salaries
    return render(request, "employee/employee.html", context=context)
