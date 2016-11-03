function show_polygon_map(div_id, coord_tag_id, coordinates) {
    var coords = get_google_maps_latlngs(coordinates);
    // Styling and controls
    var polygon = new google.maps.Polygon({
        paths : coords,
        draggable : false,
        editable : false,
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
    
    polygon.setMap(map);
}
