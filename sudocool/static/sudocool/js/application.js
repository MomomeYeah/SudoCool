function isValidSudokuNumber(n) {
    if(n === '') return true;
    var num = Number(n);
    return !isNaN(num) && num === Math.floor(num) && n > 0 && n <= 9;
}

function populateSolution() {
    var solutionString = $("#solutionString").val();
    if(typeof solutionString !== "undefined" && solutionString !== '') {
        var solutionItems = solutionString.split(',');
        var sudocoolCells = $(".sudocoolItem");
        $.each(sudocoolCells, function(i, value) {
            $(this).val(solutionItems[i]);
        })
    }
}

$(document).ready(function() {
    populateSolution();

    $("#solveSudocoolForm").submit(function(event) {
        $(this).find("div.sudocoolCol").removeClass("badCol");

        var sudocoolCells = new Array();
        var cells = $(this).find(".sudocoolItem");
        $.each(cells, function(i, value) {
            var cellData = $(value).val();
            if (!isValidSudokuNumber(cellData)) {
                $(this).parent().addClass("badCol");
                event.preventDefault();
            }
            sudocoolCells[sudocoolCells.length] = cellData;
        });

        var input = $("<input>").attr("type", "hidden").attr("name", "sudocoolData").val(sudocoolCells.toString());
        $(this).append($(input));
    })
})