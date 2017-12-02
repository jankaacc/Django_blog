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


# class HomeView(TemplateView):
#     template_name = "home.html"
#
#     def get_context_data(self,*args, **kwargs):
#         context = super(HomeView, self).get_context_data(*args, **kwargs)
#         print(context)
#         context = {
#             "num" : 555
#         }
#         return context

# def restaurant_listview(request):
#     # template_name = 'restaurants/restaurants_list.html'
#     queryset = Restaurant.objects.all()
#     context = {
#         "object_list" : queryset
#     }
#     return render(request, template_name, context)


# def restaurant_createview(reqest):
#     form = RestaurantLocationCreateForm(reqest.POST or None)#RestaurantCreateForm(reqest.POST or None)
#     errors = None
#     if form.is_valid():
#         form.save()
#         # obj = Restaurant.objects.create(
#         #     name = form.cleaned_data.get('name'),
#         #     location = form.cleaned_data.get('location'),
#         #     category = form.cleaned_data.get('category')
#         # )
#         return HttpResponseRedirect('/restaurants/')
#     if form.errors:
#         errors = form.errors
#
#     template_name = 'form.html'
#     context = {
#         'form':form,
#         'errors':errors
#     }
#     return render(reqest, template_name,context)

class Restaurant_listview(LoginRequiredMixin, ListView):
    # template_name = 'restaurants/restaurants_list.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner = self.request.user)
        return queryset
        # print(self.kwargs)
        # slug = self.kwargs.get("slug")
        # if slug:
        #     queryset = Restaurant.objects.filter(
        #         Q(location__iexact=slug) |
        #         Q(location__icontains=slug)
        #     )
        # else:
        #     queryset = Restaurant.objects.all()
        # print(queryset)
        # return queryset


class Restaurant_detailview(LoginRequiredMixin, DetailView):
    # queryset = Restaurant.objects.filter(owner = self.request.user)
    # template_name = 'restaurants/restaurant_detail.html'
    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner = self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(Restaurant_detailview, self).get_context_data(*args, **kwargs)
        # print(context)
        print(kwargs)
        return context

    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('rest_id')
    #     print('your object')
    #     obj = get_object_or_404(Restaurant, id=rest_id)
    #     print(obj)
    #     return obj

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



















