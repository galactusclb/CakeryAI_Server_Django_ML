from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import modelTrainer
from .services import getPredict,getPredict2

def index(request):
    return HttpResponse('Welcome to cakery.Ai predict app')

@api_view(['GET'])
def trainPredict(request):
    if request.method == 'GET':
        try:
            res = modelTrainer.trainModel()
            return Response(res)
        except:
            return Response({"Error": "something wrong"}, status=500)

@api_view(['GET'])
def getPrediction(request):
    if request.method == 'GET':
        res = getPredict.getPredict()
        return Response(res)

@api_view(['GET'])
def getPredictionEduraca(request):
    # print(request.query_params.get('q'))
    query_params = request.query_params

    print(query_params)

    if request.method == 'GET':
        fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
        needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
        months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1

        res = getPredict2.getPredict(fileURL,needPrediction,months)
        return Response(res)