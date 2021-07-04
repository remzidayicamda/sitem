from django.contrib import admin
from django.urls import path, include
from home.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',home_view, name="home_view"),
    path('hakkimda/',info_view, name="info_view"),
    path('iletisim/',contact, name="contact"),
    path('gizlilik-politikasi/',gizlilik_politika, name="gizlilik-politika"),
    path('cerez-politikasi/',cerez_politika, name="cerez-politika"),

    path('post/', include("post.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'post.views.hendler_400'
handler403 = 'post.views.hendler_403'
handler404 = 'post.views.hendler_404'
handler500 = 'post.views.server_error'

