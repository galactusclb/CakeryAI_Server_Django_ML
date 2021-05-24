from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import pandas as pd
from six import print_
from .services import modelTrainer
from .services import getPredict,getPredict2,getMonthlyPredictionForUsers

def index(request):
    return HttpResponse('Welcome to cakery.Ai predict app')

@api_view(['GET'])
def trainPredict(request):
    query_params = request.query_params
    
    if request.method == 'GET':
        try:

            print(query_params)
            fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
            needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
            userId = query_params.get('userId') if query_params.get('userId') else ''

            needPredictionList = json.loads(needPrediction)
            print(needPredictionList)

            outputs = []

            for item in needPredictionList:
                print(item)
                res = modelTrainer.trainModel(fileURL,item,userId)
                outputs.append({ 'product': item, 'trainedModelURL': res})

            print(outputs)
            
            return Response(outputs, status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"Error": "something wrong"}, status=500)

@api_view(['GET'])
def getPrediction_pro(request):

    query_params = request.query_params

    if request.method == 'GET':
        try:
            fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
            modelURL = query_params.get('modelURL') if query_params.get('modelURL') else ''
            needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
            months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1

            needPrediction = json.loads(needPrediction)
            print('fileURL: ', fileURL)
            print('modelURL: ', modelURL)
            print('needPrediction: ', needPrediction)
            print('months: ', months)

            res = getPredict.getPredict(fileURL,modelURL,needPrediction,months)
            
            print('gg : ', res)
            return Response(res)

        except (FileNotFoundError,ImportError) as e:
            obj = json.loads(str(e))
            print(type(e))
            print(obj["message"])
            return Response(obj, status=status.HTTP_404_NOT_FOUND) 

        except Exception as e: 
            print(e)
            return Response({"Error": "something wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# free users
@api_view(['GET'])
def getPredictionFree(request):
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

    print(query_params)

    if request.method == 'GET':
        fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
        needPredictionList = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
        months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1

        needPrediction = json.loads(needPredictionList)

        outputs = []

        for item in needPrediction:
            res = getPredict2.getPredict(fileURL,item,months)
            res = res[0] 
            outputs.append({ 'product': item, 'prediction': res})

        print('final outpust : ',outputs)
        return Response(outputs)

    # if request.method == 'GET':
    #     fileURL = query_params.get('fileURL') if query_params.get('fileURL') else ''
    #     needPrediction = query_params.get('needPrediction') if query_params.get('needPrediction') else ''
    #     months = int(query_params.get('monthsCount')) if query_params.get('monthsCount') else 1
    

    #     try:
    #         print("*****************************************************")
    #         url = fileURL
    #         dataset = pd.read_csv(url)
    #     except:
    #         print("*******************Dead*********************")

    
    #     if(dataset.empty):
    #         print ('CSV file is empty')
    #     else:
    #         print ('CSV file is not empty')
    #         r = str(needPrediction).replace("'",'')
    #         data = json.loads(r)

    #         for product in data:
    #             print(product)
                
    #             if product in dataset.columns:
    #                 print('\n\n\n\n\n\n\n\n')
    #                 print(product +' is exists in dataset')
    #                 getMonthlyPredictionForUsers.getPredictMonthly(fileURL, dataset, product, months)
    #                 # print(res)
    #             else:
    #                 print('\n\n\n\n\n\n\n\n')
    #                 print(product +' is not exists in dataset')
    #                 # res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
    #                 # print(res)
    #             # res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
    #             # outputs.append(res)
    #             # print(res)

    #     # r = str(needPrediction).replace("'",'')
    #     # data = json.loads(r)
    #     # data

    #     # for product in data:
    #     #     print(product)
    #     #     res = getMonthlyPredictionForUsers.getPredict(fileURL,product,months)
    #     #     # outputs.append(res)
    #     #     print(res)

    #     # print(outputs)


    #     # res = getMonthlyPredictionForUsers.getPredict(fileURL,needPrediction,months)
    #     # return Response(res)
    return HttpResponse('Welcome to cakery.Ai predict app')