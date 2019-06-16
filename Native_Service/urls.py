from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.Pricing.as_view(), name="pricing"),
    path("upload", views.SubmitPricing.as_view(), name="submit_pricing"),
    path(
        "final_pricing/<str:secret_key>/",
        views.FinalPricing.as_view(),
        name="final_pricing",
    ),
    path(
        "price_for_you/<str:secret_key>/",
        views.FinalPricing.as_view(),
        name="price_for_you",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
