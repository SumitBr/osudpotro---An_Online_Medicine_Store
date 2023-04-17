from django.contrib import admin
from django.urls import path, include
from MVC import controllers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MVC.routes',namespace='MVC')),
    # path('account/', include('account.urls',namespace='account')),
    path('', include('MVC.routes',namespace='account')),
    path('payment-success', controllers.payment_success_view,name='payment-success'),
    path('search', controllers.search_view, name='search'),
    path('checkout', controllers.user_address_view, name='address'),
    path('purchase', controllers.payment_success_view, name='payment'),

]
 
# Media Folder
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
