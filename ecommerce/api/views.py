from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getdata(request):
    person = {'name':'prasad','age':28}
    return Response(person)

