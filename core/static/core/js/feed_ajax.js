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

//// feed updating methods
var env = new nunjucks.Environment(new nunjucks.WebLoader("/js_templates"));
var escapeJSMap = {
    '\\': '\\u005C',
    '\'': '\\u0027',
    '"': '\\u0022',
    '>': '\\u003E',
    '<': '\\u003C',
    '&': '\\u0026',
    '=': '\\u003D',
    '-': '\\u002D',
    ';': '\\u003B'
};

env.addFilter('escapejs', function(str) {
    return str.replace(/["'><&=\-;\\]/g, function(ch) {
	return escapeJSMap[ch];
    });
});


// mini items go on the bottom of participate views as recommendations
var display_item_mini = function(item_id, element_id){
    var cb = function(response_content, status){
	console.log("ajax form response. status:"+status);
	console.log("ajax form response. response_content:"+response_content);
	console.log(JSON.stringify(response_content));
	var link = response_content["link"];
	var img_url = response_content["img_url"];
	var title = response_content["title"];
	if (title.length > 30){
	    title = title.substring(0,30)+"..."
	}
	var new_tab = response_content["external_link"];
	var elem = document.getElementById(element_id);
	if (new_tab){
	    elem.innerHTML = "<a target=\"_blank\" id=\"mini_item_link_"+element_id+"\"href=\""+link+"\"></a>";
	} else {
	    elem.innerHTML = "<a id=\"mini_item_link_"+element_id+"\"href=\""+link+"\"></a>";
	}
	$("#mini_item_link_"+element_id).text(title)
	$("#mini_item_link_"+element_id).prepend("<img src=\""+img_url+"\">")
	$(elem).addClass('item-mini');
    }
    submit_ajax_form("/item_info/"+item_id+"/", "", cb);
}

// feed items populate news feeds, admin views, and are also used within participate pages
var display_feed_item = function(item_id, element_id, app_name){
    var cb = function(response_content, status){
	console.log("ajax form response. status:"+status);
	console.log("ajax form response. response_content:"+response_content);
	console.log(JSON.stringify(response_content));
        // TODO: update html and content

	var res = env.render(app_name+"/feed_item.html", response_content);
	$("#"+element_id).html(res)
        // TODO: call javascript methods for inline displays, set up ajax within items, etc.
    }
    submit_ajax_form("/apps/"+app_name+"/item_info/"+item_id, "", cb);
}

var get_feed_recommendations_next_page = function(){
    var cb = function(response_content, status){
	console.log("ajax form response. status:"+status);
	console.log("ajax form response. response_content:"+response_content);
	console.log(JSON.stringify(response_content));
	var item_recommendations = response_content["recommendations"]
	for (i = 0; i < item_recommendations.length; i++){
	    current_feed_contents.push(item_recommendations[i][0])
	    var eid = "feed_item_"+(item_recommendations[i][0]);
	    $("#feed").append("<div id=\""+eid+"\"></div>");
	    display_feed_item(item_recommendations[i][0], eid, item_recommendations[i][1]);
	}
    }
    submit_ajax_form("/feed_recommendations/", JSON.stringify({"current_feed_contents":current_feed_contents}), cb);
}

var current_feed_contents = [];


