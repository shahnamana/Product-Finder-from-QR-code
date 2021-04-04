"""qrcode_project_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from myapp import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('django.contrib.auth.urls')), # new
    path('', TemplateView.as_view(template_name='home.html'), name='HomePage'),
    # path(r'', views.homePage, name='HomePage'),
    path('myapp/', include('myapp.urls'), name='Signup'), # new
    path(r'show/<int:num>', views.show_details, name='ShowImg'),
    url(r'codegenerator/', views.qr_code_generate_func, name="GenerateQR"),
    path(r'products/', views.all_products, name='AllProducts')
]
#
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# #
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
