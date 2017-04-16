var RELOAD_SECONDS = 1;

$(document).ready(function() {

    setTimeout(reload_children, (RELOAD_SECONDS * 1000));
});

function reload_children() {
    var children = $("#children_table");

    $.get("/refreshchildren", function(data) {
        if (data.errors === 0) {
            children.html(data.children);
        }
    });

    setTimeout(reload_children, (RELOAD_SECONDS * 1000));
}
