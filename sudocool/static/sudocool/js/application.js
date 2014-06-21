$(document).ready(function() {
    $("#solveSudocoolForm").submit(function() {
        var sudocoolCells = new Array();
        var cells = $(this).find(".sudocoolItem");
        $.each(cells, function(i, value) {
            sudocoolCells[sudocoolCells.length] = $(value).val();
        });

        var input = $("<input>").attr("type", "hidden").attr("name", "sudocoolData").val(sudocoolCells.toString());
        $(this).append($(input));
    })
})