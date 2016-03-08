from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate
from emailusernames.utils import create_user, get_user
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# FIXME: Really, really ugly!
from .. import models
from .. import forms


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('../../') ## TODO: OPRAVIT, vyvaruj se absolutnim adresam


class User(DetailView):
    header = "User control panel and information page"
    form = forms.ManageForm

    def get(self, request):
        return render(request, 'web/user.html', {"form": self.form,
                                                 "header": self.header})
    def post(self, request):
        pass


class LoginScreen(DetailView):
    """
        Allows user to login into the system.
    """
    header = "Login"

    name = None
    password = None
    login_form = forms.LoginForm()
    redirect_bool = False
    info_text = None

    user = None

    def get(self, request):
        return render(request, 'web/login_screen.html', {"form": self.login_form,
                                                         "header": self.header})

    def post(self, request):
        self.name = request.POST['user_name']
        self.password = request.POST['user_pass']
        self._check_credentials()
        print (self.name, self.password)

        if self.user:
            login(request, self.user)
            return HttpResponseRedirect('../../')
        else:
            return HttpResponse("INVALID CREDENTIALS!")

    def _check_credentials(self):
        if self.name and self.password:
            self.user = authenticate(email=self.name,
                                     password=self.password)
        else:
            return HttpResponse("MISSING CREDENTIALS!")


class RegisterScreen(DetailView):
    header = "User Registration"

    mail = None
    mail_confirm = None
    password = None
    password_confirm = None
    register_form = forms.RegisterForm()

    correct_day = None
    asked_day = None

    question_ok = False
    exists = False

    correct_details = {}

    request = None

    def get(self, request):
        return render(request, 'web/register.html', {"form": self.register_form,
                                                     "header": self.header})

    def post(self, request):
        self.correct_day = self.register_form.correct_day
        self.request = request

        self._post_get_details()
        self._check_security_question()
        self._check_details()
        self._check_existing_user()

        if self.exists:
            return HttpResponse("ERROR: USER ALREADY EXISTS!")
        else:
            new_user = create_user(email = self.mail, password = self.password)
            new_user.save()
            return HttpResponse("SUCCESS: USER CREATED")

    def _post_get_details(self):
        self.mail = self.request.POST['email']
        self.mail_confirm = self.request.POST['email_confirm']
        self.password = self.request.POST['password']
        self.password_confirm = self.request.POST['password_confirm']

        self.asked_day = self.request.POST['random_antibot']

    def _check_security_question(self):
        self.correct_day = self.register_form.correct_day
        if self.correct_day == self.asked_day:
            self.question_ok = True
        else:
            return HttpResponse("ERROR: INVALID CONTROL ANSWER!")

    def _check_details(self):
        self.correct_details.update({"correct_name": self.mail == self.mail_confirm})
        self.correct_details.update({"correct_password": self.password == self.password_confirm})

        if False in self.correct_details:
            return HttpResponse("ERROR: Some data you entered does not match")


    def _check_existing_user(self):
        test_auth = authenticate(username = self.mail,
                                 password = self.password,
                                 email = self.mail)
        if test_auth:
            self.exists = True
        else:
            self.exists = False


class UserDetail(DetailView):
    model = models.User
