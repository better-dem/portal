// var ajax_text_field_data = {}

function attach_ajax_string_listener(text_field_id) {
    console.log("Attaching ajax string listener to"+ text_field_id)

    // ajax_text_field_data[text_field_id] = $("#"+text_field_id).val()

    // $("#"+text_field_id).change(function() {
    // 	$.post("/autocomplete/", 
    // 	      {"str_beginning": $("#"+text_field_id).val()},
    // 	      function (data) {
    // 		  $("#"+text_field_id).autocomplete(data);
    // 		  // ajax_text_field_data[text_field_id] = data;
		  
    // 	      })
    // });

    $("#"+text_field_id).autocomplete({
	serviceUrl: '/autocomplete/',
	type: "POST",
    })
}
