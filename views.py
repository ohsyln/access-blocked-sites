from django.shortcuts import render
    
from django.http import HttpResponse

from .models import Greeting

import requests

def index(request):
  # Get URL of page to visit
  url = request.GET.get('url')
  
  # Get page
  r = requests.get(url)
  html = r.content

  # Return page
  return HttpResponse(html)

