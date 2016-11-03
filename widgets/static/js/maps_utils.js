function getPolygonBounds(polygon) {
    var bounds = new google.maps.LatLngBounds();
    var paths = polygon.getPaths();
    var path;
    for (var i = 0; i < paths.getLength(); i++) {
        path = paths.getAt(i);
        for (var ii = 0; ii < path.getLength(); ii++) {
            bounds.extend(path.getAt(ii));
        }
    }
    return bounds;
}

function get_google_maps_latlngs(coordinates) {
    var coords = [];
    for (var i = 0; i < coordinates.length; i++) {
        var coord = coordinates[i];
        var llng = new google.maps.LatLng(coord[0], coord[1]);
        coords.push(llng);
    }
    return coords;
}
