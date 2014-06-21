from django.shortcuts import render
#from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from sudocool.forms import SolveForm

def index(request):
    return render(request, 'sudocool/index.html', {'range': range(9)})

def solve(request):
    if request.method == 'POST':
        form = SolveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sudocoolData = cd['sudocoolData']
    return HttpResponseRedirect(reverse('sudocool:index'))