from django.contrib import admin
from django.urls import path, include
from vehicleapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('help/', views.help, name='help'),
    path('helpreply/', views.helpreply, name='helpreply'),
    path('ride/', views.ride, name='ride'),
    path('drive/', views.drive, name='drive'),
    path('book/<int:did>/', views.book, name='book'),
    path('d_activity/', views.d_activity, name='d_activity'),
    path('r_activity/', views.r_activity, name='r_activity'),
    path('accept/', views.accept, name='accept'),
    path('reject/', views.reject, name='reject'),
    path('request/', views.request, name='request'),
    path('admin/', admin.site.urls),
    path('payment/<int:did>/', views.payment_view, name='payment'),
    path('', include('django.contrib.auth.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
