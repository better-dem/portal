// feed_ajax.js
// functions supporting ajax functionality from the portal participation feed

// csrf django setup
function getCookie(name) {
    console.log("Checking for CSRF cookie")
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
	    // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }
	}
    } else {
	console.log("No CSRF cookie")
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	    xhr.setRequestHeader("X-CSRFToken", csrftoken);
	}
    }
});


//// functions to handle inline ajax forms

function setContent(elem, val){
    // WARNING: use elem.textContent, never elem.innerHTML to prevent possible javascript injection
    if (elem != null){
	elem.textContent = val;
    }
}

function revealElement(elem){
    var display_style = elem.getAttribute("data-display-style");
    if (display_style == null){
	if (elem.tagName == "SPAN"){
	    elem.style.display = "inline";					
	} else {
	    elem.style.display = "block";
	}
    } else {
	elem.style.display = display_style;
    }
}

var get_form_response_cb = function(result_element_id){
    return function(response_content, status){
	// use the content to populate child nodes and set display of child nodes of the result element
	console.log("ajax form response. status:"+status);
	console.log("ajax form response. response_content:"+response_content);
	console.log(JSON.stringify(response_content));
	// response content is a json string
	var e = document.getElementById(result_element_id);
	for (var key in response_content){
	    if (response_content.hasOwnProperty(key)){
		var val = response_content[key];
		if (key == "reveal" || key == "hide"){
		    for (var  i = 0; i < val.length; i++ ){
			var child = e.querySelector("."+val[i]);
			if (child != null){
			    if (key == "reveal"){
				revealElement(child);
			    } else if (key == "hide"){
				child.style.display = "none";
			    }
			}
		    }
		} else {
		    var child = e.querySelector("."+key)
		    if (child != null){
			setContent(child, val);
			if (child.style.display = "none"){
			    revealElement(child);
			}
		    }
		}
	    }
	}
    };
}

// submit a form
var submit_ajax_form = function(url, content, cb) {
    $.post(url, content, cb);
}

// get a map of elementID -> value for all the elements in b's data-target-element attribute
var get_form_data_object = function(b){
    var data_elements = b.getAttribute("data-target-element").split(",")
    var message = {}
    for (var i = 0; i < data_elements.length; i++){
	if (data_elements[i] != ""){
	    message[data_elements[i]] = document.getElementById(data_elements[i]).value;
	}
    }
    return JSON.stringify(message)
}

// register event triggers for a button based on its attributes
var register_event_trigger = function(b){
    b.addEventListener("click", function(e) {
	submit_ajax_form(b.getAttribute("data-target-url"),
			 get_form_data_object(b),
			 get_form_response_cb(b.getAttribute("data-result-element")))
    }, false);
}

// register ajax form event triggers on all forms on the page
var ajax_form_setup = function(){
    var portal_ajax_form_submit_buttons = document.getElementsByClassName("portal_ajax_submit");
    console.log("portal ajax form submit buttons:");
    console.log(portal_ajax_form_submit_buttons);

    for ( var i = 0; i < portal_ajax_form_submit_buttons.length; i++){
	console.log("registering button:" + i);
	var b = portal_ajax_form_submit_buttons[i];
	register_event_trigger(b)
    };
}

//// feed updating methods
var display_item_mini = function(item_id, element_id){
    var cb = function(response_content, status){
	console.log("ajax form response. status:"+status);
	console.log("ajax form response. response_content:"+response_content);
	console.log(JSON.stringify(response_content));
	var link = response_content["link"];
	var img_url = response_content["img_url"];
	var title = response_content["title"];
	var elem = document.getElementById(element_id);
	elem.innerHTML = "<a id=\"mini_item_link_"+element_id+"\"href=\""+link+"\"></a>";
	$("#mini_item_link_"+element_id).text(title)
	$("#mini_item_link_"+element_id).prepend("<img src=\""+img_url+"\">")
	$(elem).addClass('item-mini');
    }
    submit_ajax_form("/item_info/"+item_id+"/", "", cb);
}

$(document).ready(ajax_form_setup);


