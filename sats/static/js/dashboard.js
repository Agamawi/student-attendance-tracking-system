var RELOAD_SECONDS = 1;

$(document).ready(function() {

    setTimeout(reload_children, (RELOAD_SECONDS * 1000));
});

function reload_children() {
    var absent_children = $("#absent_children_table");
    var late_children = $("#late_children_table");

    $.get("/refreshabsentlatechildren", function(data) {
        if (data.errors === 0) {
            absent_children.html(data.absent_children);
            late_children.html(data.late_children);
        }
    });

    setTimeout(reload_children, (RELOAD_SECONDS * 1000));
}
