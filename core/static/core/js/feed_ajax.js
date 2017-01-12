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
    console.log("tag has a data-display-style"+display_style)
    if (display_style == null){
	if (elem.tagName == "SPAN"){
	    console.log("elem is a span!")
	    elem.style.display = "inline";					
	} else {
	    elem.style.display = "block";
	}
    } else {
	elem.style.display = display_style;
    }
}

function get_form_response_cb(result_element_id){
    return function(response_content, status){
	// use the content to populate child nodes and set display of child nodes of the result element
	console.log("ajax form response. status:"+status)
	console.log("ajax form response. response_content:"+response_content)
	console.log(JSON.stringify(response_content))
	// response content is a json string
	var e = document.getElementById(result_element_id);
	for (var key in response_content){
	    if (response_content.hasOwnProperty(key)){
		var val = response_content[key];
		if (key == "reveal" || key == "hide"){
		    for ( i = 0; i < val.length; i++ ){
			var child = e.querySelector("."+val[i]);
			if (child != null){
			    if (key == "reveal"){
				revealElement(child);
			    } else if (key == "hide"){
				child.style.display = "none"
			    }
			}
		    }
		} else {
		    var child = e.querySelector("."+key)
		    if (child != null){
			setContent(child, val)
			if (child.style.display = "none"){
			    revealElement(child);
			}
		    }
		}
	    }
	}
    }
}

// submit a form
function submit_ajax_form(url, content, cb) {
    $.post(url, content, cb)
}

// register event triggers on all forms on the page based on their attributes
var portal_ajax_form_submit_buttons = document.getElementsByClassName("portal_ajax_submit");
console.log("portal ajax form submit buttons:")
console.log(portal_ajax_form_submit_buttons)

for ( i = 0; i < portal_ajax_form_submit_buttons.length; i++){
    console.log("registering button:" + i)
    var b = portal_ajax_form_submit_buttons[i]
    b.addEventListener("click", function(e) {
	submit_ajax_form(b.getAttribute("data-target-url"), 
			 document.getElementById(b.getAttribute("data-target-element")).value,
			 get_form_response_cb(b.getAttribute("data-result-element")))
    }, false);
};

