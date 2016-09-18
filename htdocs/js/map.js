var apiProvider = new MockApiProvider();
var mapDroneMarkers = {};
var mapParcelMarkers = {};

function updateMarkers(map, markersObject, imageName, data, zIndex) {
  //console.log(drones);
  var thingsById = {};
  for(var i = 0; i < data.length; i++) {
    thingsById[data[i].id] = data[i];
  }

  for(var i in thingsById) {
    var thing = thingsById[i];
    var image = imageName;
    if(markersObject[i]) {
      markersObject[i].setPosition({
        lat: thing.geolocation.latitude,
        lng: thing.geolocation.longitude
      });
      continue;
    }
    markersObject[thing.id] = new google.maps.Marker({
      position: {
        lat: thing.geolocation.latitude,
        lng: thing.geolocation.longitude
      },
      map: map,
      icon: image,
      zIndex: zIndex
    });
  }

  for(var x in markersObject) {
    if(!thingsById[x]) {
      markersObject[x].setMap(null);
    }
  }
}

function reloadMapData(map) {
  console.log("ReloadMapData called");
  apiProvider.getAllDrones().then(function(drones){
    updateMarkers(map, mapDroneMarkers, '/img/drone.png', drones, 10);
  });
  
  apiProvider.getAllParcels().then(function(parcels){
    //console.log(parcels);
    updateMarkers(map, mapParcelMarkers, '/img/parcel.png', parcels, 9);
  });
}


function initMap() {
  var myLatlng = new google.maps.LatLng(42.3583387, -71.0766567);
  var mapOptions = {
    zoom: 14,
    center: myLatlng,
    mapTypeId: 'roadmap'
  };
  var map = new google.maps.Map(document.getElementById('map'),
      mapOptions);
  reloadMapData(map);
  window.setInterval(reloadMapData, 500, map);
}


    