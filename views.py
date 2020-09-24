from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def index(request):
  # Get URL of page to visit
  url = request.GET.get('url')
  
  # Get page
  r = requests.get(url)
  html = r.content

  # Parse html using BeautifulSoup
  soup = BeautifulSoup(html, 'html.parser')

  # Modify href relative links to absolute links
  parsed_uri = urlparse(url)
  result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
  PREPEND = 'https://access-blocked-sites.herokuapp.com?url={}'.format(result)
  PREPEND_REL = 'https://access-blocked-sites.herokuapp.com?url={}'.format(url)
  links = soup.find_all('a')
  for link in links:
    try:
      href = link.get('href')
      # href = "/a/b/c" , i.e. absolute path
      if 'http' not in href and href.startswith('/'):
        link['href'] = PREPEND + href
      # href = "./a/b/c" OR "a/b/c" , i.e. relative path
      elif 'http' not in href:
        link['href'] = PREPEND_REL + href
    except:
      # if any <a> tag fails to parse, ignore that tag
      continue

  # Return page
  return HttpResponse(str(soup))

