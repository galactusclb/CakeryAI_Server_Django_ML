from django.contrib import admin
from django.urls import path

from .views import index,trainPredict,getPrediction_pro,getPredictionFree,getMonthlyPrediction

urlpatterns = [
    path('', index),
    path('trainPredict', trainPredict),
    path('getPredictPro', getPrediction_pro),
    path('getPredictionFree', getPredictionFree),
    path('getMonthlyPrediction', getMonthlyPrediction)
]
