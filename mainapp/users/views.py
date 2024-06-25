from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.models import Group

from .forms import UserRegistrationForm, LoginUserForm, UserUpdateForm, ProfileUpdateForm
from .models import Review


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


class UsersListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/users-list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return get_user_model().objects.filter(groups=1)


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['user'] = get_object_or_404(get_user_model(), username=self.kwargs['username'])
            return context


class UserReviewsView(ListView):
    template_name = 'users/reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(get_user_model(), username=username)
        return Review.objects.filter(employee=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return context


class ReviewCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'content']
    template_name = 'users/create_review.html'
    permission_required = 'users.add_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return context

    def form_valid(self, form):
        form.instance.employee = self.get_context_data()['employee']
        return super().form_valid(form)


class UserDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:users-list')
    permission_required = 'users.add_user'
    raise_exception = True
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm  # Additional form for Profile
    template_name = 'users/profile_update.html'  # Create this template

    def get_object(self, queryset=None):
        if self.request.user.has_perm('users.change_user'):
            return get_user_model().objects.get(username=self.kwargs['username'])
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form_class(instance=self.object.profile)
        return context

    def form_valid(self, form):
        profile_form = self.profile_form_class(self.request.POST, self.request.FILES, instance=self.object.profile)
        if profile_form.is_valid():
            profile_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.object.username})


def handle_permission_denied(request, exception):
    return render(request, 'mainsite/permission_denied.html', status=403)
