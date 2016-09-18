function ApiProvider() {
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
    xhr.open('GET', url, true);
    xhr.onload = function() {
      var responseJson = JSON.parse(xhr.responseText);
      if(responseJson.status === "success")
        resolve(responseJson.data);
      else
        reject({status: xhr.status, statusText: responseJson.message});
    }
    xhr.onerror = function() {
      reject({status: xhr.status, statusText: xhr.statusText});
    }
  });
}

function xhrPostPromise(url, postFields) {
  return new Promise(function(resolve, reject){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      var responseJson = JSON.parse(xhr.responseText);
      if(responseJson.status === "success")
        resolve(responseJson.data);
      else
        reject({status: xhr.status, statusText: responseJson.message});
    }
    xhr.onerror = function() {
      reject({status: xhr.status, statusText: xhr.statusText});
    }
    xhr.send(JSON.stringify(postFields));
  });
}

ApiProvider.prototype.getAllDrones = function() {
  return xhrGetPromise(this.apiUrl + "/drones");
};

MockApiProvider.prototype.getAllDrones = function() {
  for(var i = 0; i < this.data.drones.length; i++) {
    this.data.drones[i].geolocation.longitude += 0.001;
  }
  return mockPromise(this.data.drones);
}

ApiProvider.prototype.getAllParcels = function() {
  return xhrGetPromise(this.apiUrl + "/parcels");
};

MockApiProvider.prototype.getAllParcels = function() {
  return mockPromise(this.data.parcels);
};

ApiProvider.prototype.logIn = function(email, password) {
  return xhrPostPromise(this.apiUrl + "/login", {email: email, password: password});
}

ApiProvider.prototype.logOut = function() {
  document.cookie = "user_id=; max-age=0;";
}

ApiProvider.prototype.register = function(email, password) {
  return xhrPostPromise(this.apiUrl + "/user", {email: email, password: password});
}


function MockApiProvider() {
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

/**

UUID: string <123e4567-e89b-12d3-a456-426655440000>

Geolocation:
{
  latitude: Number
  longitude: Number
}

drone:
{
  id: UUID,
  geolocation: Geolocation,
  battery: Number,
  parcel_id: UUID
  OPTIONAL: parcel: parcel
}

ParcelStatus: string oneof
  unassigned
  pending_pickup
  in_delivery
  delivered

parcel:
{
  id: UUID,
  sender_id: UUID,
  recipient_id: UUID,
  origin_id: UUID,
  destination_id: UUID,
  dimensions: {
      width: Number,
      height: Number,
      length: Number,
      weight: Number
  },
  status: ParcelStatus,
  created_time: DateTime,
  pickup_time: DateTime,
  dropoff_time: DateTime
}

place:
{
  id: UUID,
  geolocation: Geolocation,
  name: string
}

user:
{
  id: UUID,
  email: string,
  salted_password: string
}

 */