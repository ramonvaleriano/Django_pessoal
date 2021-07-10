from django.shortcuts import render
from django.http import HttpResponse

def index(requeste):
    return HttpResponse('<h1>Receitas</h1>')
