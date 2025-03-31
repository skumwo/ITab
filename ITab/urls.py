from django.contrib import admin
from django.urls import path, include
from products.views import product_list
from django.conf import settings
from django.conf.urls.static import static
from pages.views import home_view, contact, faq
from users.views import profile
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('profile/', profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









