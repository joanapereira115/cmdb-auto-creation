from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from colored import fg, bg, attr

blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

def index(request):
    print(blue + ">>> " + reset + "Viewing homepage.")
    return render(request, 'index.html', {})
