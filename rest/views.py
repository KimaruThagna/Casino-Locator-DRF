# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from  rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework.views import Response
from serializers import *
import geocoder
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
# Create your views here.

class ListCreateCasino(generics.ListCreateAPIView):
    #Can use IsAuthenticated. If its to be accessed only by admin...use is admin user
    #allowAny gives access to everyone
    permission_classes = (IsAdminUser,)
    #requires that one is autenticated (log In)to view data
    #if not set, and in the settings the permission is set to read only for anonnymous users,
    # anonymous can only read and not edit. If Set, you have to be authenticated to log In
    queryset =Casino.objects.all()
    serializer_class = CasinoSerializer
# ovverides the default create function Done when data needs to be saved bak to the table.
    # since we want to create a location field out of address
    def perform_create(self, serializer):
        address=serializer.initial_data['address']
        g=geocoder.google(address)
        latitude=g.latlng[0]
        longitude=g.latlng[1]
        point = GEOSGeometry('POINT(%s %s)' % (latitude, longitude))
        #one can add user=request.user if a user field exists in the model and wishes to
        # associate with user who created
        serializer.save(location=point)


# override default get_queryset method in order to return a specific queryset
    #  which is filtered or has a new field
    # Done when adding a new field that is not necessarily stored in the DB.
    #
    def get_queryset(self):
        qs=Casino.objects.all()
        #check if the query parameters exist in the request
        # if they do, assign to appropriate variable
        latitude=self.request.query_params.get('lat',None)
        longitude = self.request.query_params.get('long', None)
        if latitude and longitude:
            point=GEOSGeometry('POINT(%s %s)' % (latitude, longitude),srid=4326)
            #the distnace function takes 2 GEOESGEOMETRY points and returns the distance btn them
            qs=qs.annotate(distance=Distance('location', point,)).order_by('distance')

        return qs

class CasinoDetail(generics.RetrieveUpdateDestroyAPIView):
 # No need to over-ride the perform_create function since its purpose is to create the location field
 #Which is already created in the previous class. this one is to display a single instance.
 # Its a derivation of the main thing

    serializer_class = CasinoSerializer
# This one is important to annotate distance which is calculated on the fly
 # Its not stored.
    def get_queryset(self):
        qs=Casino.objects.all()
        #check if the query parameters exist in the request if they do, assign to appropriate variable
        latitude=self.request.query_params.get('lat',None)
        longitude = self.request.query_params.get('long', None)
        if latitude and longitude:
            point=GEOSGeometry('POINT(%s %s)' % (latitude, longitude),srid=4326)
            #the distnace function takes 2 GEOESGEOMETRY points and returns the distance btn them
            # annotate adds the specified field to the queryset
            qs=qs.annotate(distance=Distance('location', point,)).order_by('distance')

        return qs

class viewCasinos(viewsets.ReadOnlyModelViewSet):
    queryset = Casino.objects.all()
    serializer_class = CasinoSerializer

def display(request):
    return render(request, 'rest/display.html', {})

class userViewSet(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MainView(APIView):
    #List or create new activity
    def get_queryset(self):
        return Casino.objects.all()

    def get(self,request,format=None):
        casinos=Casino.objects.all()
        serializer=CasinoSerializer(casinos,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer=CasinoSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.data,status=HTTP_400_BAD_REQUEST)