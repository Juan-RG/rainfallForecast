from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def help(request):
  template = loader.get_template('help.html')
  return HttpResponse(template.render())

