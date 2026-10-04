from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import FormView
from main import forms

class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from main import models


class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4  # បង្ហាញ ៤ ផលិតផលក្នុងមួយទំព័រ

    def get_queryset(self):
        tag = self.kwargs["tag"]
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug=tag)
            products = models.Product.objects.active().filter(tags=self.tag)
        else:
            products = models.Product.objects.active()
        return products.order_by("name")