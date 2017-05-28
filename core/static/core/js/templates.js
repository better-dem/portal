(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["core/feed_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<div class=\"panel panel-default\">\n    <div class=\"panel-heading\"><a ";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("custom_link_content"))(env, context, frame, runtime, function(t_2,t_1) {
if(t_2) { cb(t_2); return; }
output += t_1;
output += " href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"link"), env.opts.autoescape);
output += "\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"label"), env.opts.autoescape);
output += "</a></div>\n    <div class=\"panel-body\">\n\n";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("display_image"))(env, context, frame, runtime, function(t_4,t_3) {
if(t_4) { cb(t_4); return; }
output += t_3;
output += "\n\n\t<span class=\"item_content\">\n\t  <div>\n\t  ";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("custom_item_content"))(env, context, frame, runtime, function(t_6,t_5) {
if(t_6) { cb(t_6); return; }
output += t_5;
output += "\n\t  </div>\n\t</span>\n    </div>\n    <div class=\"panel-footer\">\n      ";
frame = frame.push();
var t_9 = runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"tags");
if(t_9) {var t_8 = t_9.length;
for(var t_7=0; t_7 < t_9.length; t_7++) {
var t_10 = t_9[t_7];
frame.set("tag", t_10);
frame.set("loop.index", t_7 + 1);
frame.set("loop.index0", t_7);
frame.set("loop.revindex", t_8 - t_7);
frame.set("loop.revindex0", t_8 - t_7 - 1);
frame.set("loop.first", t_7 === 0);
frame.set("loop.last", t_7 === t_8 - 1);
frame.set("loop.length", t_8);
output += "<span class=\"label label-default\">";
output += runtime.suppressValue(t_10, env.opts.autoescape);
output += "</span> ";
;
}
}
frame = frame.pop();
output += "\n      <a style=\"float: right; padding-left: 10px; cursor:pointer;\" data-toggle=\"tooltip\" title=\"Bookmark this item\" onclick=\"submit_ajax_form('/add_bookmark/', JSON.stringify({'item_id':";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "}));\"><span class=\"glyphicon glyphicon-bookmark\"></span></a>\n      <a style=\"float: right; padding-left: 10px;\" href=\"/report_issues";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"link"), env.opts.autoescape);
output += "\" data-toggle=\"tooltip\" title=\"Report a problem with this item\"><span class=\"glyphicon glyphicon-ban-circle\"></span></a>\n      <a style=\"float: right; padding-left: 10px; cursor:pointer;\" data-toggle=\"tooltip\" title=\"Share this item on Facebook\" onclick=\"share_og('";
output += runtime.suppressValue(env.getFilter("escapejs").call(context, runtime.contextOrFrameLookup(context, frame, "site")), env.opts.autoescape);
output += runtime.suppressValue(env.getFilter("escapejs").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"link")), env.opts.autoescape);
output += "', '";
output += runtime.suppressValue(env.getFilter("escapejs").call(context, runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"label")), env.opts.autoescape);
output += "');\"> <span class=\"glyphicon glyphicon-share\" ></span>\n      </a>\n      <div class=\"clearfix\"></div>\n    </div>\n</div>\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
})})});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_custom_link_content(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_display_image(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += "\t<span>\n\t<img src=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"img_url"), env.opts.autoescape);
output += "\" class=\"img-thumbnail\" width=\"90\" height=\"90\">\n\t</span>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_custom_item_content(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += "\n\t  ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"display"), env.opts.autoescape);
output += "\n\t  ";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
b_custom_link_content: b_custom_link_content,
b_display_image: b_display_image,
b_custom_item_content: b_custom_item_content,
root: root
};

})();
})();

