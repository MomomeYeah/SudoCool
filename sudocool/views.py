from django.shortcuts import get_object_or_404, render, redirect

from sudocool.models import SudocoolBoard
from sudocool.forms import SolveForm

def index(request):
    return render(request, 'sudocool/index.html', {'range': range(9)})

def solve(request):
    if request.method == 'POST':
        form = SolveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            board = SudocoolBoard.objects.create_sudocoolboard(cd['sudocoolData'])
            return redirect('sudocool:solution', board.id)
    return redirect('sudocool:index')

def solution(request, sudocoolboard_id):
    solution = get_object_or_404(SudocoolBoard, pk = sudocoolboard_id)
    return render(request, 'sudocool/solution.html', {'range': range(9), 'solution': solution})
