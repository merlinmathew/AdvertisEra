from applications.advertisements.ElasticEmailClient import Email
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic
from .forms import ContactForm
from .models import Contact
from applications.advertisements.ElasticEmailClient import ApiClient

ApiClient.apiKey = 'c2134a3e-be27-4e55-a3b8-c8032b80c84e'

# class ContactView(generic.CreateView):
#     """
#     For Feedbacks
#     """
#     model = Contact
#     form_class = ContactForm
#     template_name = 'contact/contact.html'
#
#     def form_valid(self, form):
#         form = form.save(commit=False)
#         current_site = get_current_site(self.request)
#         mail_subject = 'Advertisera-Contact Form Submission Succesful!'
#         message = render_to_string('contact/contact_response.html', {
#             'user': form.name,
#         })
#         to_email = form.email
#         email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#         )
#         email.send()
#         form.save()
#         messages.success(self.request, "Oh Great! Your response has been recorded!")
#         return redirect('contact')

# class ContactView(generic.CreateView):
#     """
#     For Feedbacks
#     """
#     model = Contact
#     form_class = ContactForm
#     template_name = 'contact/contact.html'
#
#     def form_valid(self, form):
#         form = form.save(commit=False)
#
#         subject = 'Your subject'
#         fromEmail = 'merlin.sayone@gmail.com'
#         fromName = 'Your Company Name'
#         bodyText = 'Text body'
#         bodyHtml = '<h1>Hello, {username}.</h1>'
#         files = { 'templates/base/recipients.csv' }
#         filenameWithRecipients = 'templates/base/recipients.csv' # same as the file above
#         email = Email()
#         emailResponse = email.Send(subject, fromEmail, fromName, bodyText = bodyText, bodyHtml = bodyHtml,to={'merlin.sayone@gmail.com'})
#
#         try:
#             print ('MsgID to store locally: ', emailResponse['messageid'], end='\n') # Available only if sent to a single recipient
#             print ('TransactionID to store locally: ', emailResponse['transactionid'])
#         except TypeError:
#             print ('Server returned an error: ', emailResponse)
#         form.save()
#         messages.success(self.request, "Oh Great! Your response has been recorded!")
#         return redirect('contact')

class ContactView(generic.CreateView):
    """
    For Feedbacks
    """
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        send_mail = EmailMessage(subject='Advertisera-Contact Submission Successfull', body='Thank You for contacting us..We will get back to you',from_email='merlin.sayone@gmail.com', to=['merlinm.mathew07@gmail.com',])
        send_mail.send()
        form.save()
        return redirect('contact')