(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["interactive_visualization/feed_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
env.getTemplate("core/feed_item.html", true, "interactive_visualization/feed_item.html", false, function(t_2,_parentTemplate) {
if(t_2) { cb(t_2); return; }
parentTemplate = _parentTemplate
for(var t_1 in parentTemplate.blocks) {
context.addBlock(t_1, parentTemplate.blocks[t_1]);
}
output += "\n";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("display_image"))(env, context, frame, runtime, function(t_4,t_3) {
if(t_4) { cb(t_4); return; }
output += t_3;
output += "\n";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("custom_item_content"))(env, context, frame, runtime, function(t_6,t_5) {
if(t_6) { cb(t_6); return; }
output += t_5;
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
})})});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_display_image(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += "\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_custom_item_content(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += "\n\n\n<h3>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_name"), env.opts.autoescape);
output += "</h3>\n<div id=\"IV_anchor_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\"></div>\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"switch_variable")) {
output += "\n<div style=\"padding-bottom: 10px;\">\n  <h4>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"switch_title"), env.opts.autoescape);
output += "</h4>\n  <div style=\"padding-bottom: 5px;\">\n  ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"switch_note"), env.opts.autoescape);
output += "\n  </div>\n  <div id=\"dc_switch_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\"></div>\n</div>\n";
;
}
output += "\n\n<div class=\"row\" style=\"padding-left: 15px;\">\n  ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "\n  <div id=\"bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\">\n    <h4 style=\"display: inline;\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_title"), env.opts.autoescape);
output += "</h4>\n    <a class=\"reset\" href=\"javascript:bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll();dc.redrawAll();\" style=\"display: none;\">reset</a>\n\n    <div class=\"clearfix\"></div>\n  </div>\n  ";
;
}
output += "\n\n  ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "\n  <div id=\"pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\">\n    <h4 style=\"display: inline;\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_title"), env.opts.autoescape);
output += "</h4>\n    <a class=\"reset\" href=\"javascript:pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll();dc.redrawAll();\" style=\"display: none;\">reset</a>\n\n    <div class=\"clearfix\"></div>\n  </div>\n  ";
;
}
output += "\n\n  ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "\n  <div id=\"bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\">\n    <h4 style=\"display: inline;\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_title"), env.opts.autoescape);
output += "</h4>\n    <a class=\"reset\" href=\"javascript:bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll();dc.redrawAll();\" style=\"display: none;\">reset</a>\n\n    <div class=\"clearfix\"></div>\n  </div>\n  ";
;
}
output += "\n\n  ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "\n  <div id=\"pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\">\n    <h4 style=\"display: inline;\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_title"), env.opts.autoescape);
output += "</h4>\n    <a class=\"reset\" href=\"javascript:pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll();dc.redrawAll();\" style=\"display: none;\">reset</a>\n\n    <div class=\"clearfix\"></div>\n  </div>\n  ";
;
}
output += "\n</div>\n\n<div style=\"padding-left: 15px;\">\n  <h4>Methodology Note</h4>\n  ";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"methodology_note"), env.opts.autoescape);
output += "<br>\n  Find out more about our methodology <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"methodology_url"), env.opts.autoescape);
output += "\">here</a>\n</div>\n\n<script>\n\n// declare charts as globals\nvar iv_data_loaded_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = false;\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "var bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = null;";
;
}
output += "\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "var bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = null;";
;
}
output += "\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "var pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = null;";
;
}
output += "\n";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "var pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = null;";
;
}
output += "\n\nvar handle_dc_switch_toggle_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = function(elem){}\n\nvar resize_IV_charts_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = function(){\n     if (!iv_data_loaded_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart){\n\t return;\n     }\n\n     var horizontal_space_available = document.getElementById(\"IV_anchor_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\").parentNode.clientWidth - 30;\n     var num_charts = 0;\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "num_charts += 1;";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "num_charts += 1;";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "num_charts += 1;";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "num_charts += 1;";
;
}
output += "\n     var width = 300;\n     if (horizontal_space_available > num_charts * 350){\n\t width = d3.min([Math.floor(horizontal_space_available / num_charts), 500]);\n     } else {\n\t width = d3.min([Math.floor(horizontal_space_available), 500]);\n     }\n     \n     var height = d3.max([Math.floor(width * 1.0/2), 200])\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.width(width).height(height).rescale().redraw();";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.width(width).height(height).rescale().redraw();";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.width(width).height(height).redraw();";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.width(width).height(height).redraw();";
;
}
output += "\n };\n \n$( window ).resize(function() {\n     resize_IV_charts_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "();\n});\n\n\n\n// No spaces around commas! This is important!! :( \nd3.csv(\"/apps/interactive_visualization/customActionCsvData/";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\", function(parsed_data_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "){\n     console.log('parsed data', parsed_data_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n     var bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "=5 // this value is overwritten\n     var num_bins_IV = 10;\n     var xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = crossfilter(parsed_data_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ");\n\n     //// bar chart 1\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "\n     var xExtent = d3.extent(parsed_data_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ", function(d) { return +d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable"), env.opts.autoescape);
output += "\"]; });\n     var min = xExtent[0];\n     var max = xExtent[1];\n     bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = 1.0 * (max - min) / num_bins_IV;\n     var xMin = min - bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\n     var xMax = max + bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\n     console.log(min, max, xMin, xMax, bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n\n     var bar1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".dimension(function(d) {return +d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable"), env.opts.autoescape);
output += "\"];}),\n\t number_of_samples = bar1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".group(function(d) { return 1.0 * bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " * Math.floor(1.0 * d / bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")});\n\n     bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = dc.barChart(\"#bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\"); \n     bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart\n    .width(350)\n    .height(200)\n    .dimension(bar1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .group(number_of_samples)\n    .turnOnControls(true)\n    .x(d3.scale.linear().domain([xMin, xMax]))\n    .xAxisPadding(bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .xUnits(dc.units.fp.precision(bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "))\n    .elasticY(true)\n    .brushOn(true)\n    .yAxisLabel(\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_y_label"), env.opts.autoescape);
output += "\")\n    .xAxisLabel(\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_x_label"), env.opts.autoescape);
output += "\")\n     ";
;
}
output += "\n\n     //// bar chart 2\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "\n     var xExtent = d3.extent(parsed_data_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ", function(d) { return +d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable"), env.opts.autoescape);
output += "\"]; });\n     var min = xExtent[0];\n     var max = xExtent[1];\n     bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = 1.0 * (max - min) / num_bins_IV;\n     var xMin = min - bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\n     var xMax = max + bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\n     console.log(min, max, xMin, xMax, bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n\n     var bar2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".dimension(function(d) {return +d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable"), env.opts.autoescape);
output += "\"];}),\n\t number_of_samples = bar2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".group(function(d) { return bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " * Math.floor(1.0 * d / bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")});\n\n     bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = dc.barChart(\"#bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\"); \n     bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart\n    .width(350)\n    .height(200)\n    .dimension(bar2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .group(number_of_samples)\n    .turnOnControls(true)\n    .x(d3.scale.linear().domain([xMin, xMax]))\n    .xAxisPadding(bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .xUnits(dc.units.fp.precision(bin_width_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "))\n    .elasticY(true)\n    .brushOn(true)\n    .yAxisLabel(\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_y_label"), env.opts.autoescape);
output += "\")\n    .xAxisLabel(\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_x_label"), env.opts.autoescape);
output += "\")\n     ";
;
}
output += "\n\n     //// pie chart 1 (for now, I'm actually using row charts instead of pie charts)\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "\n     var pie1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".dimension(function(d) {return d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable"), env.opts.autoescape);
output += "\"];}),\n\t number_of_samples = pie1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".group();\n\n     pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = dc.pieChart(\"#pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\");\n     pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart\n    .width(350)\n    .height(200)\n    .dimension(pie1_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .group(number_of_samples)\n    .legend(dc.legend());\n     ";
;
}
output += "\n\n     //// pie chart 2 (for now, I'm actually using row charts instead of pie charts)\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "\n     var pie2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".dimension(function(d) {return d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable"), env.opts.autoescape);
output += "\"];}),\n\t number_of_samples = pie2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".group();\n\n     pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = dc.pieChart(\"#pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_div\");\n     pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart\n    .width(350)\n    .height(200)\n    .dimension(pie2_dimension_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ")\n    .group(number_of_samples)\n    .legend(dc.legend());\n     ";
;
}
output += "\n\n     //// Render all charts\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.render()";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.render()";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie1_variable")) {
output += "pie1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.render()";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"pie2_variable")) {
output += "pie2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.render()";
;
}
output += "\n\n     //// set up a data toggle using radio buttons\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"switch_variable")) {
output += "\n     var toggl_dim_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = xfilter_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".dimension(function(d) {return d[\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"switch_variable"), env.opts.autoescape);
output += "\"];});\n     handle_dc_switch_toggle_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = function(elem){\n\t $('.dc_switch_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "').removeClass(\"btn-info\");\n\t $('.dc_switch_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "').addClass(\"btn-default\");\n\t $(elem).removeClass(\"btn-default\");\n\t $(elem).addClass(\"btn-info\");\n\t var val = elem.value;\n\t toggl_dim_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".filterAll()\n\t toggl_dim_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".filter(function(d){return d == val;})\n\t dc.redrawAll();\n     }\n\n     var toggle_group_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = toggl_dim_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".group();\n     var toggle_keys_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = toggle_group_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".all().map(function(x) {return x.key;})\n     var switch_elem_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " = document.getElementById(\"dc_switch_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "\")\n     for (var i = 0; i < toggle_keys_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".length; i++){\n\t var selected_str = \"btn-default\"\n\t if (i==0){\n\t     selected_str = \"btn-info\"\n\t     handle_dc_switch_toggle_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "({\"value\":toggle_keys_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "[i]})\n\t }\n\t switch_elem_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += ".innerHTML += \"<input type='button' class='dc_switch_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += " btn \"+selected_str+\"' onclick='handle_dc_switch_toggle_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "(this);' name='optradio' value='\"+toggle_keys_IV_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "[i]+\"'>\"\n     }\n     ";
;
}
output += "\n\n     // remove filters and redraw bar charts so they don't start out with a reset button \n     // (due to what I assume is a dc.js bug)\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar1_variable")) {
output += "bar1_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll()";
;
}
output += "\n     ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"bar2_variable")) {
output += "bar2_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart.filterAll()";
;
}
output += "\n\n     iv_data_loaded_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "_chart = true;\n     resize_IV_charts_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "();\n     dc.redrawAll()\n});\n\n\n// the portal interface for a page to refresh item widgets in the case of hiding / showing, etc.\nvar portal_item_refresh_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += " = function(){\nresize_IV_charts_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"project_id"), env.opts.autoescape);
output += "();\n}\n\n</script>\n\n\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
b_display_image: b_display_image,
b_custom_item_content: b_custom_item_content,
root: root
};

})();
})();

