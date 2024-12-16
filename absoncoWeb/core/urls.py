from django.conf import settings
from django.urls import path
from .views import ItemDescriptionView, landing_page ,search_page
from django.conf.urls.static import static
app_name = 'core'

urlpatterns = [
    path('',landing_page,name='landing_page'),
    path('search/',search_page,name='search'),
    path('item/<slug:item_slug>/<int:pk>/',ItemDescriptionView.as_view(),name='item_description')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    