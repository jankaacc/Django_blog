from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q


from .utils import unique_slug_generator

# Create your models here.
User = settings.AUTH_USER_MODEL


class RestaurantQuerySet(models.query.QuerySet):
    def search(self,query):
        return self.filter(
            Q(name__icontains=query)|
            Q(category__icontains=query)|
            Q(location__icontains=query)|
            Q(item__name__icontains=query)
        ).distinct()

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Restaurant(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)
    # my_date_field = models.DateTimeField(auto_now=False, auto_now_add=False)

    objects = RestaurantManager()

    def __str__(self):
        str = ''
        if self.name:
            str = str + self.name
        if self.location:
            str = str +' '+ self.location
        if self.category:
            str = str + ' ' + self.category
        return str

    def get_absolute_url(self):
        # return "/restaurants/{}".format(self.slug)
        return reverse('restaurants:detailrestaurant', kwargs={'slug' : self.slug})

    @property
    def title(self):
        return self.name


def rest_pre_save_reciever(sender,instance, *args, **kwargs):

    if instance.category:
        cat = instance.category.lower()
        cat = cat.capitalize()
        instance.category = cat
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rest_pre_save_reciever, sender=Restaurant)
