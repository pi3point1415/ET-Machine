from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy

from .models import Settings, Discord
from .forms import *

import csv


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required
def FileListView(request):
    rushee_list = Rushee.objects.all()

    filings = []
    for i in rushee_list:
        filing = Filing.objects.filter(active_id=request.user.id, rushee_id=i.id)
        if len(filing) > 0:
            filings.append(filing[0].type)
        else:
            filings.append('x')

    initial = [
        {'type': i} for i in filings
    ]

    if request.method == 'POST':
        formset = FilingFormSet(request.POST)
        for i, form in enumerate(formset):
            if form.is_valid():
                type = form.cleaned_data['type']

                rushee = rushee_list[i]

                filings = Filing.objects.filter(active_id=request.user.id, rushee_id=rushee.id)
                for j in filings:
                    j.delete()

                active_file = [Filing(rushee=rushee, active=request.user, type=type)]
                active_file[0].save()

                initial[i] = {'type': type}

    formset = FilingFormSet(
        initial=initial
    )

    context = {
        'list': list(zip(rushee_list, formset)),
        'formset': formset
    }

    return render(request, 'rush/file_list.html', context)


@login_required
def RusheeListView(request):
    rushee_list = Rushee.objects.all()

    if request.method == 'POST':
        form = AddRusheesForm(request.POST)

        if form.is_valid():
            rushees = form.cleaned_data['rushees']
            for i in rushees.splitlines():
                if not Rushee.objects.filter(name__exact=i).exists():
                    rushee = Rushee(name=i)
                    rushee.save()

    form = AddRusheesForm()

    context = {
        'rushee_list': rushee_list,
        'form': form
    }

    return render(request, 'rush/rushee_list.html', context)


@login_required
def RusheeDetailView(request, pk):
    rushee = get_object_or_404(Rushee, pk=pk)
    active_file = Filing.objects.filter(active_id=request.user.id).filter(rushee_id=rushee.id)
    user_file = Filing.objects.filter(active_id=request.user.id).filter(rushee_id=rushee.id)
    if len(active_file) > 0:
        user_file = user_file[0].type
    else:
        user_file = 'x'

    user_file = {'type': user_file}

    if request.method == 'POST':
        if 'update' in request.POST:
            modify_form = ModifyRusheeForm(instance=rushee, data=request.POST)
            filing_form = FilingForm(initial=user_file)

            if modify_form.is_valid():
                for i in modify_form.cleaned_data.keys():
                    setattr(rushee, i, modify_form.cleaned_data[i])
                rushee.save()
        elif 'file' in request.POST:
            filing_form = FilingForm(request.POST)

            if filing_form.is_valid():
                type = filing_form.cleaned_data['type']
                for i in active_file:
                    i.delete()
                active_file = []
                if type != 'x':
                    active_file = [Filing(rushee=rushee, active=request.user, type=type)]
                    active_file[0].save()
        elif 'delete' in request.POST:
            filing_form = FilingForm(initial=user_file)
            delete_form = DeleteForm(request.POST)
            if delete_form.is_valid():
                if delete_form.cleaned_data['rushees']:
                    rushee.delete()
                    return redirect('rushee-list')
                if delete_form.cleaned_data['filings']:
                    filings = Filing.objects.all()
                    for i in filings:
                        if i.rushee == rushee:
                            i.delete()
        else:
            filing_form = FilingForm(initial=user_file)
    else:
        filing_form = FilingForm(initial=user_file)

    modify_form = ModifyRusheeForm(instance=rushee)
    delete_form = DeleteForm()

    if len(active_file) > 0:
        active_file = active_file[0].get_type_display()
    else:
        active_file = 'No Filing'

    context = {
        'rushee': rushee,
        'file_form': filing_form,
        'modify_form': modify_form,
        'active_file': active_file,
        'delete_form': delete_form,
    }

    return render(request, 'rush/rushee_detail.html', context)


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def ActiveListView(request):
    User = get_user_model()
    active_list = User.objects.all()

    if request.method == 'POST':
        new_actives_form = NewActiveForm(request.POST)
        modify_actives_form = ModifyActivesForm(active_list, request.user, request.POST)

        if new_actives_form.is_valid():
            actives = new_actives_form.cleaned_data['actives']
            for i in actives.splitlines():
                i = i.lower()
                User = get_user_model()
                if len(User.objects.filter(username=i)) == 0:
                    user = User.objects.create_user(i, '', i)
                    user.save()
        if modify_actives_form.is_valid():
            for i in modify_actives_form.cleaned_data.keys():
                if i.endswith('Staff'):
                    active = i[:-5]
                    User = get_user_model()
                    user = User.objects.filter(username=active)[0]
                    user.is_staff = modify_actives_form.cleaned_data[i]
                    user.save()
                elif i.endswith('Delete'):
                    if modify_actives_form.cleaned_data[i]:
                        active = i[:-6]
                        User = get_user_model()
                        user = User.objects.filter(username=active)[0]
                        user.delete()
                elif i.endswith('Password'):
                    if modify_actives_form.cleaned_data[i]:
                        active = i[:-8]
                        User = get_user_model()
                        user = User.objects.filter(username=active)[0]
                        user.set_password(user.username)
                        user.save()

    active_list = User.objects.all()
    active_list = sorted(active_list, key=lambda x: x.username.lower())
    new_actives_form = NewActiveForm()
    modify_actives_form = ModifyActivesForm(active_list, request.user)

    context = {
        'new_actives_form': new_actives_form,
        'modify_actives_form': modify_actives_form
    }

    return render(request, 'rush/active_list.html', context)


