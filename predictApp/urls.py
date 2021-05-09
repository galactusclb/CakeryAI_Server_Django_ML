from django.contrib import admin
from django.urls import path

from .views import index,trainPredict,getPrediction,getPredictionEduraca,getMonthlyPrediction

urlpatterns = [
    path('', index),
    path('trainPredict', trainPredict),
    path('getPredict', getPrediction),
    path('getPredictionEduraca', getPredictionEduraca),
    path('getMonthlyPrediction', getMonthlyPrediction)
]
