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
from cart.views import my_notifications

schema_view = get_schema_view(
    openapi.Info(title="API Документация", default_version='v1'),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('chat/', include('chat.urls')),

    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('profile/', profile, name='profile'),
    path('notifications/', my_notifications, name='my_notifications'),

    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









