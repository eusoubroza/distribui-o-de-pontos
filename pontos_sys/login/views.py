from django.shortcuts import render, redirect, get_object_or_404
from ldap3 import Server, Connection, ALL
from flask import Flask, render_template, request, jsonify
from django.contrib.auth import login, authenticate, admin
from django.contrib.auth.models import User
from .forms import RegistrationForm, TransactionForm, RequestForm
from .models import CustomUser, Transaction, Requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv
from django.http import HttpResponse
from django.http import JsonResponse
import sweetify
import time

def my_view(request):
    # Your view logic here
    sweetify.info(request, 'Message sent', button='Ok', timer=3000)
    return redirect(request.path, {'user': user, 'transactions': transactions, 'userr': userr})



def process(request):
    data_not_null = 0
    show_alert = False
    show_alert_mail_exists = False
    
    if request.method == 'POST' and request.POST.get('submit-button') == 'clicked':
        print("oi")
        email = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_id = request.session.get('user_id')
            """ user_email = request.session[user.email]  """
            login(request, user)
            return redirect('account')
        else:
            show_alert = True
            return render(request, 'pages/newhtml.html', {'show_alert': show_alert})
    
    else:
    
        # Handle other HTTP methods like GET, if needed
        # For example, render a template for the initial form display
        return render(request, 'pages/newhtml.html')
    


def check_ad(login):
    
    # Replace 'your_domain_controller' with the hostname or IP address of your Active Directory server
    server = Server('DC901.sysmexamerica.com', get_info=ALL)
    conn = Connection(server, user="", password="", auto_bind=True)

    # Replace 'your_base_dn' with the base Distinguished Name (DN) where you want to start the search
    base_dn = 'ou=brazil,ou=latam,ou=user,ou=company,dc=sysmexamerica,dc=com'

    # Replace 'your_filter' with the LDAP filter to specify the search criteria (e.g., '(objectClass=user)')
    """ search_filter = '(objectClass=user)' """

    search_filter = f'(mail={login})'

    

    # Replace 'your_attributes' with a list of attributes you want to retrieve (e.g., ['cn', 'mail'])
    attributes = ['mail', 'cn', 'department']

    # Perform the LDAP search
    conn.search(base_dn, search_filter, attributes=attributes)
    num = 0
    # Access the search results
    if len(conn.entries) > 0:
        print(f"The email address '{login}' exists in the Active Directory.")
        mail_exists = True
        # Access additional attributes of the entry if needed
        for entry in conn.entries:
            print(f"Name: {entry.mail.value}")
            
            cc_complete = entry.department.value
            cc = ''.join([char for char in cc_complete if char.isdigit()])
            
    else:
        print(f"The email address '{login}' is not found in the Active Directory.")
        mail_exists = False
        cc = ""
        
    conn.unbind()

    return mail_exists, cc



@login_required
def test(request):
    listt = []
    transacoes = 0
    email = request.user.email
    print(email)
    user = request.user
    transactions = Transaction.objects.all()
    for transaction in transactions:
        if transaction.reciever.cc == user.cc:
            transacoes += 1
            listt.append(transaction.sender.cc)
    print(listt)

    data = [
        ('2311000060', 'Production'),
        ('2311100060', 'Quality Control'),
        ('2311200060', 'Industrial Maintenance'),
        ('2311300060', 'Management Production Support'),
        ('2311400060', 'Internal Warehouse'),
        ('2312000050', 'Finance e Controlling'),
        ('2312110050', 'Finance e Operations  Bright Project'),
        ('2319000050', 'LA Affiliates'),
        ('2312900050', 'Customer Operations'),
        ('2312100050', 'Human Resources'),
        ('2312400050', 'Administrative  SJP'),
        ('2312500050', 'Administrative  SP'),
        ('2312200050', 'General Manager'),
        ('2312300050', 'Information Technology'),
        ('2312600050', 'Maintenance Facilities'),
        ('2312130050', 'Legal Department'),
        ('2313000040', 'Marketing'),
        ('2313100010', 'Marketing Communication e Events SBR'),
        ('2313200010', 'SBR Urinalysis Marketing'),
        ('2314000011', 'SBR Technical Consultants'),
        ('2314600011', 'Customer Care Operations  SBR'),
        ('2318300010', 'SBR Training Center'),
        ('2314100011', 'SBR Scientific & Application Service'),
        ('2314300011', 'SBR Direct Sales CAS Clinical Application Specialist'),
        ('2314200011', 'SBR Field Service Representatives'),
        ('2314400011', 'SBR Technical Assistance Center TAC'),
        ('2315000020', 'Logistics SBR'),
        ('2315100020', 'Logistics SLA'),
        ('2315550020', 'Logistic  Bright Project'),
        ('2315200020', 'Purchasing'),
        ('2315300020', 'Operations Director'),
        ('2315400020', 'Operations Support'),
        ('2316000050', 'Regulatory Affairs'),
        ('2316100050', 'Quality Assurance'),
        ('2316200050', 'Compliance'),
        ('2317000050', 'Business Planning'),
        ('2318000010', 'Sales'),
        ('2318100010', 'SBR Sales Distribution'),
        ('2318200010', 'SBR Hematology Marketing'),
        ('2312800050', 'IT Data Center'),
        ('2318400010', 'Sales Operations  SBR'),
        ('2330000050', 'Global Opportunity for Local Development')
    ]
    
    wedgeprops = {'linewidth': 10, 'edgecolor': 'none'}
    unique_ids_in_data = set(item[1] for item in data)
    
    id_counts = {}

    for id in listt:
        for num, sect in data:
            if id == num:
                if sect in id_counts:
                    id_counts[sect] += 1
                else:
                    id_counts[sect] = 1 
    ids = id_counts

    labels = list(ids.keys())
    sizes = list(ids.values())

    def autopct_format(pct, total):
        absolute = int(pct/100.*total)
        return f'{pct:.1f}% ({absolute:d})'

    # Create the pie chart with custom settings
    plt.figure(figsize=(5, 5))  # Set the figure size as needed
    plt.pie(sizes, labels=labels, autopct=lambda pct: autopct_format(pct, sum(sizes)), startangle=140, wedgeprops=wedgeprops)  # Adjust labeldistance for more space

    # Increase the font size of labels
    plt.rcParams['font.size'] = 14  # Increase the font size for larger labels

    plt.title('reconhecimentos feitos por outros setores')
    

    # Save the chart with a larger size
    fig = plt.gcf()
    fig.set_size_inches(9, 9)  # Set the desired size in inches
    plt.savefig('chart.png', format='png', bbox_inches='tight')  # Save the chart with a larger size

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return render(request, 'pages/account.html', {'transactions' : transactions, 'user' : user, 'setor_externo' : transacoes, 'lista' : listt, "ids" : ids, 'chart_data' : chart_data})

