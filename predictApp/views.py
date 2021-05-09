from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pandas as pd
from .services import modelTrainer
from .services import getPredict,getPredict2,getMonthlyPredictionForUsers

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
    print("*********\n\n\n\n\n\n\n\n\n\n\n\n\n*******************")
    print(query_params)

    if request.method == 'GET':
        fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
        needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
        months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1

        res = getPredict2.getPredict(fileURL,needPrediction,months)
        return Response(res)

# 1 by 1 users
@api_view(['GET'])
def getMonthlyPrediction(request): 
    # print(request.query_params.get('q'))
    query_params = request.query_params

    # print(query_params)

    if request.method == 'GET':
        fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
        needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
        months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1
    

        try:
            print("*****************************************************")
            url = fileURL
            dataset = pd.read_csv(url)
        except:
            print("*******************Dead*********************")

    
        if(dataset.empty):
            print ('CSV file is empty')
        else:
            print ('CSV file is not empty')
            r = str(needPrediction).replace("'",'')
            data = json.loads(r)

            for product in data:
                print(product)
                
                if product in dataset.columns:
                    print('\n\n\n\n\n\n\n\n')
                    print(product +' is exists in dataset')
                    getMonthlyPredictionForUsers.getPredictMonthly(fileURL, dataset, product, months)
                    # print(res)
                else:
                    print('\n\n\n\n\n\n\n\n')
                    print(product +' is not exists in dataset')
                    # res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
                    # print(res)
                # res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
                # outputs.append(res)
                # print(res)

        # r = str(needPrediction).replace("'",'')
        # data = json.loads(r)
        # data

        # for product in data:
        #     print(product)
        #     res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
        #     # outputs.append(res)
        #     print(res)

        # print(outputs)


        # res = getMonthlyPredictionForUsers.getPredict(fileURL,needPrediction,months)
        # return Response(res)
        return HttpResponse('Welcome to cakery.Ai predict app')