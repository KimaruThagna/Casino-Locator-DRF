
from django.conf.urls import url,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from views import *
from . import views
from rest_framework import routers

# urlpatterns = [
#
# url(r'^api/Casinos/$', ListCreateCasino.as_view()),
# url(r'^dis/$', views.display,name='display'),
# url(r'^api/users/?P<pk>[0-9]+/$', userViewSet.as_view()),
# url(r'^api/Casino/(?P<pk>[0-9]+)/$', CasinoDetail.as_view()),
# ]
#(?P<pk>[a-z0-9]+) can work for alphanumeric input where pk is name of column from table
#allows you to specify the output format of your API eg in json or xml format
#eg http://127.0.0.1:8000/api/Casino/13.json?lat=-1.32455&long=36.2144
#urlpatterns=format_suffix_patterns(urlpatterns)

# another way to accomplish multiple formats such as json and csv
#This uses viewsets
router=routers.DefaultRouter()
router.register(r'casino',viewCasinos,base_name=None)
router.register(r'users',userViewSet,base_name=None)

urlpatterns = [

url(r'^api/Casinos/', ListCreateCasino.as_view()),
url(r'ne/',include(router.urls)),# The API Root which when visited,
    # reveals links to all other routes registered by the router
url(r'api-auth-token',obtain_auth_token),# If its a post method, it allows you to greb the token
url(r'^api/Casino/(?P<pk>[0-9]+)/$', CasinoDetail.as_view()),
]