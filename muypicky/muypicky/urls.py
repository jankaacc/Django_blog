"""muypicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import include, url
from django.views.generic import TemplateView


from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view
from menus.views import HomeView




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$',RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[A-Z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^login/',LoginView.as_view(redirect_field_name='home.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(redirect_field_name='/home'), name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^contact/$', TemplateView.as_view(template_name ='contact.html'), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name ='about.html'), name='about'),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^menus/', include('menus.urls', namespace='menus')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),


]
# (?P<id>\d+)/