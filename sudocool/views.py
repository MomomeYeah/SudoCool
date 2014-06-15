from django.shortcuts import render
#from django.shortcuts import get_object_or_404, render
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'sudocool/index.html')