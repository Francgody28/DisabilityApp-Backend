from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import generics
from .models import DisabledPerson, Location
from .serializers import DisabledPersonSerializer, LocationSerializer

#AUTHENTICATION VIEWS
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

# DISABLED PERSON VIEWS
@api_view(['POST', 'GET'])
def register_disabled_person(request):
    if request.method == 'POST':
        data = request.data.copy()

        data['first_name'] = data.get('firstName')
        data['middle_name'] = data.get('middleName')
        data['last_name'] = data.get('lastName')
        data['age'] = data.get('age')
        data['gender'] = data.get('gender')
        data['disability_type'] = (
            data.get('customDisability') if data.get('disabilityType') == 'Other' else data.get('disabilityType')
        )
        data['contact'] = data.get('contact')

        serializer = DisabledPersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Person registered successfully!'}, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        people = DisabledPerson.objects.all()
        serializer = DisabledPersonSerializer(people, many=True)
        return Response(serializer.data)


@api_view(['PUT'])
def update_disabled_person(request, pk):
    try:
        person = DisabledPerson.objects.get(pk=pk)
    except DisabledPerson.DoesNotExist:
        return Response({'error': 'Person not found'}, status=404)

    data = request.data.copy()
    data['first_name'] = data.get('firstName')
    data['middle_name'] = data.get('middleName')
    data['last_name'] = data.get('lastName')
    data['age'] = data.get('age')
    data['gender'] = data.get('gender')
    data['disability_type'] = (
        data.get('customDisability') if data.get('disabilityType') == 'Other' else data.get('disabilityType')
    )
    data['contact'] = data.get('contact')

    serializer = DisabledPersonSerializer(person, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Person updated successfully!', 'data': serializer.data}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_person(request, id):
    try:
        person = DisabledPerson.objects.get(id=id)
        person.delete()
        return JsonResponse({'message': 'Deleted'}, status=200)
    except DisabledPerson.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# LOCATION VIEWS
@api_view(['GET', 'POST'])
def location_list_create(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Location added successfully', 'data': serializer.data}, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PUT'])
def update_location(request, pk):
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=404)

    serializer = LocationSerializer(location, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Location updated successfully', 'data': serializer.data}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_location(request, pk):
    try:
        location = Location.objects.get(pk=pk)
        location.delete()
        return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
