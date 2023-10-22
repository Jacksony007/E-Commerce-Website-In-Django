from django.shortcuts import render, redirect
from django.contrib import messages
from E_Commerce_App.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.shortcuts import render


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Replace 'home' with the name of your home page URL pattern
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    # Replace 'login' with the appropriate URL name for your login page URL pattern
    return redirect('login_view')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken.')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered.')
            else:
                user = CustomUser.objects.create_user(username=username, first_name=first_name,
                                                      last_name=last_name, email=email, password=password)
                user.save()
                messages.success(
                    request, 'Registration successful. Please log in.')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match.')

    return render(request, 'register.html')



User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'
    html_email_template_name = 'reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form, email_not_available=True)
            return render(self.request, self.template_name, context)
