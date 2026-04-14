from django.conf import settings


def page_config(request):
    return {'ADS_ON': settings.ADS_ON}
