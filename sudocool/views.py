import requests

from django.shortcuts import get_object_or_404, render, redirect

from sudocool.models import SudocoolBoard
from sudocool.forms import SolveForm, GetPuzzleForm
from sudocool.solve.board import Board
from sudocool.solve.solver import BoardSolver

section_size = 3;
num_sections = section_size**2;

def index(request, puzzle = None):
    context = {'range': range(num_sections)}
    if puzzle != None:
        b = Board()
        b.populateByRow(puzzle)
        context['puzzle'] = b.printBySection()
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

    # generate Board for the given sudocoolboard, and solve it
    b = Board()
    b.populateBySection(sudocoolboard.sudocoolData)
    bs = BoardSolver(b)
    bs.solve()

    # render a response containing the solution
    return render(request, 'sudocool/solution.html', {'range': range(num_sections), 'solution': bs.board.printBySection()})

def puzzle(request):
    if request.method == 'POST':
        form = GetPuzzleForm(request.POST)
        if not form.is_valid():
            form.cleaned_data["puzzleURL"] = "http://sudoku.com.au"
        try:
            html = requests.get(form.cleaned_data["puzzleURL"]).text
            index = html.find("var iGridUnsolved= new Array(")+len("var iGridUnsolved= new Array(")
            array = html[index:index+161]
            return redirect('sudocool:index', array)
        except (ValueError):
            return redirect('sudocool:index')
    return redirect('sudocool:index')
