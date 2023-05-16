from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from fond.views import *
from zhyly_zhurek import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # path('all/electronics', ElectronicaShowView.as_view(), name='electronics'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    # path("profile/", ProfileView.as_view(), name="profile"),
    # path('zhurek/<slug:slug>/', CategoryView.as_view(), name="category"),
    # path('zhurek/<slug:cat_slug>/<slug:slug>', SingleElectronicaView.as_view(), name='single_electronica'),
    path('register/', Register.as_view(), name="costumerRegister"),
    path('login/', LoginUser.as_view(), name="costumerLogin"),
    path('auth/logout/', costumerLogout, name="costumerLogout"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
