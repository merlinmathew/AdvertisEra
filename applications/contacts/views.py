from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic
from .forms import ContactForm
from .models import Contact


class ContactView(generic.CreateView):
    """
    For Feedbacks
    """
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        mail_subject = 'Advertisera-Contact Form Submission Succesful!'
        message = render_to_string('contact/contact_response.html', {
            'user': form.name,
        })
        to_email = form.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        form.save()
        messages.success(self.request, "Oh Great! Your response has been recorded!")
        return redirect('contact')
