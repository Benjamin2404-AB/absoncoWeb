from django.conf import settings
from django.urls import path
from .views import ItemDescriptionView, landing_page ,search_page,facebook_redirect,add_to_cart,cart_view,remove_from_cart, twitter_redirect,update_cart_quantity, whatsapp_redirect
from django.conf.urls.static import static
from .views import instagram_redirect

app_name = 'core'

urlpatterns = [
    path('',landing_page,name='landing_page'),
    path('search/',search_page,name='search'),
    path('item/<str:public_id>/<int:pk>/',ItemDescriptionView.as_view(),name='item_description'),
    path('add_to_cart/',add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/',cart_view, name='cart_view'),
    path('update_cart_quantity/', update_cart_quantity, name='update_cart_quantity'),
     
    # path('facebook/', facebook_redirect,name="facebook"),
    path('contact/whatsapp/', whatsapp_redirect, name='whatsapp_redirect'),
    path('contact/twitter/', twitter_redirect, name='twitter_redirect'),
    path('contact/facebook/',facebook_redirect, name='facebook_redirect'),
    path('contact/instagram/', instagram_redirect, name='instagram_redirect'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    