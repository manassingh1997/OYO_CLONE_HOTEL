from django.urls import path
from accounts import views

urlpatterns = [
    path('login/',views.login_page,name="login"),
    path('register/',views.register,name="register"),
    path('verify-account/user<token>/',views.verify_email_token,name="verify_email_token"),#verifies user's email
    path('<email>u/verify-otp/',views.verify_otp, name="verify_otp"),
    path('vendor-login/',views.login_vendor, name="login_vendor"),
    path('vendor-register/',views.register_vendor, name="register_vendor"),
    path('dashboard/',views.dashboard, name = "dashboard"),
    path('logout',views.logout_view,name="logout_view"),
    path('<email>v/verify-otp/',views.verify_vendor_otp, name="verify_vendor_otp"),
    path('verify-account/vendor<token>',views.verify_vendor_email, name = "verify_vendor_email"), #verifies Vendor's email
    path('<email>user/send-otp/',views.send_otp_user, name="send_otp_user"), # Sending OTP to user
    path('<email>vendor/send-otp/',views.send_otp_vendor, name="send_otp_vendor"), # Sending OTP to user
    path('add-hotel/',views.add_hotel, name="add_hotel"),
    path('<slug>/upload-images/',views.upload_images,name="upload_images"),
    path('delete_image/<id>',views.delete_images,name="delete_image"),
    path('edit-hotel/<slug>',views.edit_hotel,name="edit_hotel"),
    path('validate-password/',views.validate_password_ajax,name="validate_password_ajax"),
    path('validate-phone/',views.validate_phone_ajax,name = "validate_phone_ajax"),
]