def register(request):
    show_alert = False
    show_alert_mail_exists = False
    if request.method == 'POST' and request.POST.get('submit_button') == 'clicked':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            mail_exists, _ = check_ad(email)
            if mail_exists == True:
                user = form.save(commit=False)  # Create a model instance from form data
                password = form.cleaned_data['password']  # Get the password from form data
                user.set_password(password)  # Set and hash the password
                user.points = 0
                _, user.cc = check_ad(email)
                if user.cc == "2312100050":
                    user.is_rh = True
                user.save()  # Save the user instance to the database
                return redirect('index')  # Redirect to the login page after successful registration
            elif mail_exists == False:
                show_alert_mail_exists = True
                return redirect(request.path, {'show_alert_mail_exists': show_alert_mail_exists, 'form': form})
        else:
            show_alert = True
            return redirect(request.path, 'pages/register.html', {'show_alert': show_alert, 'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'pages/register.html', {'form': form})

@login_required
def points(request):
    user_id = request.session.get('user.id')
    user_email = request.session.get('user.email')
    user_logged = request.user
    users = CustomUser.objects.all() 
    return render(request, 'pages/points_board.html', {'users' : users, 'user_logged' : user_logged})

@login_required
def my_points(request):
    popup = None
    userr = request.user.id
    user = request.user
    transactions = Transaction.objects.all()
    name = request.POST.get('submit button')
    exists = Requests.objects.filter(requester=user, status=True).exists()
    if request.method == 'POST' and request.POST.get('submit_button') == 'clicked' and not exists:
        popup = True
        form = RequestForm()
        requisition = form.save(commit=False)
        requisition.requester = user
        requisition.status = True
        requisition.quantidade = user.points
        requisition.save()
        return render(request, 'pages/my_points.html', {'popup': popup, 'user' : user, 'transactions' : transactions, 'userr' : userr})
    else:
        popup = False
        return render(request, 'pages/my_points.html', {'popup': popup, 'user' : user, 'transactions' : transactions, 'userr' : userr})


@login_required
def create_transaction(request):
    input_value1 = ""
    input_value = ""
    request.POST.get('submit_button') == 'clicked'
    
    transactions = Transaction.objects.all()
    user = request.user
    users = CustomUser.objects.exclude(email=request.user.email)
    if request.method == 'POST' and request.POST.get('submit_button') == 'clicked':
        form = TransactionForm(request.POST, users=users)
        reciever = request.POST.get('input_field_name')
        if users.filter(email=reciever).exists():
            input_value1 = request.POST.get('input_field_name')
            input_value = CustomUser.objects.get(email=input_value1)
            description = request.POST.get('description')
            amount = request.POST.get('amount')
            request_user = request.user
            if form.is_valid() and request_user != input_value and int(amount) <= user.manager_points:
                form = TransactionForm(request.POST, users=users)
                transactions = Transaction.objects.all()
                user.manager_points = user.manager_points - int(amount)
                transaction = form.save(commit=False)
                transaction.sender = request_user
                transaction.reciever = CustomUser.objects.get(email=input_value)
                transaction.amount = int(amount)
                transaction.description = description
                user.save()
                transaction.save()
                return redirect(request.path, {'form': form, 'users' : users, 'transactions' : transactions, 'user' : user})
            else:
                return redirect(request.path, {'form': form, 'users' : users, 'transactions' : transactions, 'user' : user})
    else:
        print("CARAU2")
        form = TransactionForm(request.POST, users=users)
        users = CustomUser.objects.exclude(email=request.user.email)

    return render(request,  'pages/gv_points.html',{'form': form, 'users': users, 'transactions' : transactions, 'user' : user})

@login_required
def requisicoes(request):
    requests = Requests.objects.all()
    users = CustomUser.objects.all()
    if request.method == 'POST':
        if request.POST.get('submit_button') == 'clicked':
            requests = Requests.objects.all()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

            writer = csv.writer(response, delimiter=';')  # Specify the delimiter as ';'

            # Write header row
            writer.writerow(['ID', 'Date', 'requisitante', 'status'])

            # Fetch data from the Transaction model
           

            # Write data rows
            for request in requests:
                status = ""
                if request.status == False:
                    status = "Fechado"
                else:
                    status = "Aberto"
                formatted_timestamp = request.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([request.id, formatted_timestamp, request.requester, status])
            return response   
            
        if 'close_request' in request.POST:
            request_id = request.POST['close_request']
            request1 = Requests.objects.get(id=request_id)
            request1.status = 0
            request1.save()
            for user in users:
                if request1.requester_id == user.id:
                    user.points = 0
                    user.save()
         


    return render(request, 'pages/requisições.html', {'requests' : requests})
