from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect  # dit zorgt ervoor dat wij templates kunnen teruggeven
from django.views.generic import View
from django.contrib.auth import authenticate, logout, login
from django.views import generic
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User, UserProfile, Pand
from master.forms import LoginForm, VerkoperForm, UserProfileForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.views.generic import TemplateView


LOGIN_PASSWORD_WRONG_TEXT = 'Email/Wachtwoord fout!'
LOGIN_NOT_FOUND_TEXT = 'Email/Wachtwoord niet in het record teruggevonden!'
LOGIN_INVALID_FORM_TEXT = 'Formulier is niet juist ingevuld!'





def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response


class PandenView(generic.ListView):
    template_name = 'master/panden.html'
    context_object_name = 'alle_panden'

    def get_queryset(self):
        return Pand.objects.all()


class PandDetail(generic.DetailView):
    model = Pand
    context_object_name = 'pand'
    template_name = 'master/pand.html'


class PartnerView(View):
    template_name = 'master/partner.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)



class IndexView(View):
    template_name = 'master/index.html'

    def get(self, request):
        return render(request, self.template_name)


class AboutView(View):
    template_name = 'master/about.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ContactView(View):
    template_name = 'master/contact.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class VerkoperView(View):
    form_class = VerkoperForm
    template_name = 'master/verkoper.html'
    subject = ""
    contact_message = ""

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("first_name") + '_' + form.cleaned_data.get("last_name")
            existing_email = User.objects.filter(email=email)
            existing_username = User.objects.filter(username=username)
            if not existing_username:
                if not existing_email:
                    first_name = form.cleaned_data.get("first_name")
                    last_name = form.cleaned_data.get("last_name")
                    username = first_name + '_' + last_name
                    sender = settings.EMAIL_HOST_USER
                    password = User.objects.make_random_password()
                    self.subject = "ViaSofie Account Registratie"
                    self.contact_message = "Jouw inlog gegevens zijn succesvol aangemaakt! \n" \
                                           "email: " + email + "\n" \
                                                               "wachtwoord: " + password
                    send_mail(self.subject, self.contact_message, sender, [email])
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    profile = UserProfile.objects.create(user=user, locatie='', geslacht='')
                    profile.save()

                    return render(request, self.template_name, {'form': form,
                                                                'success': 'Account is succesvol aangemaakt! De gebruikersnaam & wachtwoord zijn naar ' + email + ' verzonden.'})
                else:
                    return render(request, self.template_name, {'form': form, 'error': 'Dit Email bestaat al!'})
            else:
                return render(request, self.template_name,
                              {'form': form, 'error': 'De voornaam en achternaam komen overeen met een record.'})
        else:
            return render(request, self.template_name, {'form': form, 'error': 'Invalid form!'})

    def get(self, request):
        if request.user.is_superuser:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'master/index.html', {})


class AdviceView(View):
    template_name = 'master/advice.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

"""
class ProfileViewNonUser(generic.DetailView):
    template_name = 'master/profile.html'
    slug = None
    fields = ['locatie', 'geslacht']
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
"""


class ProfileView(UpdateView):
    model = UserProfile
    template_name = 'master/profile.html'
    fields = ['locatie', 'geslacht']

"""
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return render(request, 'master/index.html')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)*/
"""



class LoginFormView(View):
    form_class = LoginForm
    template_name = 'master/login.html'

    # display bank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # handle submit form
    def post(self, request):
        print request.POST['email']
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned (normalized) data = formatted properly eg date
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_object = User.objects.get(email=email)  # WORKAROUND
                user = authenticate(username=user_object.username, password=password)
                if user is not None:
                    # check if user is banned
                    if user.is_active:
                        login(request, user)
                        return redirect('loggedin')
                else:
                    return JsonResponse({'error': LOGIN_PASSWORD_WRONG_TEXT})
            except ObjectDoesNotExist:
                return JsonResponse({'error': LOGIN_NOT_FOUND_TEXT})
                # returns User objects if credentials are correct
        # if not logged in correctly
        #self.template_name, {'form': form, 'error': 'Invalid form!'}
        return JsonResponse({'error': LOGIN_INVALID_FORM_TEXT})


class Loggedin(View):
    template_name = 'master/auth/loggedin.html'

    def get(self, request):
        return render(request, self.template_name)


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            template_name = 'master/auth/logout.html'
        else:
            template_name = 'master/index.html'
        return render(request, template_name)
