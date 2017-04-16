function prep_show_modal(id, last_name, first_name, relationship, occupation) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Name</b>: `+first_name +` `+last_name+`<br>
                    <b>Relationship</b>: `+relationship+`<br>
                    <b>Occupation</b>: `+occupation+`
                </p>
                `;
    selector_body.html(code);
}

function prep_edit_modal(id, last_name, first_name, relationship, occupation, user_id) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>First Name</b>:   <input type="text" class="form-control" id="edit_first_name" value="`+first_name+`"><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="edit_last_name" value="`+last_name+`"><br>
                    <b>Relationship</b>: <input type="text" class="form-control" id="edit_relationship" value="`+relationship+`"><br>
                    <b>Occupation</b>:   <input type="text" class="form-control" id="edit_occupation" value="`+occupation+`">
                </p>
                <div id="edit_id" style="display: none">`+user_id+`</div>
                `;
    selector_body.html(code);
}

function prep_add_modal(id) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Email</b>: <input type="text" class="form-control" id="new_email" value=""><br>
                    <b>First Name</b>:   <input type="text" class="form-control" id="new_first_name" value=""><br>
                    <b>Last Name</b>:    <input type="text" class="form-control" id="new_last_name" value=""><br>
                    <b>Relationship</b>: <input type="text" class="form-control" id="new_relationship" value=""><br>
                    <b>Occupation</b>:   <input type="text" class="form-control" id="new_occupation" value="">
                </p>
                `;
    selector_body.html(code);
}

function save_edit() {

    var data_object = {
        user_id: $("#edit_id").html(),
        first_name: $("#edit_first_name").val(),
        last_name: $("#edit_last_name").val(),
        relationship: $("#edit_relationship").val(),
        occupation: $("#edit_occupation").val(),
    };

    $.ajax({
      type: "POST",
      url: '/guardianedit',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}

function delete_entry(id) {
    $.ajax({
      type: "POST",
      url: '/guardiandelete',
      data: {id: id},
      success: function(){
        location.reload();
      }
    });
}

function add_entry() {

    var data_object = {
        email: $("#new_email").val(),
        first_name: $("#new_first_name").val(),
        last_name: $("#new_last_name").val(),
        relationship: $("#new_relationship").val(),
        occupation: $("#new_occupation").val()
    };

    $.ajax({
      type: "POST",
      url: '/guardianadd',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}
