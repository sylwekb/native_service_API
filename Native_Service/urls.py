from django.urls import path
from Native_Service import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "Native_Service"
urlpatterns = [
    path("", views.Pricing.as_view(), name="index"),
    path("upload", views.FormSubmit.as_view(), name="upload"),
    path(
        "final_pricing/<str:secret_key>/",
        views.FinalPricing.as_view(),
        name="finalpricing",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
