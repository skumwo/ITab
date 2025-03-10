from django.contrib import admin
from django.urls import path, include
from products.views import product_list
from django.conf import settings
from django.conf.urls.static import static
from pages.views import contact, faq
from users.views import profile

urlpatterns = [
    path('', product_list, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', product_list, name='product_list'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('profile/', profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










