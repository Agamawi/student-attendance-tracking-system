function prep_show_modal(id, name, building_no, street, city, zone_no, start_time) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Name</b>: `+name+`<br>
                    <b>Building No.</b>: `+building_no+`<br>
                    <b>Street</b>: `+street+`<br>
                    <b>City</b>: `+city+`<br>
                    <b>Zone No.</b>: `+zone_no+`<br>
                    <b>Start Time</b>: `+start_time+`
                </p>
                `;
    selector_body.html(code);
}

function prep_edit_modal(id, name, building_no, street, city, zone_no, start_time, school_id) {
    var selector_body = $(id);
    var code = `
                <p>
                    <b>Name</b>:   <input type="text" class="form-control" id="edit_name" value="`+name+`"><br>
                    <b>Building No.</b>:    <input type="text" class="form-control" id="edit_building_no" value="`+building_no+`"><br>
                    <b>Street</b>:    <input type="text" class="form-control" id="edit_street" value="`+street+`"><br>
                    <b>City</b>: <input type="text" class="form-control" id="edit_city" value="`+city+`"><br>
                    <b>Zone No.</b>:   <input type="text" class="form-control" id="edit_zone_no" value="`+zone_no+`"><br>
                    <b>Start Time</b>:   <input type="text" class="form-control" id="edit_start_time" value="`+start_time+`">
                </p>
                <div id="edit_id" style="display: none">`+school_id+`</div>
                `;
    selector_body.html(code);
}

function prep_add_modal(id) {
    var selector_body = $(id);
    var code = `
                <p>
                <b>Name</b>:   <input type="text" class="form-control" id="new_name" value=""><br>
                <b>Building No.</b>:    <input type="text" class="form-control" id="new_building_no" value=""><br>
                <b>Street</b>:    <input type="text" class="form-control" id="new_street" value=""><br>
                <b>City</b>: <input type="text" class="form-control" id="new_city" value=""><br>
                <b>Zone No.</b>:   <input type="text" class="form-control" id="new_zone_no" value=""><br>
                <b>Start Time</b>:   <input type="text" class="form-control" id="new_start_time" value="">
                </p>
                `;
    selector_body.html(code);
}

function save_edit() {

    var data_object = {
        school_id: $("#edit_id").html(),
        name: $("#edit_name").val(),
        building_no: $("#edit_building_no").val(),
        street: $("#edit_street").val(),
        city: $("#edit_city").val(),
        zone: $("#edit_zone_no").val(),
        start_time: $("#edit_start_time").val()
    };

    $.ajax({
      type: "POST",
      url: '/schooledit',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}

function delete_entry(id) {
    $.ajax({
      type: "POST",
      url: '/schooldelete',
      data: {id: id},
      success: function(){
        location.reload();
      }
    });
}

function add_entry() {

    var data_object = {
        name: $("#new_name").val(),
        building_no: $("#new_building_no").val(),
        street: $("#new_street").val(),
        city: $("#new_city").val(),
        zone: $("#new_zone_no").val(),
        start_time: $("#new_start_time").val()
    };

    $.ajax({
      type: "POST",
      url: '/schooladd',
      data: data_object,
      success: function(){
        location.reload();
      }
    });

}
