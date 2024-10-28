from django.shortcuts import render,redirect
from accounts.models import Hotel,HotelBooking,HotelUser
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page


# Create your views here.
# @cache_page(60 * 2)
def index(request):
    hotels = Hotel.objects.all().select_related('hotel_owner').prefetch_related('hotel_images')

    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains = request.GET.get('search'))
    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')
    return render(request,'index.html',context={'hotels':hotels[:50]})


from datetime import datetime

def hotel_details(request,slug):
    hotel = Hotel.objects.get(hotel_slug = slug)
    
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if not start_date or not end_date:
            messages.warning(request,"Please enter Start Date and End Date of Booking")
            return redirect(f'/hotel-details/{slug}')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days_count = (end_date - start_date).days

        if days_count < 0:
            messages.warning(request,"Invalid Dates")
            return HttpResponseRedirect(request.path_info)

        HotelBooking.objects.create(
            hotel = hotel,
            booking_user = HotelUser.objects.get(id=request.user.id),
            booking_start_date = start_date,
            booding_end_date = end_date,
            price = hotel.hotel_offer_price * days_count,
        )
        messages.warning(request,"Booking Captured")

        return HttpResponseRedirect(request.path_info)

    return render(request,'hotel_details.html',context = {'hotel':hotel})


'''def otp(request):
    return render(request,'otp_auth.html')'''