from rest_framework import serializers
from dashboard.models import *

class CarparkSerializers(serializers.ModelSerializer):
    slot_no = serializers.IntegerField(read_only=True)
    ip_adress = serializers.IPAddressField(read_only=True)
    class Meta:
        model = carPark
        fields = ['car_no', 'slot_no', 'ip_adress']


class UnparkSerializers(serializers.ModelSerializer):
    ip_adress = serializers.IPAddressField(read_only=True)
    class Meta:
        model = carPark
        fields = ['car_no', 'slot_no', 'ip_adress']


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ['car_no', 'slot_no']

# class UnparkSerializer(serializers.ModelSerializer):
#     slot_no = serializers.IntegerField()
#     class Meta:
#         model = Unpark
#         fields = ['slot_no']
