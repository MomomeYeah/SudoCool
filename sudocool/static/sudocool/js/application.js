$(document).ready(function() {
    $("#category_id").change(function() {
        $("#addCategoryForm").submit();
    })

    $(".removeCategoryForm a").click(function() {
        $(this).parents(".removeCategoryForm").submit();
    })

    $(".item_id").change(function() {
        $(this).parents(".addItemForm").submit();
    })

    $(".removeItemForm a").click(function() {
        $(this).parents(".removeItemForm").submit();
    })

    $(".showHideCategory").click(function() {
        categoryContents = $(this).parents("div.category").find("div.categoryContents").toggle();
        $(this).find(".showCategory").toggle();
        $(this).find(".hideCategory").toggle();
    })

    $(".itemContainer").sortable({
      axis: "y",
      scroll: true,
      placeholder: "sortable-item-placeholder",
      forcePlaceholderSize: true,
      cursor: "move",
      revert: false,
      stop: function(event, ui) {
        reorderItemForm = ui.item.find(".reorderItemForm");
        reorderItemForm.find("input[name='item_position']").val(ui.item.index());
        reorderItemForm.submit();
      }
    });

    $(".categoryContainer").sortable({
      axis: "y",
      scroll: true,
      placeholder: "sortable-category-placeholder",
      forcePlaceholderSize: true,
      cursor: "move",
      revert: false,
      handle: ".categoryHandle",
      stop: function(event, ui) {
        reorderItemForm = ui.item.find(".reorderCategoryForm");
        reorderItemForm.find("input[name='category_position']").val(ui.item.index());
        reorderItemForm.submit();
      }
    });

})