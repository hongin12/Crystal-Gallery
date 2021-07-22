"""CrystalGallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from CrystalGallery.crystal.views import auction
from django.contrib import admin
from django.urls import path, include
from crystal import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
<<<<<<< HEAD
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
=======
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),    
>>>>>>> aa84f8c99ad31b0c53d0bb982228d8ae6aec5fa7
    path('signup/', views.signup, name="signup"),
    path('mypage/', views.mypage, name="mypage"),
    path('mygallery/', views.mygallery, name="mygallery"),
    path('auction/<int:listings_id>', views.auction, name="auction"),
    path('auctionArts/', views.auctionArts, name="auctionArts"),
    #path('.auctionArts/', views.auctionArts2, name="auctionArts2"),
    #path(',auctionArts/', views.auctionArts3, name="auctionArts3"),
    path('about/', views.about, name="about"),
<<<<<<< HEAD
    path('logout/', auth_views.LogoutView.as_view(template_name="/"), name='logout'),
    path('upload/', include('profile_maker.urls')),
    path('create/', views.create_profile, name = 'create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
=======
    path('logout/', auth_views.LogoutView.as_view(template_name="/"), name='logout'), 
    path('create/', views.create, name="create"),
    path(' ', views.main2, name="main2"),
    path('.auction/2', views.auction2, name="auction2"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> aa84f8c99ad31b0c53d0bb982228d8ae6aec5fa7
