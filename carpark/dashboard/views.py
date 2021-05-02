from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.utils.text import slugify
from django.shortcuts import reverse
from django.urls import reverse_lazy
from .forms import *


from dashboard.models import *
from dashboard.serializers import CarparkSerializers, UnparkSerializers, InformationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView

from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

from dashboard import config

import time
# Create your views here.

class IndexView(CreateView):
    template_name = 'main.html'
    model = carPark
    form_class = CarParkForm

    def get(self, *args, **kwargs):
        form = CarParkForm()
        return render(self.request, 'main.html', {'form': form})

    def post(self, *args, **kwargs):
        form = CarParkForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            car_no = form.cleaned_data['car_no']
            post = carPark(
                car_no=car_no
            )
            obj = post.save()
            return redirect('index')
        return render(self.request, 'main.html')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'Park': reverse('cars', request=request, format=format),
        'Info': reverse('info', request=request, format=format),
    })

    

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# rate limit hobe tokhon jokhon time 10s == request 10ta:
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle
# from rest_framework.views import APIView

# class ExampleView(APIView):
#     throttle_classes = [UserRateThrottle]

#     def get(self, request, format=None):
#         content = {
#             'status': 'request was permitted'
#         }
#         return Response(content)

def rate_limit(request):
    customer_ip = get_client_ip(request)
    rate_limit = 10
    
    # new_limit = []
    if request.method == "GET":
        pass
    return customer_ip


class CarparkList(APIView):
    serializer_class = CarparkSerializers
    

    def get(self, request, format=None):
        cars = carPark.objects.all()
        print(rate_limit(request))
        serializer = CarparkSerializers(cars, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        c = carPark.objects.all()
        ip = [a.ip_adress for a in c]
        full_slot = [a.slot_no for a in c]
        total_space = [i for i in range(1, 9)]
        data = {
            'car_no': request.data.get('car_no'),
        }
        serializer = CarparkSerializers(data=data)
        d = len(c) + 1
        if serializer.is_valid():
            current_ip = get_client_ip(request)
            if d == 6:
                return Response({
                    'message': 'All Slot Are Blocked'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif current_ip in ip:
                return Response({
                    'message': 'A Car is booked by your IP'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = serializer.save() 
                obj.slot_no = len(c) + 1
                obj.ip_adress = current_ip
                if obj.slot_no in full_slot:
                    space_slot = [b for b in total_space if b not in full_slot]
                    obj.slot_no = space_slot[0]
                obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnparkList(APIView):
    serializer_class = CarparkSerializers

    def get_object(self, slot_no):
        try:
            return carPark.objects.get(slot_no=slot_no)
        except carPark.DoesNotExist:
            raise Http404
    def get(self, request, slot_no, format=None):
        check_item = self.get_object(slot_no)
        serializer = self.serializer_class(check_item)
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def delete(self, request, slot_no, format=None):
        event = self.get_object(slot_no)
        if event.ip_adress == get_client_ip(request):
            event.delete()
            return Response({
                'message': 'Slot Open'
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'message': 'Input Your Correct Slot No'
            }, status=status.HTTP_400_BAD_REQUEST)

class InfoCar(APIView):
    serializer_class = InformationSerializer

    def get(self, request, format=None):
        cars = Information.objects.all()
        z = [car.slot_no for car in cars]
        j = [car.car_no for car in cars]
        if len(z) == 0 or len(j) == 0:
            return Response({
                "message": "Type Car No Or Slot No"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            info = carPark.objects.filter(slot_no=z[-1]) or carPark.objects.filter(car_no=j[-1]) 
            serializer = InformationSerializer(info, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cars = carPark.objects.all()
        z = [car.slot_no for car in cars]
        j = [car.car_no for car in cars]
        data = {}
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        if (serializer.data['car_no']) not in j and (serializer.data['slot_no'])==None:
            return Response({
                'message': 'Your Car is not parked or type correct Car No'
            })
        elif (serializer.data['slot_no']) not in z and (serializer.data['car_no'])==None:
            return Response({
                'message': 'Your Car is not parked or type correct Slot No'
            })
        else:
            data = {
                'message': 'Found Click On Get'
            }
            return Response(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)