import random
import string
from django.utils.text import slugify
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''

DONT_USE = 'create'

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug == DONT_USE:
        print("HEY DONT USE THAT")
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug