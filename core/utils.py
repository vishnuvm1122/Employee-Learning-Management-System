import random
import string
from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):
    slug = new_slug if new_slug else slugify(str(instance))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))