import hashlib
import json

import mailchimp_marketing as MailchimpMarketing
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View, generic
from mailchimp_marketing.api_client import ApiClientError

from blog.models import Post

from .forms import LeadForm, NewsletterForm


class IndexPageView(generic.FormView):
    template_name = "index.html"
    form_class = LeadForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = Post.objects.all()[:3]

        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Thank you, we will be in touch shortly")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "It seems you have registered already")
        return super().form_invalid(form)


class PricingView(generic.TemplateView):
    template_name = "pricing.html"


class NewsletterView(View):

    def post(self, request):

        email = request.POST.get('email')

        print(email)

        if not email:
            return HttpResponse('<p class="text-xs">Please enter a valid email address.<p>')

        subscriber_hash = hashlib.md5(email.encode(
            'utf-8')).hexdigest()  # Gets subscriber hash

        try:
            client = MailchimpMarketing.Client()  # Configures Mailchimp client
            client.set_config({
                "api_key": settings.MAILCHIMP_API_KEY,
                "server": settings.MAILCHIMP_SERVER
            })

            # Adds poster to newsletter
            client.lists.add_list_member(settings.MAILCHIMP_LIST_ID, {
                                         "email_address": email, "status": "subscribed", "tags": ["newsletter"]})

            return HttpResponse('<p class="text-xs w-max">Congratulaitons! You are now subscribed.<p>')
        except ApiClientError as error:
            print(error.text)
            res = json.loads(error.text)
            # Custom condition for users that are already subscribed
            if res['title'] == "Member Exists":
                client.lists.update_list_member_tags(settings.MAILCHIMP_LIST_ID, subscriber_hash, {
                                                     "tags": [{"name": "newsletter", "status": "active"}]})
                return HttpResponse('<p class="text-xs w-max">You are already subscribed!</p>')
            return HttpResponse('<p class="text-xs w-max">Something went wrong.</p>')
