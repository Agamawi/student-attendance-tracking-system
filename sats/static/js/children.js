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

function prep_show_modal(id, last_name, first_name, age, grade, section, location, last_seen, school, tag) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Name</b>: `+first_name +` `+last_name+`<br>
                    <b>Age</b>: `+age+`<br>
                    <b>Grade</b>: `+grade+`<br>
                    <b>Section</b>: `+section+`<br>
                    <b>Location</b>: `+location+`<br>
                    <b>Last Seen</b>: `+last_seen+`<br>
                    <b>School</b>: `+school+`<br>
                    <b>Tag</b>: `+tag+`<br>
                </p>
                `;
    selector_body.html(code);
}