from django.conf.urls import url


from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    )


app_name = 'menus'
urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='list'),
    url(r'^create$', ItemCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\w-]+)/$', ItemDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w-]+)/edit$', ItemUpdateView.as_view(), name='update')
]