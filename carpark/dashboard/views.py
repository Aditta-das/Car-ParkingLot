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
import threading
import datetime, time
# Create your views here.

 
# IP ADDRESS GET
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# CASE 1
class CarparkList(APIView):
    serializer_class = CarparkSerializers
    
    # get
    def get(self, request, format=None):
        cars = carPark.objects.all()
        serializer = CarparkSerializers(cars, many=True)
        return Response(serializer.data)
    
    # post
    def post(self, request, *args, **kwargs):
        carpark = carPark.objects.all()
        ip = [ip.ip_adress for ip in carpark]
        full_slot = [slot.slot_no for slot in carpark]
        total_space = [i for i in range(1, 9)]
        data = {
            'car_no': request.data.get('car_no'),
        }
        serializer = CarparkSerializers(data=data)
        vaccancy = len(carpark) + 1
        if serializer.is_valid():
            current_ip = get_client_ip(request)
            if vaccancy > config.TOTAL_VACCANCY: # if you want more vaccancy change dashboard/config file TOTAL_VACANCY
                return Response({
                    'message': 'All Slot Are Blocked'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif current_ip in ip:
                return Response({
                    'message': 'A Car is booked by your IP'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = serializer.save() 
                obj.slot_no = len(carpark) + 1
                obj.ip_adress = current_ip
                if obj.slot_no in full_slot:
                    space_slot = [sep_slot for sep_slot in total_space if sep_slot not in full_slot]
                    obj.slot_no = space_slot[0]
                obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CASE 2:
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


# CASE 3:
class InfoCar(APIView):
    serializer_class = InformationSerializer

    def get(self, request, format=None):
        cars = Information.objects.all()
        slots = [car.slot_no for car in cars]
        car_nos = [car.car_no for car in cars]
        if len(slots) == 0 or len(car_nos) == 0:
            return Response({
                "message": "Type Car No Or Slot No"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            info = carPark.objects.filter(slot_no=slots[-1]) or carPark.objects.filter(car_no=car_nos[-1]) 
            serializer = InformationSerializer(info, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cars = carPark.objects.all()
        slots = [car.slot_no for car in cars]
        car_nos = [car.car_no for car in cars]
        data = {}
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        if (serializer.data['car_no']) not in car_nos and (serializer.data['slot_no'])==None:
            return Response({
                'message': 'Your Car is not parked or type correct Car No'
            })
        elif (serializer.data['slot_no']) not in slots and (serializer.data['car_no'])==None:
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


@api_view(['GET'])
def api_root(request, format=None):
    start_time = datetime.datetime.now()
    customer_ip = get_client_ip(request)
    count_ip = []
    check_count = [ip.ip_adress for ip in Rate.objects.all()]
    for your_ip in check_count:
        if customer_ip == your_ip:
            count_ip.append(your_ip)

    if request.method == "GET":
        if len(count_ip) < config.RATE_LIMIT: # if want to change request limit change dashboard/config RATE_LIMIT
            rate_limit = Rate.objects.create()
            rate_limit.ip_adress = customer_ip
            time_diff = (datetime.datetime.now() - start_time).total_seconds()
            rate_limit.time_field = time_diff
            rate_limit.save()
            return Response({
                'Park': reverse('cars', request=request, format=format),
                'Info': reverse('info', request=request, format=format),
            })
        else:
            del_rate = Rate.objects.filter(ip_adress=customer_ip)
            del_rate.delete()
            time.sleep(5)
            return Response({
                'message': f'You were blocked for 5 seconds'
            }, status=status.HTTP_400_BAD_REQUEST)