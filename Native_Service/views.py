from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from .models import NativePost, FinalPricing as FinalPricingModel
from .forms import NativePostForm, FinalPricingForm
from Native_Service.lib.native_service import ProgressStages
from Native_Service.lib.native_service import secret_key_generator
from Native_Service.lib.native_service import final_pricing_url_genrator
from Native_Service.lib.native_service import accept_view_url_generator
from Native_Service.lib.native_service import accept_price_url_generator


import datetime

"""
def dispatch(self, request, *args, **kwargs):
    import pdb
    breakpoint()
    return super().dispatch(request, *args, **kwargs)
"""


class Pricing(FormView):
    """ Pricing view for not logged in users. """

    template_name = "pricing.html"
    secret_key = None
    form_class = NativePostForm
    success_url = "/upload"
    files = None

    def get(self, request, *args, **kwargs):
        """ Method generates secret_key in every request. """
        self.secret_key = secret_key_generator()

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = self.secret_key

        # Sets secret_key as default value in form.
        self.initial = {"secret_key": self.secret_key}
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """ Method posts form and saves the files in storage"""
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Makes list of files
        self.files = request.FILES.getlist("file")

        if form.is_valid():
            for f in self.files:
                fs = FileSystemStorage(
                    location=settings.MEDIA_ROOT + f"uploads/{datetime.date.today()}/"
                )
                fs.save(f"{f}".replace(" ", "_"), ContentFile(f.read()))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """ Form validation with an email alert for NativeService. """

        # Gets secret_key from session
        self.secret_key = self.request.session["secret_key"]
        post = form.save(commit=False)
        post.save()

        # Creates custom url for performer
        url = final_pricing_url_genrator(self.secret_key)
        # Initializing Progress Stages library
        ProgressStages(form.cleaned_data, self.files, url).in_queue_stage()

        self.request.session.set_test_cookie()
        return super().form_valid(form)


class SubmitPricing(Pricing):
    """ Correct form view for CUSTOMER protected by session. """

    def get(self, request, *args, **kwargs):
        if self.request.session.test_cookie_worked():
            # Gets secret_key from session
            self.secret_key = self.request.session["secret_key"]
            return self.render_to_response(self.get_context_data())

    def render_to_response(self, context, **response_kwargs):
        """ Form data rendering in submit view. Protected by session. """
        template_name = "pricing_submit.html"

        if self.request.session.test_cookie_worked():
            # getting record from db by 'secret_key'
            data = NativePost.objects.filter(secret_key=self.secret_key)
            self.data_dict = {}
            for i in data.values():
                self.data_dict.update(i)

            self.request.session.delete_test_cookie()
            return render(self.request, template_name, self.data_dict)


class FinalPricing(FormView):
    """ View for performer to set a price for customer. """

    template_name = "final_pricing.html"
    form_class = FinalPricingForm
    success_url = "final_pricing_submit"

    def get(self, request, *args, **kwargs):
        # Gets 'secret_key' from url
        path = self.request.path
        self.secret_key = path.rsplit("/")[-2]

        # Passing secret_key by session to other methods
        self.request.session["secret_key"] = self.secret_key

        # Finds record in db with 'secret_key'
        data = NativePost.objects.filter(secret_key=self.secret_key)

        self.data_dict = {}
        for i in data.values():
            self.data_dict.update(i)

        self.initial = {"secret_key": self.secret_key}
        return self.render_to_response(self.get_context_data())


    def form_valid(self, form):
        """ Form validation with an email alert for NativeService. """
        post = form.save(commit=False)
        post.save()

        # Gets secret_key from session
        self.secret_key = self.request.session["secret_key"]

        # Gets record from NativePost by 'secret_key'
        data = NativePost.objects.filter(secret_key=self.secret_key)
        self.data_dict = {}
        for i in data.values():
            self.data_dict.update(i)

        # Gets record from FinalPricing by 'secret_key'
        price = FinalPricingModel.objects.filter(secret_key=self.secret_key)
        self.price_dict = {}
        for j in price.values():
            self.price_dict.update(j)

        # Creates url for customer to see price
        email_url = accept_view_url_generator(self.secret_key)

        # Creates url which gives possibility to accept price by customer
        price_accept_url = accept_price_url_generator(self.secret_key)
        # Setting stage in Progress Stages library
        ProgressStages(
            data=self.data_dict,
            url=email_url,
            price=self.price_dict,
            url_accept_price=price_accept_url,
        ).pricing_in_progress_stage()

        self.request.session.set_test_cookie()
        return super().form_valid(form)

class FinalPricingSubmit(TemplateView):
    template_name = "final_pricing_submit.html"