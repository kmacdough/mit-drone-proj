function DataService() {
  this.apiUrl = "";
};

function mockPromise(data) {
  return new Promise(function(resolve){
    resolve(data);
  });
}

function xhrGetPromise(url) {
  return new Promise(function(resolve, reject){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.onload = function() {
      resolve(xhr.response.data);
    }
    xhr.onerror = function() {
      reject({status: xhr.status, statusText: xhr.statusText});
    }
  });
}

DataService.prototype.getAllDrones = function() {
  return xhrGetPromise(this.apiUrl + "/drones");
};

MockDataService.prototype.getAllDrones = function() {
  for(var i = 0; i < this.data.drones.length; i++) {
    this.data.drones[i].geolocation.longitude += 0.001;
  }
  return mockPromise(this.data.drones);
}

DataService.prototype.getAllParcels = function() {
  return xhrGetPromise(this.apiUrl + "/parcels");
};

MockDataService.prototype.getAllParcels = function() {
  return mockPromise(this.data.parcels);
};

function MockDataService() {
  this.data = {};
  this.data.drones = [
    {
      battery: 1,
      geolocation: {
        latitude: 42.3583387,
        longitude: -71.0766567
      },
      id: "4124123-12323-12323-12312332312",
      parcel: {
        
      }
    }, {
      battery: 1,
      geolocation: {
        latitude: 42.3083387,
        longitude: -71.0566567
      },
      id: "4124123-12323-12323-12312332311",
      parcel: {
        id: "23475-8923-49525-3453455545"
      }
    }
  ];
  
  this.data.parcels = [
    {
      id: "12312-123123-12323-23123123123",
      geolocation : {
        latitude: 42.310,
        longitude: -71.046
      }
    },
    {
      id: "12312-123123-12323-2312312223",
      geolocation : {
        latitude: 42.316,
        longitude: -71.066
      }
    }
  ];
}