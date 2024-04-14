from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auths_views
from django.urls import reverse_lazy
from .models import Relation


# Create your views here.

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'User created successfully', 'success')
            return redirect('home:home')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    templates_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(self,request,*args,**kwargs)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.templates_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                if self.next :
                    return redirect(self.next)
                return redirect('home:home')

            messages.error(request, 'user or pass is wrong', 'warning')
        return render(request, self.templates_name, {'form': self.form_class})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if_following = False
        user = get_object_or_404(User, pk=user_id)
        post = user.posts.all()
        relation = Relation.objects.filter(from_user = request.user , to_user=user)
        if relation.exists():
            if_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': post,'is_following':if_following})


class UserPasswordResetView(auths_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auths_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordConfirmView(auths_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auths_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request,'you are already following this user','danger')
        else :
            Relation(from_user = request.user,to_user = user).save()
            messages.success(request,'you followed this user','success')
        return redirect('account:user_profile', user.id )


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else :
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('account:user_profile', user.id )