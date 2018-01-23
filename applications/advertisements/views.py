from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from django.views.generic import TemplateView, FormView
from django.contrib.auth import logout

from applications.ad_payment.forms import SalePaymentForm
from applications.advertisements.tokens import account_activation_token
from .forms import RegistrationForm, LoginForm, AdvertisementAddForm, AdvertisementEditForm
from .models import Advertisement, Category


class HomeView(TemplateView):
    """
    home page
    """
    template_name = "advertisements/home.html"


class ContactView(TemplateView):
    """
    contact page
    """
    template_name = "advertisements/contact.html"


class AboutView(TemplateView):
    """
    about page
    """
    template_name = "advertisements/about.html"


class CategoryListingView(generic.ListView):
    """
    to list advertisements under a particular category
    """
    model = Category
    template_name = 'advertisements/category_listing.html'
    context_object_name = 'ads'

    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        ads = Advertisement.objects.filter(category=category)
        return ads


class RegisterView(FormView):
    """
    to register a new user
    """
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Advertisera account.'
        message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(self.request, 'Hey %s !! Please confirm your email address to complete the registration !' % user.username)
        return render(self.request, self.template_name, {'form': RegistrationForm()})


class AccountActivationView(FormView):
    """
    view for activating an account after registration
    """
    def get(self, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            login(self.request, user)
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


class LoginView(FormView):
    """
    view for login
    """
    model = User
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'You have successfully logged in !')
        return redirect('add-advertisement')


def logout_view(request):
    """
    view for logout
    """
    logout(request)
    return redirect('home')


class AddAdvertisementView(generic.CreateView):
    """
    to create an advertisement
    """
    model = Advertisement
    success_url = reverse_lazy('home')
    form_class = AdvertisementAddForm
    template_name = 'advertisements/add_advertisement.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.created_by = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        object = Advertisement.objects.latest('id')
        slug = object.slug
        return reverse_lazy('advertisement-detail', kwargs={'slug': slug})


class AdvertisementDetailView(generic.DetailView):
    """
    to display advertisement detail
    """
    template_name = 'advertisements/advertisement_detail.html'
    context_object_name = 'advertisement'
    model = Advertisement


class AdvertisementEditView(generic.UpdateView):
    """
    to edit an advertisement
    """
    model = Advertisement
    template_name = 'advertisements/edit_advertisement.html'
    context_object_name = 'advertisement'
    form_class = AdvertisementEditForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('advertisement-detail', kwargs={'slug': self.kwargs['slug']})


class AdvertisementDeleteView(generic.DeleteView):
    """
    to delete an advertisement
    """
    model = Advertisement
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, '%s has been deleted...!' % obj.title)
        return self.post(request, *args, **kwargs)


def charge(request):
    """
    view for making a payment
    """
    if request.method == "POST":
        form = SalePaymentForm(request.POST)

        if form.is_valid():  # charges the card
            return HttpResponse("Success! We've charged your card!")
    else:
        form = SalePaymentForm()

    return render(request, "payment/charge.html", {'form': form})
