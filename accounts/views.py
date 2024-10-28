from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken,sendEmailToken,sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import random
from django.contrib.auth.decorators import login_required
from .utils import generateSlug
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse


def login_page(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email =email)

        if not hotel_user.exists():
            messages.warning(request,"Account does not exists please register")
            return redirect('/accounts/login/')
        
        if not hotel_user[0].is_verified:
            messages.warning(request,"Account not verified")
            return redirect('/accounts/login')

        hotel_user = authenticate(username = hotel_user[0].username,password=password)

        if hotel_user:
            messages.success(request,"login Success")
            login(request,hotel_user)
            return redirect('/')
        
        messages.warning(request,"Invalid Credentials")

        return redirect('/accounts/login/')





    return render(request,'login_page.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email = email)| Q(phone_number = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request,"Account exists with Email or Phone Number")
            return redirect('/accounts/register/')
            
        try:
            validate_password(password)  # This triggers all configured password validators
        except ValidationError as e:
            messages.warning(request, e.messages[0])
            return redirect('/accounts/vendor-register/') 

        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name =first_name,
            last_name =last_name,
            email =email,
            phone_number =phone_number,
            email_token = generateRandomToken()
        )

        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token,r="user")

        messages.success(request,"An email has been sent to your email address")
        return redirect('/accounts/register/')
    

    return render(request,'register_page.html')

def verify_email_token(request,token):
    try:
        hotel_user = HotelUser.objects.get(email_token = token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/login/')
    except Exception as e:
        return HttpResponse("Invalid Token")
        
def verify_vendor_email(request,token):
    try:
        hotel_vendor = HotelVendor.objects.get(email_token = token)
        hotel_vendor.is_verified = True
        hotel_vendor.save()
        messages.success(request,"Email Verified")
        return redirect('/accounts/vendor-login/')
    except Exception as e:
        return HttpResponse("Invalid Token")

def send_otp_user(request,email):
    hotel_user = HotelUser.objects.filter(email =email)

    if not hotel_user.exists():
        messages.warning(request,"Account does not exists please register")
        return redirect('/accounts/login/')   

    otp = random.randint(1000,9999)
    hotel_user.update(otp=otp)
    sendOTPtoEmail(email,otp)

    return redirect(f'/accounts/{email}u/verify-otp/')

def send_otp_vendor(request,email):
    hotel_vendor = HotelVendor.objects.filter(email = email) 
    
    if not hotel_vendor.exists():
        messages.warning(request,'Account Does Not Exixts please register')
        return redirect('/accounts/vendor-login/')

    otp = random.randint(1000,9999)
    
    hotel_vendor.update(otp=otp)
    sendOTPtoEmail(email,otp)

    return redirect(f'/accounts/{email}v/verify-otp/')

def verify_otp(request,email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email = email)

        if otp == hotel_user.otp:
            messages.success(request,"Login Success")
            login(request, hotel_user)
            return redirect('/accounts/login/')

        messages.warning(request,"Wrong OTP")
        return redirect(f'/accounts/{email}u/verify-otp/')
    
    return render(request,'verify_otp.html')

def verify_vendor_otp(request,email):
    if request.method == "POST":
        otp = request.POST.get('otp')
        hotel_vendor = HotelVendor.objects.get(email = email)

        if otp == hotel_vendor.otp:
            messages.success(request,'Login Success')
            login(request,hotel_vendor)
            return redirect('/accounts/dashboard/')
        
        messages.warning(request,"Wrong OTP")
        return redirect(f'/accounts/{email}v/verify-otp/')
    return render(request,'verify_otp.html')

def register_vendor(request):
    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelVendor.objects.filter(
            Q(email = email)| Q(phone_no = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request,"Account exists with Email or Phone Number")
            return redirect('/accounts/vendor-register/')
            
        try:
            validate_password(password)  # This triggers all configured password validators
        except ValidationError as e:
            messages.warning(request, e.messages[0])
            return redirect('/accounts/vendor-register/')

        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name =first_name,
            last_name =last_name,
            email =email,
            phone_no =phone_number,
            business_name = business_name,
            email_token = generateRandomToken()
        )

        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token,r='vendor')

        messages.success(request,"An email has been sent to your email address")
        return redirect('/accounts/vendor-register/')
    

    return render(request,'vendor/register_vendor.html')

def validate_password_ajax(request):
    if request.method == "POST":
        password = request.POST.get('password')

        try:
            validate_password(password)
            return JsonResponse({'valid':True})
        except ValidationError as e:
            return JsonResponse({'valid':False,'errors':e})

    return JsonResponse({'error':'Invalid request'},status=400)

def validate_phone_ajax(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')

        if phone_number.isdigit() and len(phone_number) == 10:
            return JsonResponse({'valid':True})
        else:
            return JsonResponse({'valid': False,'error':'Phone number must be exactly 10 digits.'})
        
    return JsonResponse({'valid':False, 'error':'Invalid request method.'})

def login_vendor(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(email =email)

        if not hotel_user.exists():
            messages.warning(request,"Account does not exists please register")
            return redirect('/accounts/vendor-login/')
        
        if not hotel_user[0].is_verified:
            messages.warning(request,"Account not verified")
            return redirect('/accounts/vendor-login')

        hotel_user = authenticate(username = hotel_user[0].username,password=password)

        if hotel_user:
            messages.success(request,"login Success")
            login(request,hotel_user)
            return redirect('/accounts/dashboard')
        
        messages.warning(request,"Invalid Credentials")

        return redirect('/accounts/vendor-login/')

    return render(request,'vendor/login_vendor.html')



@login_required(login_url = 'login_vendor')
def dashboard(request):
    context = {'hotels': Hotel.objects.filter(hotel_owner = request.user),'bookings':HotelBooking.objects.all()}

    return render(request,'vendor/vendor_dashboard.html',context)



@login_required(login_url = 'login_vendor')
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties = request.POST.getlist('amenetie')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)

        hotel_vendor = HotelVendor.objects.get(id = request.user.id)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor,
        )

        for amenetie in ameneties:
            amenetie = Ameneties.objects.get(id = amenetie)
            hotel_obj.ameneties.add(amenetie)
            hotel_obj.save()


        messages.success(request,"Hotel Created")
        return redirect('/accounts/add-hotel/')
    
    ameneties = Ameneties.objects.all()
    return render(request,"vendor/add_hotel.html",context={'ameneties':ameneties})


@login_required(login_url = 'login_vendor')
def upload_images(request,slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
        
        
    if request.method == "POST":
        image = request.FILES.get('image')
        if not image:
            messages.warning(request,"No image selected")
            return redirect(f'/accounts/{slug}/upload-images')
        
        print(image)
        HotelImages.objects.create(
            hotel = hotel_obj,
            image = image
        )
        return HttpResponseRedirect(request.path_info)
    
    return render(request,'vendor/upload_images.html',context = {'images':hotel_obj.hotel_images.all()})


@login_required(login_url = 'login_vendor')
def delete_images(request,id):
    hotel_image = HotelImages.objects.get(id=id)
    hotel_image.delete()

    messages.success(request,"Hotel Image Deleted")

    return redirect('/accounts/dashboard')


@login_required(login_url = 'login_vendor')
def edit_hotel(request,slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
        
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")
        
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')

        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location

        hotel_obj.save()

        messages.success(request,"Hotel Details Updated")
        return HttpResponseRedirect(request.path_info)
    
    ameneties = Ameneties.objects.all()
    return render(request,'vendor/edit_hotel.html',context = {'hotel':hotel_obj,"ameneties":ameneties})