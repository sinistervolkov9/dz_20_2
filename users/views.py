from django.views.generic import CreateView, UpdateView, TemplateView
import secrets
from config.settings import EMAIL_HOST_USER
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from users.forms import UserRegisterForm, UserProfileForm, PasswordRecoveryForm
from users.models import User
from django.http import HttpResponseRedirect


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    # success_url = reverse_lazy('users:code')
    # success_url = reverse_lazy('users:register_message')
    success_url = reverse_lazy('users:register_message')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/)'
        send_mail(
            subject='Подтверждение почты',
            message=f'Подтвердите почту по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        # def form_valid(self, form):
        #     new_pass = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        #     new_user = form.save(commit=False)
        #     new_user.ver_code = new_pass
        #     new_user.save()
        #     send_mail(
        #         subject='Подтверждение почты',
        #         message=f'Код {new_user.ver_code}',
        #         from_email=EMAIL_HOST_USER,
        #         recipient_list=[new_user.email]
        #     )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class RegisterMessageView(TemplateView):
    # model = User
    template_name = 'users/register_message.html'


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    # extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user


# class CodeView(View):
#     model = User
#     template_name = 'users/code.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         code = request.POST.get('code')
#         user = User.objects.filter(ver_code=code).first()
#
#         if user is not None:
#             user.is_active = True
#             user.save()
#             return redirect('users:login')
#
#         else:
#             return redirect('users:code')


class PasswordRecoveryMessageView(TemplateView):
    template_name = 'users/password_recovery_message.html'


class PasswordRecoveryView(TemplateView):
    template_name = 'users/password_recovery_form.html'
    success_url = reverse_lazy('users:recovery_message')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('users:password_recovery'))

        code = secrets.token_hex(8)
        user.set_password(code)
        user.save()

        host = request.get_host()
        url = f'http://{host}/users/'

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль: {code}. Пожалуйста, перейдите по ссылке {url} для входа.',
            EMAIL_HOST_USER,
            [user.email],
        )

        return HttpResponseRedirect(self.success_url)
