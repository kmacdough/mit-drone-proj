var App = function() {
  // do app initialization here;
  this.dataService = new ApiProvider();
  this.loggedIn = document.cookie !== "";
  this.userId = document.cookie.split('=')[1];
  
}

App.prototype.start = function() {
  var data = [{
      key: "Hey",
      action: function(el){},
      text: "Test text 1"
  }, {
      key: "Hey",
      action: function(el){},
      text: "Test text 2"
  }];
  var name = "My active deliveries";
  console.log("Starting app");
  
  this.dataService.logIn("test", "test");
  ReactDOM.render(<ListBox name={name} data={data} />, document.getElementById("main"));
}

new App().start();