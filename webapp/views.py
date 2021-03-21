from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import user_admin, user_client, lead_sources, lead_status, create_lead, Customer
from .forms import Admin_Profile, Client_Profile, lead_sources_form, lead_status_form, create_lead_form, \
    update_lead_form_without_status, lead_history_form, CustomerForm
import csv
import json
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .filters import LeadFilters
import requests

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def webhook_example(request):
    return HttpResponse('Hello, world. This is the webhook response.')


def home_requests(request):
    # response = requests.get("https://api.covid19api.com/countries").json()
    response = requests.get('https://www.yodiso.com/comp-kec5fc5hinlineContent')
    # response = requests.get('https://www.google.com/')
    return render(request, 'request.html', {'response': response})


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def input_animation(request):
    return render(request, 'input_animation.html')


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'webapp/authentication/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'webapp/authentication/logout.html')


def notifications(request):
    return render(request, 'webapp/notification.html')


@login_required(login_url='/login')
def super_admin_dashboard(request):
    admin_count = user_admin.objects.all()
    # data = user_admin.objects.raw("SELECT * FROM user_admin_user.username WHERE lead_id=1")
    # print(data)
    lead_data = create_lead.objects.filter(lead_assign=request.user.id - 1)
    # client_count = user_client.objects.count()
    lead_count = create_lead.objects.count()
    # count = admin_count + client_count
    context = {
        # 'count': count,
        'admin_count': len(admin_count),
        # 'client_count': client_count,
        'lead_count': lead_count,
        'lead_data': len(lead_data),
    }
    return render(request, 'webapp/dashboard.html', context)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def lead_source_create_form(request):
    if request.method == 'POST':
        form = lead_sources_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_source_view')
    else:
        form = lead_sources_form()
    return render(request, 'webapp/lead_source/lead_source_create_form.html', {'form': form})


def lead_source_view(request):
    lead_source_data = lead_sources.objects.all()
    lead_count = create_lead.objects.values('lead_sour').annotate(Count('lead_sour_id'))
    return render(request, 'webapp/lead_source/lead_sources.html',
                  {'lead_data': lead_source_data, 'count': len(lead_source_data), 'lead_count': len(lead_count)})


