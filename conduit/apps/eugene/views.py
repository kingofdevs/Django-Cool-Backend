from django.http import HttpResponse
from rest_framework import status
from .models import Country
from .serializers import CountrySerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .forms import CountryChangeForm


@api_view(['GET'])
def get_countries(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_country(request):
    serializer_data = JSONParser().parse(request)
    serializer = CountrySerializer(data=serializer_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail_country(request, pk):
    try:
        project = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    serializer = CountrySerializer(project)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
def update_country(request, pk):
    try:
        project = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    form = CountryChangeForm(request.data or None, instance=project)

    if form.is_valid():
        form.save()
        return JsonResponse(form.data)
    return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_country(request, pk):
    try:
        country = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    country.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
