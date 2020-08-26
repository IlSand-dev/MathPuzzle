from django.http import HttpResponseRedirect


def should_be_active(func, url='accounts/login'):
    def wrapper(request, *args, **kwargs):
        if not request.user.role.is_active:
            return HttpResponseRedirect(url)
        return func(request, *args, **kwargs)
    return wrapper