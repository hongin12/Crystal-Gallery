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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('mypage/', views.mypage, name="mypage"),
    path('mygallery/', views.mygallery, name="mygallery"),
    path('auction/<int:listings_id>', views.auction, name="auction"),
    path('auctionArts/', views.auctionArts, name="auctionArts"),
    path('.auctionArts/', views.auctionArts2, name="auctionArts2"),
    path(',auctionArts/', views.auctionArts3, name="auctionArts3"),
    path('about/', views.about, name="about"),
    path('logout/', views.logout, name="logout"), 
    path('upload/', include('profile_maker.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)