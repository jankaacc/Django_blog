from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from .models import Restaurant
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm


class Restaurant_listview(LoginRequiredMixin, ListView):
    # template_name = 'restaurants/restaurants_list.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner = self.request.user)
        return queryset


class Restaurant_detailview(LoginRequiredMixin, DetailView):

    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner = self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(Restaurant_detailview, self).get_context_data(*args, **kwargs)
        # print(context)
        print(kwargs)
        return context

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'form.html'
    # success_url = '/restaurants/'

    def form_valid(self, form):
        instance = form.save(commit = False)
        instance.owner = self.request.user
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self,*args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = 'Update Restaurant {}'.format(name)
        return context

    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner = self.request.user)
        return queryset



















