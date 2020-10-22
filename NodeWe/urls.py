from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve


admin.site.site_header = 'NodeWe'
admin.site.site_title = 'NodeWe'

handler400 = 'Home.views.Error400'
handler403 = 'Home.views.Error403'
handler404 = 'Home.views.Error404'
handler500 = 'Home.views.Error500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('account/auth/', include('allauth.urls')),
    # url('download<str:path>/', serve, {'document_root': settings.MEDIA_ROOT})
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
