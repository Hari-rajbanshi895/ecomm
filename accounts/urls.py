from django.urls import path
from accounts.views import login_page,register_page , activate_email , add_to_cart , cart , remove_cart  , verify_payment

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('cart/' , cart , name="cart"),
   path('add-to-cart/<uid>/' , add_to_cart , name="add_to_cart"),
   path('remove-cart/<cart_item_uid>/' , remove_cart , name="remove_cart"),
   path('your-verify-url/', verify_payment, name='verify_payment'),

]