from django.conf.urls import url


from .views import (
    ProfileDetailView
    )


app_name = 'profiles'
urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='details'),
]