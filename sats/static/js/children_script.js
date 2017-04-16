function prep_edit_modal(id, last_name, first_name, age, grade, section, location, last_seen, school, school_id, tag, user_id) {
    var selector_body = $(id);
    var school_code = $("#school_dropdown").html();
    var code = `
                <p class="prep_edit_modal123">
                    <b>First Name</b>:   <input type="text" class="form-control" id="edit_first_name" value="`+first_name+`"><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="edit_last_name" value="`+last_name+`"><br>
                    <b>Age</b>: <input type="text" class="form-control" id="edit_age" value="`+age+`"><br>
                    <b>Grade</b>:   <input type="text" class="form-control" id="edit_grade" value="`+grade+`"><br>
                    <b>Section</b>:   <input type="text" class="form-control" id="edit_section" value="`+section+`"><br>
                    <b>School</b>: `+school_code+`<br>
                    <b>Tag</b>:   <input type="text" class="form-control" id="edit_tag" value="`+tag+`">
                </p>
                <div id="edit_id" style="display: none">`+user_id+`</div>
                `;
    selector_body.html(code);
    $(".prep_edit_modal123 > select").val(school_id);
}

function prep_add_modal(id) {
    var selector_body = $(id);
    var school_code = $("#school_dropdown").html();
    var code = `
                <p>
                    <b>First Name</b>:   <input type="text" class="form-control" id="new_first_name" value=""><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="new_last_name" value=""><br>
                    <b>Age</b>: <input type="text" class="form-control" id="new_age" value=""><br>
                    <b>Grade</b>:   <input type="text" class="form-control" id="new_grade" value=""><br>
                    <b>Section</b>:   <input type="text" class="form-control" id="new_section" value=""><br>
                    <b>School</b>: `+school_code+`<br>
                    <b>Tag</b>:   <input type="text" class="form-control" id="new_tag" value=""><br>
                </p>
                `;
    selector_body.html(code);
}

function save_edit() {

    var data_object = {
        user_id: $("#edit_id").html(),
        first_name: $("#edit_first_name").val(),
        last_name: $("#edit_last_name").val(),
        age: $("#edit_age").val(),
        grade: $("#edit_grade").val(),
        section: $("#edit_section").val(),
        school: $('#select_dropdown_option').val(),
        tag: $('#edit_tag').val()
    };

    $.ajax({
      type: "POST",
      url: "/childedit",
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}

function delete_entry(id) {
    $.ajax({
      type: "POST",
      url: "/childdelete",
      data: {id: id},
      success: function(){
        location.reload();
      }
    });
}

function add_entry() {

    var data_object = {
        first_name: $("#new_first_name").val(),
        last_name: $("#new_last_name").val(),
        age: $("#new_age").val(),
        grade: $("#new_grade").val(),
        section: $("#new_section").val(),
        school: $('#select_dropdown_option').val(),
        tag: $("#new_tag").val()
    };

    $.ajax({
      type: "POST",
      url: "/childadd",
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}
