function prep_show_modal(id, email, first_name, last_name, contact_number, super_admin, school) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Email</b>: `+email+`<br>
                    <b>Name</b>: `+first_name+` `+last_name+`<br>
                    <b>Contact Number</b>: `+contact_number+`<br>
                    <b>Super Admin</b>: `+super_admin+`<br>
                    <b>School</b>: `+school+`<br>
                </p>
                `;
    selector_body.html(code);
}

function prep_edit_modal(id, email, first_name, last_name, contact_number, super_admin, school, admin_id) {
    var selector_body = $(id);
    var school_code = $("#school_dropdown").html();
    var code = `
                <p>
                    <b>Email</b>:   <input type="text" class="form-control" id="edit_email" value="`+email+`"><br>
                    <b>First Name</b>:   <input type="text" class="form-control" id="edit_first_name" value="`+first_name+`"><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="edit_last_name" value="`+last_name+`"><br>
                    <b>Contact Number</b>:    <input type="text" class="form-control" id="edit_contact_number" value="`+contact_number+`"><br>
                    <b>Super Admin</b>: <input type="text" class="form-control" id="edit_super_admin" value="`+super_admin+`">
                    <b>School</b>:`+school_code+`
                </p>
                <div id="edit_id" style="display: none">`+admin_id+`</div>
                `;
    selector_body.html(code);
}

function prep_add_modal(id) {
    var selector_body = $(id);
    var school_code = $("#school_dropdown").html();
    var code = `
                <p>
                    <b>Email</b>:   <input type="text" class="form-control" id="new_email" value=""><br>
                    <b>First Name</b>:   <input type="text" class="form-control" id="new_first_name" value=""><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="new_last_name" value=""><br>
                    <b>Contact Number</b>:    <input type="text" class="form-control" id="new_contact_number" value=""><br>
                    <b>Super Admin</b>: <input type="text" class="form-control" id="new_super_admin" value=""><br>
                    <b>School</b>:   `+school_code+`<br>
                </p>
                `;
    selector_body.html(code);
}

function save_edit() {

    var data_object = {
        admin_id: $("#edit_id").html(),
        email:$("#edit_email").val(),
        first_name: $("#edit_first_name").val(),
        last_name: $("#edit_last_name").val(),
        contact_number: $("#edit_contact_number").val(),
        super_admin: $("#edit_super_admin").val(),
        school: $('#select_dropdown_option').val()
    };

    $.ajax({
      type: "POST",
      url: '/adminedit',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}

function delete_entry(id) {
    $.ajax({
      type: "POST",
      url: '/admindelete',
      data: {id: id},
      success: function(){
        location.reload();
      }
    });
}

function add_entry() {

    var data_object = {
        email:$("#new_email").val(),
        first_name: $("#new_first_name").val(),
        last_name: $("#new_last_name").val(),
        contact_number: $("#new_contact_number").val(),
        super_admin: $("#new_super_admin").val(),
        school: $('#select_dropdown_option').val()
    };

    $.ajax({
      type: "POST",
      url: '/adminadd',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}
