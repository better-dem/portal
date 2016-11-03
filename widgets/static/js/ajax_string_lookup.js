function attach_ajax_string_listener(ajax_url, text_field_id) {
    console.log("Attaching ajax string listener to"+ text_field_id)

    // using: https://github.com/devbridge/jQuery-Autocomplete
    // version 1.2.26

    $("#"+text_field_id).autocomplete({
	serviceUrl: ajax_url,
	type: "POST",
    })
}