def lead_source_update_form(request, id):
    if request.method == 'POST':
        lead_source_update = lead_sources.objects.get(source_id=id)
        form = lead_sources_form(request.POST, instance=lead_source_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_source_view')
    else:
        lead_source_update = lead_sources.objects.get(source_id=id)
        form = lead_sources_form(instance=lead_source_update)
    return render(request, 'webapp/lead_source/lead_source_update_form.html', {'form': form})


def lead_source_delete(request, id):
    if request.method == 'POST':
        dl = lead_sources.objects.get(source_id=id)
        dl.delete()
        return HttpResponseRedirect('/lead_source_view')


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def lead_status_create_form(request):
    if request.method == 'POST':
        form = lead_status_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_status_view')
    else:
        form = lead_status_form()
    return render(request, 'webapp/lead_status/lead_status_create.html', {'form': form})


# def lead_status_create_form(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         bcolor = request.POST['bcolor']
#         tcolor = request.POST['tcolor']
#         c = lead_status(name=name, background_color=bcolor, text_color=tcolor)
#         c.save()
#         return HttpResponseRedirect('/lead_status_view')
#     return render(request, 'webapp/lead_status/lead_status_create_form.html')


def lead_status_view(request):
    lead_status_data = lead_status.objects.all().order_by('status_id')
    return render(request, 'webapp/lead_status/lead_status.html',
                  {'lead_data': lead_status_data, 'count': len(lead_status_data)})


def change_status(request):
    context = {}
    error = True
    message = 'Something went wrong'
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        load_status_obj = lead_status.objects.filter(status_id=object_id).first()
        if load_status_obj:
            if load_status_obj.status == '1':
                load_status_obj.status = '2'
            else:
                load_status_obj.status = '1'
            load_status_obj.save()
            error = False
            message = 'Ok'
    context['error'] = error
    context['message'] = message
    return HttpResponse(json.dumps(context))


def lead_status_update_form(request, id):
    if request.method == 'POST':
        lead_status_update = lead_status.objects.get(status_id=id)
        form = lead_status_form(request.POST, instance=lead_status_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_status_view')
    else:
        lead_status_update = lead_status.objects.get(status_id=id)
        form = lead_status_form(instance=lead_status_update)
    return render(request, 'webapp/lead_status/lead_status_update_form.html', {'form': form})


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from django import forms


def admin_user_create_form(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        mob = request.POST['mobile']
        img = request.FILES['image']
        em = request.POST['email']
        pwd = request.POST['pwd']
        usr = User.objects.create_user(uname, em, pwd)
        usr.is_staff = True
        usr.save()
        au = user_admin(user=usr, mobile=mob, image=img)
        au.save()
        return HttpResponseRedirect('/admin_client_user_view/')
    message = 'Your Account has been created Successfully.'
    return render(request, 'webapp/admin_client/admin_user_create_form.html', {'message': message})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'webapp/admin_client/admin_client_change_password_form.html', {'form': form})


# def admin_user_update_form(request, id):
#     if request.method == 'POST':
#         admin_update = user_admin.objects.get(admin_id=id)
#         form = admin_update_form(request.POST, instance=admin_update)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/admin_client_user_view/')
#     else:
#         admin_update = user_admin.objects.get(admin_id=id)
#         form = admin_update_form(instance=admin_update)
#     return render(request, 'webapp/admin_client/admin_user_update_form.html', {'form': form})


def admin_profile(request):
    context = {}
    check = user_admin.objects.filter(user=request.user.id)
    print(check, len(check))
    if len(check) > 0:
        profile = user_admin.objects.get(user=request.user.id)
        if request.method == 'POST':
            form = Admin_Profile(request.POST, request.FILES, instance=profile)
            context['form'] = form
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        else:
            form = Admin_Profile(instance=profile)
            context['form'] = form
    return render(request, 'webapp/admin_client/admin_profile.html', context)


# def admin_profile(request):
#     context = {}
#     check = user_admin.objects.filter(user=request.user.id)
#     print(check, len(check))
#     if len(check) > 1:
#         profile = user_admin.objects.get(user=request.user.id)
#         if request.method == 'POST':
#             form = Admin_Profile(request.POST, request.FILES, instance=profile)
#             if form.is_valid():
#                 form.save()
#             else:
#                 print(form.errors)
#         else:
#             form = Admin_Profile(instance=profile)
#         context['form'] = form
#     return render(request, 'webapp/admin_client/admin_profile.html', context)


def admin_client_user_view(request):
    admin_data = user_admin.objects.all()
    client_data = user_client.objects.all()
    count = len(admin_data) + len(client_data)
    context = {
        'admin_data': admin_data,
        'client_data': client_data,
        'count': count,
    }
    return render(request, 'webapp/admin_client/admin_client_user_view.html', context)


def admin_user_data(request):
    admin_data = user_admin.objects.all()
    admin_count = len(admin_data)
    return render(request, 'webapp/admin_client/admin_user_data.html',
                  {'count': admin_count, 'admin_data': admin_data})


def delete_admin_data(request, id):
    dl = user_admin.objects.get(admin_id=id)
    dl.delete()
    return HttpResponseRedirect('/admin_client_user_view/')


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def client_user_create_form(request):
    c_user = user_admin.objects.all()
    if request.method == 'POST':
        uname = request.POST['uname']
        mob = request.POST['mobile']
        img = request.FILES['image']
        em = request.POST['email']
        pwd = request.POST['pwd']
        parent = request.POST['parent']
        usr = User.objects.create_user(uname, em, pwd)
        usr.save()
        usr.is_staff = True
        au = user_client(user=usr, mobile=mob, image=img, parent=parent)
        au.save()
        return HttpResponseRedirect('/admin_client_user_view/')
    return render(request, 'webapp/admin_client/client_user_create_form.html', {'c_user': c_user})


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# from django.views.generic.edit import UpdateView
# class Lead_Status_Update(UpdateView):
#     model = create_lead
#     template_name = 'webapp/lead_view/lead_history_form.html'
#     form_class = lead_history_form
#     success_url = '/lead_view'


def lead_view(request):
    current_user = request.user
    lead_data = create_lead.objects.filter(lead_assign=current_user.id - 1)
    # lead_data = create_lead.objects.all()
    # lead_data = create_lead.objects.filter(lead_id__id=request.user.id)

    # for i in create_lead.objects.all():
    #     print(i.lead_stat)
    # for p in create_lead.objects.raw(
    #         'SELECT lead_id, count(lead_id) FROM webapp_create_lead WHERE lead_sour_id = 2 GROUP BY lead_id;'):
    #     print(p.lead_sour)

    # query = "SELECT lead_id, count(lead_id) FROM webapp_create_lead WHERE lead_sour_id = 1 GROUP BY lead_id;"

    p = Paginator(lead_data, per_page=10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(p.num_pages)
    if request.user.is_superuser:
        lead_data = create_lead.objects.all()
        p = Paginator(lead_data, per_page=10)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(p.num_pages)
    lead_status_name = lead_status.objects.all()
    lead_source_name = lead_sources.objects.all()
    lead_status_data = lead_status.objects.all()

    lead_status_count = lead_status.objects.all().count()
    lead_source_count = lead_sources.objects.all().count()

    google = create_lead.objects.all().filter(lead_sour=1)
    facebook = create_lead.objects.all().filter(lead_sour=2)
    instagram = create_lead.objects.all().filter(lead_sour=3)
    whatsapp = create_lead.objects.all().filter(lead_sour=4)
    twitter = create_lead.objects.all().filter(lead_sour=5)

    new = create_lead.objects.all().filter(lead_stat=1)
    won = create_lead.objects.all().filter(lead_stat=2)
    inprogress = create_lead.objects.all().filter(lead_stat=3)
    lost = create_lead.objects.all().filter(lead_stat=4)
    noresponse = create_lead.objects.all().filter(lead_stat=5)

    # source_count = 0
    # for i in source:
    #     source_count += 1
    # status = create_lead.objects.values('lead_stat')
    # status_count = 0
    # for i in status:
    #     status_count += 1

    myFilter = LeadFilters(request.GET, queryset=lead_data)
    lead_data = myFilter.queryset

    context = {
        'lead_data': page,
        'count': len(lead_data),
        'lead_status_name': lead_status_name,
        'lead_status_count': lead_status_count,
        'lead_source_count': lead_source_count,
        'lead_source_name': lead_source_name,
        'lead_status_data': lead_status_data,
        # 'source_count': source_count,
        # 'status_count': status_count,
        'p': p,
        'google': len(google),
        'facebook': len(facebook),
        'instagram': len(instagram),
        'whatsapp': len(whatsapp),
        'twitter': len(twitter),
        'page_num': int(page_num),
        'myFilter': myFilter,
        'new': len(new),
        'won': len(won),
        'inprogress': len(inprogress),
        'lost': len(lost),
        'noresponse': len(noresponse),
    }
    return render(request, 'webapp/lead_view/lead_view.html', context)


# def lead_view(request):
#     current_user = request.user
#     lead_data = create_lead.objects.filter(lead_assign=current_user.id - 1)
#     lead_data = create_lead.objects.all()
#     myFilter = LeadFilters(request.GET, queryset=lead_data)
#     lead_data = myFilter.qs
#     context = {
#         'lead_data': lead_data,
#         'myFilter': myFilter
#     }
#     return render(request, 'webapp/lead_view/lead_view.html', context)


def lead_create_form(request):
    if request.method == 'POST':
        form = create_lead_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_view')
    else:
        form = create_lead_form()
    return render(request, 'webapp/lead_view/lead_create_form.html', {'form': form})


def lead_update_form(request, id):
    if request.method == 'POST':
        lead_update = create_lead.objects.get(lead_id=id)
        form = update_lead_form_without_status(request.POST, instance=lead_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lead_view')
    else:
        lead_update = create_lead.objects.get(lead_id=id)
        form = update_lead_form_without_status(instance=lead_update)
    return render(request, 'webapp/lead_view/lead_update_form.html', {'form': form})


def lead_history_form_view(request, id):
    lead_stata = lead_status.objects.all()
    if request.method == 'POST':
        lead_history = create_lead.objects.get(lead_id=id)
        form = lead_history_form(request.POST, instance=lead_history)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/lead_history_eye_data/{id}')
    else:
        lead_history = create_lead.objects.get(lead_id=id)
        form = lead_history_form(request.POST, instance=lead_history)
    return render(request, 'webapp/lead_view/lead_history_form.html',
                  {'form': form, 'l_h': lead_history, 'lead_stata': lead_stata})


#
# lead_stat = lead_status.objects.all()
#     if request.method == 'POST':
#         lead_stat_f = request.POST['lead_status_field']
#         f_date = request.POST['follow_up']
#         rm = request.POST['remark_text']
#         lhs = create_lead(lead_stat=lead_stat_f, follow_up_date=f_date, remark=rm)
#         lhs.save()
#         return HttpResponseRedirect(f'/lead_history_eye_data/{id}')


def lead_history_eye_data(request, id):
    if request.method == 'POST':
        lead_history = create_lead.objects.get(lead_id=id)
        form = lead_history_form(request.POST, instance=lead_history)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/lead_history_eye_data/{id}')
    else:
        lead_history = create_lead.objects.get(lead_id=id)
        form = lead_history_form(request.POST, instance=lead_history)
    return render(request, 'webapp/lead_view/lead_history_eye_data.html', {'l_h': lead_history, 'form': form})


# def lead_history_pagination(request):
#     lead_history = create_lead.objects.all()
#     p = Paginator(lead_history, 2)
#     page_num = request.GET.get('page', 1)
#     try:
#         page = p.page(page_num)
#     except EmptyPage:
#         page = p.page(1)
#     return render(request, 'webapp/lead_view/lead_history_eye_data.html', {'l_h': page})


# from django.views.generic import ListView
#
#
# class PaginationView(ListView):
#     paginate_by = 2
#     model = create_lead
#     template_name = 'webapp/lead_view/lead_view.html'
#     context_object_name = 'pagination'


def lead_delete(request, id):
    if request.method == 'POST':
        dl = create_lead.objects.get(lead_id=id)
        dl.delete()
        return HttpResponseRedirect('/lead_view')


def export_lead_excel_sheet_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lead_excel.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Name', 'Query', 'Mobile', 'Email', 'Source', 'Status', 'User', 'Description', 'Created On', 'Last Login'])

    excel_sheet_data = create_lead.objects.all().values_list('name', 'query', 'mobile', 'email', 'lead_sour',
                                                             'lead_stat', 'lead_assign', 'description', 'created',
                                                             'updated')
    for data in excel_sheet_data:
        writer.writerow(data)

    return response


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def customer_form(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        company = request.POST['company']
        gst = request.POST['gst']
        email = request.POST['email']
        phone = request.POST['phone']
        website = request.POST['website']
        position = request.POST['position']
        country = request.POST['country']
        city = request.POST['city']
        address = request.POST['address']
        contact = request.POST['contact']
        cust = Customer(firstname=fname, lastname=lname, email=email, phone=phone, website=website, position=position,
                        company=company, gst_number=gst, country=country, city=city, address=address, contact=contact)
        cust.save()
        return redirect('/customer_data')
    return render(request, 'webapp/Customer/customer_form.html')


# def customer_form(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = CustomerForm()
#     return render(request, 'customer_form.html', {'form': form})


def customer_data(request):
    data = Customer.objects.all().order_by('-id')
    return render(request, 'webapp/Customer/customer_data.html', {'data': data})


def delete_customer_data(request, id):
    dl = Customer.objects.get(pk=id)
    dl.delete()
    return HttpResponseRedirect('/customer_data/')


def customer_eye_data(request, id):
    data = Customer.objects.get(pk=id)
    return render(request, 'webapp/Customer/customer_eye_data.html', {'data': data})


def customer_update_form(request, id):
    if request.method == 'POST':
        customer_update = Customer.objects.get(pk=id)
        form = CustomerForm(request.POST, instance=customer_update)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/customer_data')
    else:
        customer_update = Customer.objects.get(pk=id)
        form = CustomerForm(instance=customer_update)
    return render(request, 'webapp/Customer/customer_update_form.html', {'form': form})

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
