function show_point_map(div_id, coord_tag_id, coordinate, zoom) {
    var llng = new google.maps.LatLng(coordinate[0], coordinate[1]);
    var map_options = {
        center: llng,
        mapTypeId: 'terrain',
	zoom: zoom
    };
    var map = new google.maps.Map(document.getElementById(div_id), map_options); 
}