@login_required
def PasswordResetView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'rush/password_reset_complete.html')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, 'rush/password_reset.html', context)


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def MeetingListView(request):
    rushees = Rushee.objects.all()
    User = get_user_model()
    actives = User.objects.all()
    actives = sorted(actives, key=lambda x: x.username.lower())
    rows = []
    for i in rushees:
        row = []
        for j in actives:
            file = Filing.objects.filter(rushee=i, active=j)
            if len(file) > 0:
                row.append(file[0].type)
            else:
                row.append('')
        rows.append(row)

    actives = [list(i.username.upper()) for i in actives]

    context = {
        'rushees': zip(rushees, rows),
        'actives': actives,
    }

    return render(request, 'rush/meeting_list.html', context=context)


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def SettingsView(request):
    settings = Settings.objects.get(id=1)
    initial = {'b': settings.b, 'n': settings.n, 'w': settings.w, 'f': settings.f}

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST)
        delete_form = DeleteForm(request.POST)
        if settings_form.is_valid():
            data = (settings_form.cleaned_data['b'], settings_form.cleaned_data['n'],
                    settings_form.cleaned_data['w'], settings_form.cleaned_data['f'])
            data = ','.join([str(i) for i in data])
            settings.autobid = data
            settings.save()
        elif delete_form.is_valid():
            settings_form = SettingsForm(initial=initial)
            if delete_form.cleaned_data['rushees']:
                rushees = Rushee.objects.all()
                for i in rushees:
                    i.delete()
            if delete_form.cleaned_data['filings']:
                filings = Filing.objects.all()
                for i in filings:
                    i.delete()
        else:
            settings_form = SettingsForm(initial=initial)
    else:
        settings_form = SettingsForm(initial=initial)

    delete_form = DeleteForm()

    context = {
        'settings_form': settings_form,
        'delete_form': delete_form,
    }
    return render(request, 'rush/settings.html', context=context)


@login_required
def RusheeCSV(request):
    response = HttpResponse(content_type='text/csv',
                            headers={"Content-Disposition": 'attachment; filename="rushees.csv"'},)

    writer = csv.writer(response)
    rushees = Rushee.objects.all()
    writer.writerow(['Name', 'Status', 'Bidder', 'Dorm', 'Email', 'Discord', 'Phone', 'Comments'])
    for i in rushees:
        writer.writerow([i.name, i.get_status_display(), i.bidder, i.dorm, i.email, i.discord, i.phone, i.comments])

    return response


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def FileAsView(request):

    if request.method == 'POST':
        form = FileAsUserForm(request.POST)
        if form.is_valid():
            rushee = form.cleaned_data['rushee']
            active = form.cleaned_data['user']
            for i in Filing.objects.filter(rushee=rushee, active=active):
                i.delete()
            if form.cleaned_data['type'] != 'x':
                filing = Filing(rushee=rushee, active=active, type=form.cleaned_data['type'])
                filing.save()
    else:
        form = FileAsUserForm()

    context = {
        'form': form
    }

    return render(request, 'rush/file.html', context=context)


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def MergeView(request):
    if request.method == 'POST':
        form = MergeForm(request.POST)
        if form.is_valid():
            r1 = form.cleaned_data['r1']
            r2 = form.cleaned_data['r2']
            filings1 = Filing.objects.filter(rushee=r1)
            filings2 = Filing.objects.filter(rushee=r2)

            for i in filings2:
                if filings1.filter(active=i.active).exists():
                    i.delete()
                else:
                    i.rushee = r1
                    i.save()

            r2.delete()
    else:
        form = MergeForm()

    context = {
        'form': form
    }

    return render(request, 'rush/merge.html', context=context)


@login_required
def DiscordView(request):
    if request.method == 'POST':
        form = DiscordForm(request.POST)
        if form.is_valid():
            if 'submit' in request.POST:
                for i in Discord.objects.filter(user=request.user):
                    i.delete()
                Discord(user=request.user, id=form.cleaned_data['id']).save()
            elif 'unlink' in request.POST:
                for i in Discord.objects.filter(user=request.user):
                    i.delete()
                form = DiscordForm()
    else:
        discord_id = ''
        for i in Discord.objects.filter(user=request.user):
            discord_id = i.id
        form = DiscordForm(initial={'id': discord_id})

    context = {
        'form': form
    }

    return render(request, 'rush/discord_config.html', context=context)


@login_required
def DictionaryView(request):
    return render(request, 'rush/dictionary.html')


def SigninView(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            heard = form.cleaned_data['heard']
            signin = Signin(name=name, email=email, heard=heard)
            signin.save()
    form = SigninForm()

    context = {
        'form': form
    }
    return render(request, 'rush/signin.html', context=context)


@login_required
@staff_member_required(login_url=reverse_lazy('login'))
def SigninListView(request):
    signins = Signin.objects.all()

    context = {
        'signins': signins
    }
    return render(request, 'rush/signin-list.html', context=context)
