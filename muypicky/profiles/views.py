
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View, CreateView

from menus.models import Item
from restaurants.models import Restaurant
from .models import Profile
from .forms import UserRegisterForm

User = get_user_model()
User._meta.get_field('email')._unique = True
# Create your models here.


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    return redirect("/login")




class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = '/login'


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        username_to_toggle = request.POST.get("username")
        logged_user = request.user
        f_profile, is_following = Profile.objects.toggle_follow(logged_user, username_to_toggle)

        return redirect("/profiles/{}/".format(f_profile.user.username))



class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        object = get_object_or_404(User, username=username)
        # # print(object)
        return object


    def get_context_data(self,*args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()
        print(context)
        user = context['object']
        is_following = False
        # if user.profile in self.request.user.is_following.all():
        #     is_following = True
        if self.request.user in user.profile.followers.all():
            is_following = True

        context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exist = Item.objects.filter(user=user).exists()
        restaurants_qs = Restaurant.objects.filter(owner=user)
        if query:
            restaurants_qs = restaurants_qs.search(query)
        if items_exist and restaurants_qs.exists():
            context['restaurants_qs'] = restaurants_qs
        return context
