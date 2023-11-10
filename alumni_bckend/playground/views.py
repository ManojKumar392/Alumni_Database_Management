from django.shortcuts import render
from django.http import HttpResponse
from .models import Alumni, Batch
from django.db import connection , ProgrammingError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import NameForm
import re
from .forms import AlumniForm
from .models import JobOpening
from .forms import JobOpeningForm  
from django.utils import timezone
from .models import User
from .forms import LoginForm



def choose(request):
    return render(request, 'login_success.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            passkey = form.cleaned_data['passkey']
            
            user = User.objects.filter(password=password, passkey=passkey).first()

            if user:
                request.session['user_password'] = password
                return redirect('http://127.0.0.1:8000/playground/choose/')
            else:
                return HttpResponse("Invalid User")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def send_email(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'manoj2003r@gmail.com'  
            alumni = Alumni.objects.filter(First_name=first_name, Last_name=last_name).first()

            if alumni:
                recipient_email = alumni.email
                print(recipient_email)
                send_mail(subject, message, from_email, [recipient_email])
                return render(request, 'email_sent.html', {'email_sent': True})
            else:
                return render(request, 'email_sent.html', {'email_sent': False})

    else:
        form = NameForm()

    return render(request, 'email_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')


def query_form(request):
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        action = request.POST.get('action')
        user_password = request.session.get('user_password')
        user_password = user_password[6:8]
        if int(user_password) > 22:
            forbidden_keywords = ['INSERT', 'UPDATE', 'DELETE']

            if any(keyword in user_query.upper() for keyword in forbidden_keywords):
                return HttpResponse("You are not allowed to perform this operation.")

        try:
            if action == 'execute':
                with connection.cursor() as cursor:
                    cursor.execute(user_query)
                    results = cursor.fetchall()
                return render(request, 'query_result.html', {'results': results})
            elif action == 'download':
                with connection.cursor() as cursor:
                    cursor.execute(user_query)
                    results = cursor.fetchall()
                    if results:
                        columns = [desc[0] for desc in cursor.description]
                        csv_data = "\n".join([",".join(map(str, row)) for row in results])
                    else:
                        return render(request, 'no_result.html')
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="query_result.csv"'
                response.write(f"{','.join(columns)}\n{csv_data}")
                return response
        except ProgrammingError as e:
            error_message = f"Syntax error in the query: {str(e)}"
            return HttpResponse(error_message)
    else:
        return render(request, 'query_form.html')


def alumni_list(request):
    alumni = Alumni.objects.all()
    return render(request, 'alumni_list.html', {'alumni': alumni})

def alumni_create(request):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
            
    if request.method == 'POST':
        form = AlumniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
    else:
        form = AlumniForm()
    return render(request, 'alumni_form.html', {'form': form})

def alumni_update(request):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
    if request.method == 'POST':
        alumni_id = request.POST['Alumni_ID']
        alumni = Alumni.objects.filter(Alumni_ID=alumni_id).first()
        if alumni:
            form = AlumniForm(request.POST, instance=alumni)
            if form.is_valid():
                form.save()
                return redirect('alumni_list')
        else:
            return HttpResponse("The Alumni does not exist.")

    else:
        form = AlumniForm()

    return render(request, 'alumni_update.html', {'form': form})


def alumni_delete(request,first_name,last_name):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
    if request.method == 'POST':
        alumni = Alumni.objects.filter(First_name=first_name, Last_name=last_name).first()
        if alumni:
            alumni.delete()
            return redirect('alumni_list')
        else:
            return HttpResponse("The Alumni does not exist.")
    return render(request, 'alumni_confirm_delete.html', {'first_name':first_name , 'last_name':last_name})

def delete_alumni(request):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        return redirect('alumni_delete',first_name,last_name)
    return render(request, 'delete_alumni.html')


def list_tables(request):
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
    table_names = ['alumni', 'batch', 'degree', 'donations', 'work', 'publications']

    return render(request, 'list_tables.html', {'tables': tables, 'table_names': table_names})

def view_table(request, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

    context = {
        'table_name': table_name,
        'columns': columns,
        'data': data,
    }

    return render(request, 'view_table.html', context)

def job_openings(request):
    current_date = timezone.now().date()  

    job_listings = JobOpening.objects.select_related('alumni').filter(application_deadline__gte=current_date)

    return render(request, 'job_opening.html', {'job_listings': job_listings})


def add_job_opening(request):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_openings')
    else:
        form = JobOpeningForm()
    
    return render(request, 'add_job_opening.html', {'form': form})

def delete_job_opening(request, job_id):
    user_password = request.session.get('user_password')
    user_password = user_password[6:8]
    if int(user_password) < 22:
        return HttpResponse("You are not allowed to perform this operation.")
    job = JobOpening.objects.get(pk=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('job_openings')
    
    return render(request, 'delete_job_opening.html', {'job': job})

def call_stored_procedure(p_graduation_year):
    with connection.cursor() as cursor:
        cursor.callproc('GetAlumniByGraduationYear', [p_graduation_year])
        results = cursor.fetchall()
    return results


def alumni_by_graduation_year(request, graduation_year):
    alumni_list = call_stored_procedure(graduation_year)
    context = {'alumni_list': alumni_list, 'graduation_year': graduation_year}
    return render(request, 'procedure.html', context)
