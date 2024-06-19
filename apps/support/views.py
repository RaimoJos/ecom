# ecom/apps/support/views.py
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import translation


def set_language(request):
    lang_code = request.GET.get('lang', None)
    if lang_code and lang_code in dict(settings.LANGUAGES).keys():
        translation.activate(lang_code)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response
    else:
        return redirect('/')


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)
