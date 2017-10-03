#used to convert database data to json for the API and vice versa
from rest_framework import  serializers
from django.contrib.auth.models import User
from models import *


class CasinoSerializer(serializers.ModelSerializer):
    #declare distance since it doesnt exist on the form
    distance=serializers.DecimalField(source='distance.km',read_only=True,
                                      required=False,decimal_places=3,
                                      max_digits=10) # distance.mi will return figure in miles
    class Meta:
        model= Casino
        fields=['id','name','address','location','distance']
        read_only_fields=['location','distance']#doesnt appear in the input textbox


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=['id','url','username','is_staff']