(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["single_quiz/feed_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
env.getTemplate("core/feed_item.html", true, "single_quiz/feed_item.html", false, function(t_2,_parentTemplate) {
if(t_2) { cb(t_2); return; }
parentTemplate = _parentTemplate
for(var t_1 in parentTemplate.blocks) {
context.addBlock(t_1, parentTemplate.blocks[t_1]);
}
output += "\n";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("custom_item_content"))(env, context, frame, runtime, function(t_4,t_3) {
if(t_4) { cb(t_4); return; }
output += t_3;
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
})});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_custom_item_content(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += "\n        \n<div id=\"single_quiz_result_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\">\n  <div class=\"single_quiz_ajax_form\">\n    <div>";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"name"), env.opts.autoescape);
output += "</div>\n    <select id=\"single_quiz_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\">\n      ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option1")) {
output += "  <option value=\"1\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option1"), env.opts.autoescape);
output += "</option>";
;
}
output += "\n      ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option2")) {
output += "  <option value=\"2\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option2"), env.opts.autoescape);
output += "</option>";
;
}
output += "\n      ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option3")) {
output += "  <option value=\"3\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option3"), env.opts.autoescape);
output += "</option>";
;
}
output += "\n      ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option4")) {
output += "  <option value=\"4\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option4"), env.opts.autoescape);
output += "</option>";
;
}
output += "\n      ";
if(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option5")) {
output += "  <option value=\"5\">";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"option5"), env.opts.autoescape);
output += "</option>";
;
}
output += "\n    </select>\n    <div>\n      <input type=\"submit\" class=\"portal_ajax_submit\" id=\"single_quiz_submit_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\" data-target-element=\"single_quiz_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\" data-result-element=\"single_quiz_result_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\" data-target-url=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"link"), env.opts.autoescape);
output += "\" value=\"Submit\" />\n    </div>\n  </div>\n  <span class=\"correct\" style=\"display: none;\">\n    <h1 style=\"display: inline;\"><span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\" style=\"color:green\"></span> </h1>\n  </span>\n  <span class=\"incorrect\" style=\"display: none;\">\n    <h1 style=\"display: inline;\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\" style=\"color:red\"></span> </h1>\n  </span>\n  <span>\n    <h4 class=\"response\" style=\"display: none;\" data-display-style=\"inline\"></h4>\n  </span>\n  <p>\n    <div class=\"explanation\"></div>\n  </p>\n  <p class=\"sources\" style=\"display: none;\">\n    Follow our sources <a href=\"";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"citation_url"), env.opts.autoescape);
output += "\">here</a>!\n  </p>\n</div>\n\n<script>\n  register_event_trigger(document.getElementById(\"single_quiz_submit_";
output += runtime.suppressValue(runtime.memberLookup((runtime.contextOrFrameLookup(context, frame, "item")),"id"), env.opts.autoescape);
output += "\"));\n</script>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
b_custom_item_content: b_custom_item_content,
root: root
};

})();
})();

(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["manual_news_article_curation/feed_item.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
env.getTemplate("core/feed_item.html", true, "manual_news_article_curation/feed_item.html", false, function(t_2,_parentTemplate) {
if(t_2) { cb(t_2); return; }
parentTemplate = _parentTemplate
for(var t_1 in parentTemplate.blocks) {
context.addBlock(t_1, parentTemplate.blocks[t_1]);
}
output += "\n";
(parentTemplate ? function(e, c, f, r, cb) { cb(""); } : context.getBlock("custom_link_content"))(env, context, frame, runtime, function(t_4,t_3) {
if(t_4) { cb(t_4); return; }
output += t_3;
output += "\n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
})});
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
function b_custom_link_content(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var frame = frame.push(true);
output += " target=\"_blank\" ";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
b_custom_link_content: b_custom_link_content,
root: root
};

})();
})();

(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["core/portal_ux/tag_remove.html"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<span class=\"label label-default\">";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "tag_name"), env.opts.autoescape);
output += " <span style=\"cursor:pointer;\" class=\"glyphicon glyphicon-remove\" onclick=\"remove_filter(";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "tag_id"), env.opts.autoescape);
output += ")\"></span></span> \n";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();

