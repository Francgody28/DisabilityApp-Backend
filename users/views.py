from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import DisabledPerson
from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer



@api_view(['POST'])
def register_user(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    if not all([name, email, password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already registered'}, status=400)
    
    user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
    return Response({'message': 'User registered successfully'}, status=200)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user:
        return Response({'message': 'Login successful', 'name': user.first_name}, status=200)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)
@csrf_exempt
def register_disabled_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        person = DisabledPerson.objects.create(
            first_name=data.get('firstName'),
            middle_name=data.get('middleName'),
            last_name=data.get('lastName'),
            age=data.get('age'),
            gender=data.get('gender'),
            disability_type=data.get('customDisability') if data.get('disabilityType') == 'Other' else data.get('disabilityType'),
            contact=data.get('contact')
        )

        return JsonResponse({'message': 'Person registered successfully!'}, status=201)

    elif request.method == 'GET':
        people = list(DisabledPerson.objects.values())
        return JsonResponse(people, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def delete_person(request, id):
    try:
        person = DisabledPerson.objects.get(id=id)
        person.delete()
        return JsonResponse({'message': 'Deleted'}, status=200)
    except DisabledPerson.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@api_view(['DELETE'])
def delete_location(request, pk):
    try:
        location = Location.objects.get(pk=pk)
        location.delete()
        return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

