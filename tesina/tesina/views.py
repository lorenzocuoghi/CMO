from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


def main_page(request):
    return HttpResponseRedirect(reverse('form:index'))


def logout_view(request):
    """Log users out and re-direct them to the main page."""
    logout(request)
    return HttpResponseRedirect(reverse('form:index'))
