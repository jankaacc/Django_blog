from django.conf.urls import url


from .views import (
    Restaurant_listview,
    Restaurant_detailview,
    RestaurantCreateView,
    RestaurantUpdateView,
    )


app_name = 'restaurants'
urlpatterns = [
    url(r'^$', Restaurant_listview.as_view(), name='restaurantslist'),
    url(r'^create$', RestaurantCreateView.as_view(), name='restaurantscreate'),
    url(r'^(?P<slug>[\w-]+)/$', Restaurant_detailview.as_view(), name='detailrestaurant'),
    url(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='update')
]