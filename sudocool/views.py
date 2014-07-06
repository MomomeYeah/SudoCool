import urllib2

from django.shortcuts import get_object_or_404, render, redirect

from sudocool.models import SudocoolBoard
from sudocool.forms import SolveForm, GetPuzzleForm
from sudocool.solve import *

def index(request, puzzle = None):
    context = {'range': range(9)}
    if puzzle != None:
        context['puzzle'] = puzzle
    return render(request, 'sudocool/index.html', context)

def solve(request):
    if request.method == 'POST':
        form = SolveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            board = SudocoolBoard.objects.create_sudocoolboard(cd['sudocoolData'])
            return redirect('sudocool:solution', board.id)
    return redirect('sudocool:index')

def solution(request, sudocoolboard_id):
    sudocoolboard = get_object_or_404(SudocoolBoard, pk = sudocoolboard_id)
    b = board(sudocoolboard.sudocoolData)
    b.setupBoard()
    b.solveBoard()
    return render(request, 'sudocool/solution.html', {'range': range(9), 'solution': b.printBoard()})

def puzzle(request):
    if request.method == 'POST':
        form = GetPuzzleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                html = urllib2.urlopen(cd['puzzleURL']).read()
                index = html.find("var iGridUnsolved= new Array(")+len("var iGridUnsolved= new Array(")
                array = html[index:index+161]
                return redirect('sudocool:index', array)
            except (ValueError):
                return redirect('sudocool:index')
    return redirect('sudocool:index')
