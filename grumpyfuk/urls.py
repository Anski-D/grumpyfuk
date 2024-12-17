"""
URL configuration for grumpyfuk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.utils import timezone
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.conf import settings
from django.conf.urls.static import static

from blog.models import Post

urlpatterns = [
    path('admin/', admin.site.urls),
]

# URLs from blog app
urlpatterns += [
    path('blog/', include('blog.urls')),
    path('', RedirectView.as_view(url='blog/', permanent=True)),
]

# Media URLs
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs for sitemaps
info_dict = {
    'queryset': Post.objects.filter(published=True).filter(publish_date__lte=timezone.now()).order_by('-publish_date'),
    'date_field': 'last_updated',
}
urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"blog": GenericSitemap(info_dict)}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
