import requests

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.conf import settings


def get_json(url):
    return requests.get(url).json()


def get_all_data(data):
    result = data.get('results')
    if not result:
        return
    while data['next']:
        dat_json = get_json(data['next'])
        result.extend(dat_json['results'])
    return result


def get_actual_page(data, page, row_per_page=5):
    paginator = Paginator(data, row_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data


def get_company(request, id):
    context = {}

    company = get_json(settings.API_URLS['company']+f'{id}')

    employees = get_json(company['company_employee'])
    data = get_all_data(employees)

    if data is None:
        context['employees'], context['company'] = None, company
        return render(request, "company/company.html", context=context)

    page = request.GET.get('page', 1)
    employees = get_actual_page(data, page)

    context['employees'], context['company'] = employees, company
    return render(request, "company/company.html", context=context)


def get_companies(request):
    context = {}

    companies = get_json(settings.API_URLS['company'])
    data = get_all_data(companies)

    if data is None:
        context['companies'] = None
        return render(request, "company/companies.html", context=context)

    page = request.GET.get('page', 1)
    companies = get_actual_page(data, page, 10)

    context['companies'] = companies
    return render(request, "company/companies.html", context=context)


def get_employee(request, id):
    context = {}
    employee = get_json(settings.API_URLS['employee']+f'{id}')

    salaries = get_json(settings.API_URLS['salary']+f'{id}')
    data = get_all_data(salaries)

    if data is None:
        context['employee'], context['salaries'] = employee, None
        return render(request, "employee/employee.html", context=context)

    page = request.GET.get('page', 1)
    salaries = get_actual_page(data, page)

    context['employee'], context['salaries'] = employee, salaries
    return render(request, "employee/employee.html", context=context)
