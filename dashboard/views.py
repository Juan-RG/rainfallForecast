from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
  print("Hello")
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def dashboard(request):
  print("Hello")
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())
