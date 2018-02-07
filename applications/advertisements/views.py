import json
from applications.likes.models import Like
from applications.ad_payment.models import AdvertisementPayment
from applications.contacts.models import Contact
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth import logout
from django.db.models import Q
from endless_pagination.views import AjaxListView

import stripe

from .tokens import account_activation_token
from .forms import RegistrationForm, LoginForm, AdvertisementAddForm, AdvertisementEditForm
from .models import Advertisement, Category


class HomeView(TemplateView):
    """
    home page
    """
    template_name = "advertisements/home.html"

class TestView(AjaxListView):
     model = Contact
     paginate_by = 12
     template_name = 'advertisements/test.htm'
     page_template = 'advertisements/test_page_templatet.html'


class InactiveLinkView(TemplateView):
    """
    expired link cone
    """
    template_name = "accounts/invalid_link.html"


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
            messages.success(self.request, 'Welcome to Advertisera %s ! You may now advertise here :D!!' % user.username)
            return redirect('add-advertisement')
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('expired')


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
        form = form.save(commit=False)
        form.created_by = self.request.user
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


class PayView(generic.RedirectView):
    """
    view for making a payment
    """
    def post(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY
        user = self.request.user
        slug = self.kwargs['slug']
        current_site = get_current_site(self.request)
        ad = get_object_or_404(Advertisement, slug=slug)
        new_payment = AdvertisementPayment(advertisement=ad,)
        token = self.request.POST.get("stripeToken")
        email = self.request.POST.get("stripeEmail")
        try:
            charge = stripe.Charge.create(
                amount=2000,
                currency="usd",
                source=token,
                description="The product charged to the user"
            )
            new_payment.transaction_id = charge.id
            new_payment.save()
            mail_subject = 'Advertisera-Payment Successful!'
            message = render_to_string('payment/payment_email.html', {
                'user': user,
                'domain': current_site.domain,
                'transaction_id': new_payment.transaction_id
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            ad.is_featured = True
            ad.save()
            messages.success(self.request, 'You Advertisement Has Been Featured!Check your email for transactional details!')
            return HttpResponseRedirect(self.get_success_url(slug))
        except stripe.error.CardError as ce:
            return False, ce

    def get_success_url(self, slug, **kwargs):
        return reverse_lazy('advertisement-detail', kwargs={'slug': slug})


class LikeView(generic.RedirectView):
    """
    like view
    """
    def post(self, *args, **kwargs):
        result = {}
        slug = self.kwargs['slug']
        user = self.request.user
        ad = get_object_or_404(Advertisement, slug=slug)
        likes = Like.objects.filter(user=user, advertisement=ad)
        if likes.exists():
            likes.delete()
            result['status'] = 'unliked'
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            Like.objects.create(user=user, advertisement=ad)
            result['status'] = 'liked'
            return HttpResponse(json.dumps(result), content_type='application/json')


class SearchAdView(generic.TemplateView):
    """
    search view
    """
    template_name = 'advertisements/categories.html'

    def get(self, request, *args, **kwargs):
        ad_search = self.request.GET.get('ad_search')
        result = {}
        advertisements = Advertisement.objects.all()
        if ad_search:
            advertisements_filtered = advertisements.filter(Q(category__category__icontains=ad_search) |
                Q(title__icontains=ad_search))
            if advertisements_filtered:
                advertisements_filtered = list(advertisements_filtered.values('title', 'slug', 'image'))
                result['advs'] = advertisements_filtered
                result['status'] = 'searched'
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result['status'] = 'na-searched'
                return HttpResponse(json.dumps(result), content_type='application/json')
        result['status'] = 'no-data'
        return HttpResponse(json.dumps(result), content_type='application/json')
