from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.models import Group

from .forms import UserRegistrationForm, LoginUserForm

@login_required
@permission_required('users.add_user', raise_exception=True)
def regiser_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            group = form.cleaned_data['group']
            user.groups.add(group)
            return redirect('mainsite:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/create_employee.html', {'form': form})

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
