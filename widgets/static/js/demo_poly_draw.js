// (code inspired by the following, license copied below): http://codepen.io/jhawes/post/creating-a-real-estate-polygon-tool
// Copyright (c) 2015 by Jeremy Hawes (http://codepen.io/jhawes/pen/ujdgK)
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

function polygonCoordWriter(polygon, coord_tag_id) {
    return function() {
        var len = polygon.getPath().getLength();
        var jsonArray = [];
        for (var i = 0; i < len; i++) {
            jsonArray.push("[" + 
                polygon.getPath().getAt(i).toUrlValue(5) + 
                "]");
        }
        $('input[id='+coord_tag_id+']').val('['+jsonArray+']');
        // document.getElementByName(coord_tag_id).value = jsonArray;
    }
}

function getPolygonBoundsZoomLevel(polygonBounds) {
    var GLOBE_WIDTH = 256; // a constant in Google's map projection
    var west = polygonBounds.getNorthEast().lng();
    var east = polygonBounds.getSouthWest().lng();
    var angle = east - west;
    if (angle < 0) {
          angle += 360;
    }
    var zoom = Math.round(Math.log(pixelWidth * 360 / angle / GLOBE_WIDTH) / Math.LN2);
    return zoom;
}

function show_editable_map(div_id, coord_tag_id, coordinates) {
    // Initialize map to certain coordinates
    if (coordinates == null) {
        coordinates = [[37.41626,-122.03691],
            [37.37835,-122.0527], 
            [37.39867,-121.97889]]
    }

    var coords = get_google_maps_latlngs(coordinates);
    // Styling and controls
    var polygon = new google.maps.Polygon({
        paths : coords,
        draggable : true,
        editable : true,
        strokeColor : '#FF0000',
        strokeOpacity : 0.8,
        strokeWeight : 2,
        fillColor : '#FF0000',
        fillOpacity : 0.25
    });
    var center = getPolygonBounds(polygon).getCenter();
    var bounds = getPolygonBounds(polygon);
    var map_options = {
        center: center,
        mapTypeId: 'terrain'
    };
    var map = new google.maps.Map(document.getElementById(div_id), map_options); 
    map.fitBounds(bounds);
    // Initilalize polygon drawing

    polygon.setMap(map);
    var coord_update_function = polygonCoordWriter(polygon, coord_tag_id);
    coord_update_function(polygon);
    google.maps.event.addListener(polygon.getPath(), "insert_at", coord_update_function);
    google.maps.event.addListener(polygon.getPath(), "set_at", coord_update_function);
    google.maps.event.addListener(polygon.getPath(), "remove_at", coord_update_function);
}
