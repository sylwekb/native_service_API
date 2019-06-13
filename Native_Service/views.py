from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .models import NativePost
from .forms import NativePostForm, FinalPricing
from Native_Service.lib.native_service import ProgressStages, secret_key_generator
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
import datetime
from django.urls import reverse



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
        # Sets secret_key as default value in form.
        self.initial = {"secret_key": self.secret_key}
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
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
        post = form.save(commit=False)
        post.save()
        # initializing Progress Stages library
        ProgressStages(form.cleaned_data, self.files)
        self.request.session.set_test_cookie()
        return super().form_valid(form)


class FormSubmit(Pricing):
    """ Correct form view protected by session. """

    def render_to_response(self, context, **response_kwargs):
        """ Form data rendering in submit view. Protected by session. """
        template_name = "upload.html"
        posts = NativePost.objects.all()
        args = posts.values().last()
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return render(self.request, template_name, args)


class FinalPricing(FormView):
    template_name = "final_pricing.html"
    form_class = FinalPricing
    success_url = "final_pricing_submit"

    def get(self, request, *args, **kwargs):
        db = NativePost
        all = db.objects.filter(secret_key='i00ntk2xgj41')
        self.data_dict = {}
        for i in all.values():
            self.data_dict['secret_key'] = i['secret_key']

            print(i)
        print(self.data_dict)

        return self.render_to_response(self.get_context_data())
