from typing import Iterable
from django.db import models
from django.contrib.auth.models import User


class HotelUser(User):
    profile_picture = models.ImageField(upload_to="profile")
    phone_no = models.CharField(max_length=10,unique = True)
    email_token = models.CharField(max_length = 100, null=True, blank=True)
    otp = models.CharField(max_length = 10, null= True, blank= True)
    phone_number = models.CharField(max_length=100,null=True,blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "hotel_users"

class HotelVendor(User):
    profile_picture = models.ImageField(upload_to="profile")
    business_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100,unique = True)
    email_token = models.CharField(max_length = 100, null=True, blank=True)
    otp = models.CharField(max_length = 10, null= True, blank= True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "hotel_vendors"


class Ameneties(models.Model):
    amenetie_name = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to="hotels")

    def __str__(self) -> str:
        return self.amenetie_name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length= 100)
    hotel_description = models.TextField()
    hotel_slug = models.SlugField(max_length=1000, unique= True)
    hotel_owner = models.ForeignKey(HotelVendor, on_delete=models.CASCADE,related_name="hotel")
    ameneties = models.ManyToManyField(Ameneties)
    hotel_price = models.FloatField()
    hotel_offer_price = models.FloatField()
    hotel_location = models.TextField()
    is_active = models.BooleanField(default= True)

    def __str__(self) -> str:
        return self.hotel_name

class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="hotel_images")
    image = models.ImageField(upload_to='hotels')

class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="hotel_managers")
    manager_name = models.CharField(max_length=100)
    manager_contact = models.CharField(max_length=100)

class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name ="bookings")
    booking_user = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    price = models.FloatField()