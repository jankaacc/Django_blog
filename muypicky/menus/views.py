from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import ItemForm
from .models import Item
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'home.html', {})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Item.objects.filter(user__id__in = is_following_user_ids, public=True).order_by("-updated")
        context = {'object_list':qs}
        return render(request, 'menus/home_feed.html', context)

class ItemListView( LoginRequiredMixin, ListView):
    login_url = '/login/'

    def get_queryset(self):
        return Item.objects.filter(user = self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'

    def get_queryset(self, **kwargs):
        return Item.objects.filter(user = self.request.user)
    # def get_context_data(self, *args ,**kwargs):
    #     # context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
    #     print(kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name = 'form.html'
    login_url = '/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_queryset(self):
        return Item.objects.filter(user = self.request.user)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self,*args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args,**kwargs)
        context['title'] = 'Create Item'
        return context



class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = ItemForm
    template_name = 'form.html'

    def get_queryset(self):
        return Item.objects.filter(user = self.request.user)

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        return kwargs

    def get_context_data(self,*args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args,**kwargs)
        context['title'] = 'Update Item'
        return context
