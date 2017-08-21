# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponseRedirect, StreamingHttpResponse

from .models import UserProfile
from .forms import LoginForm, RegisterForm, UpdateEmailForm, UpdatePasswordForm, UploadFileForm
from competitions.models import Competition, AttendedPerson
from utils.mixin_utils import LoginRequiredMixin


# 自定义登陆校验
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登陆逻辑
class LoginView(View):
    def get(self, request):
        next = request.GET.get('next', '/').replace('<', '')
        return render(request, "login.html", {"next": next})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user:
                next = request.POST.get('next', '/')
                if next == '':
                    next = '/'
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"msg": "用户名或密码不可为空"})


# 注册逻辑
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            username = request.POST.get("username", "")
            if UserProfile.objects.filter(Q(email=email) | Q(username=username)):
                return render(request, "register.html", {"msg": "用户名或邮箱已被注册", "register_form": register_form})
            else:
                password_1 = request.POST.get("password_1", "")
                password_2 = request.POST.get("password_2", "")
                if password_1 != password_2:
                    return render(request, "register.html", {"msg": "两次输入密码不相同", "register_form": register_form})
                else:
                    user_profile = UserProfile()
                    user_profile.username = username
                    user_profile.email = email
                    user_profile.set_password(password_1)
                    user_profile.save()
                    return HttpResponseRedirect("/login/")
        else:
            return render(request, "register.html", {"register_form": register_form})


# 登出逻辑
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# 用户信息页
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user-info.html", {})

    def post(self, request):
        user = UserProfile.objects.get(username=request.user.username)
        user.gender = request.POST.get("gender", "")
        user.identity = request.POST.get("identity", "")
        user.city = request.POST.get("city", "")
        user.mobile = request.POST.get("mobile", "")
        user.organization = request.POST.get("organization", "")
        user.year = request.POST.get("year", "")
        user.work = request.POST.get("work", "")
        user.introduction = request.POST.get("introduction", "")
        user.save()
        return HttpResponseRedirect('/user/info/')


# 设置邮箱页
class UserSetEmailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user-set-email.html", {})

    def post(self, request):
        update_email_form = UpdateEmailForm(request.POST)
        if update_email_form.is_valid():
            password = request.POST.get("password", "")
            email = request.POST.get("email", "")
            user = UserProfile.objects.get(username=request.user.username)
            if user.check_password(password):
                user.email = email
                user.save()
                return HttpResponseRedirect('/user/info/')
            else:
                return render(request, "user-set-email.html", {"msg": "密码错误"})
        else:
            return render(request, "user-set-email.html", {"update_email_form": update_email_form})


# 设置密码页
class UserSetPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user-set-password.html", {})

    def post(self, request):
        update_password_form = UpdatePasswordForm(request.POST)
        if update_password_form.is_valid():
            old_password = request.POST.get("old_password", "")
            new_password_1 = request.POST.get("new_password_1", "")
            new_password_2 = request.POST.get("new_password_2", "")
            user = UserProfile.objects.get(username=request.user.username)
            if user.check_password(old_password):
                if new_password_1 == new_password_2:
                    user.set_password(new_password_1)
                    user.save()
                    return HttpResponseRedirect('/user/info/')
                else:
                    return render(request, "user-set-password.html", {"message": "两次输入密码不相同"})
            else:
                return render(request, "user-set-password.html", {"message": "密码错误"})
        else:
            return render(request, "user-set-password.html", {"update_password_form": update_password_form})


class UserAttendView(LoginRequiredMixin, View):
    def get(self, request):
        attended_person = AttendedPerson.objects.filter(person=request.user)
        uploaded_competitions = attended_person.exclude(Q(file__isnull=True) | Q(file__exact=''))
        other_competitions = attended_person.filter(Q(file__isnull=True) | Q(file__exact=''))
        number = attended_person.count()
        return render(request, "user-attend.html",
                      {"uploaded_competitions": uploaded_competitions,
                       "other_competitions": other_competitions,
                       "number": number})


# 上传、下载文件
class UserUploadView(LoginRequiredMixin, View):
    def post(self, request):
        file_form = UploadFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            uploaded_file = file_form.cleaned_data['file']
            competition_id = request.POST.get('competition_id', '')
            attended_person = AttendedPerson.objects.get(person=request.user, competition_id=competition_id)
            attended_person.file = uploaded_file
            attended_person.save()
            return HttpResponseRedirect('/user/attend/')
        else:
            return HttpResponseRedirect('/user/attend/')


# 下载文件
class UserDownloadView(LoginRequiredMixin, View):
    def get(self, request, competition_id):
        competition = Competition.objects.get(id=competition_id)
        exam = competition.exam

        def file_iterator(chunk_size=512):
            while True:
                c = exam.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        response = StreamingHttpResponse(file_iterator())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(exam.name.split('/')[-1])
        return response

