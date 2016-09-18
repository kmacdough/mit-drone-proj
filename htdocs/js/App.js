var App = function() {
  // do app initialization here;
  this.dataService = new ApiProvider();
  this.loggedIn = document.cookie !== "";
  this.userId = document.cookie.split('=')[1];
}

/*
 * View showing methods - these will replace whatever's currently showing
 * with the requested view.
 */

App.prototype.showListTestPage = function() {
  var data = [{
      key: "Hey",
      action: function(el){},
      text: "Test text 1"
  }, {
      key: "whoa",
      action: function(el){},
      text: "Test text 2"
  }];
  var name = "My active deliveries";
  ReactDOM.render(<ListBox name={name} data={data} />, this.root);
}

App.prototype.submitLogInForm = function() {
  var self = this;
  this.dataService.logIn("test", "test")
          .then(function(){
            self.loggedIn = true;
            self.showMainPage();
          },function(e){
            self.loggedIn = false;
            self.showErrorPage(e.statusText)
          });
}

App.prototype.submitRegisterForm = function() {
  var self = this;
  this.dataService.register("test", "test")
          .then(function(){
            self.showLogInView();
          },function(e){
            self.loggedIn = false;
            self.showErrorPage(e.statusText)
          });
}

App.prototype.showRegisterView = function() {
  ReactDOM.render(
          <section>
          <div className="section-header">Register</div>
          <input type="text" id="emailEntry" placeholder="e-mail"/><br/>
          <input type="password" id="passwordEntry" placeholder="password"/><br/>
          <button onClick={this.submitRegisterForm.bind(this)}>Register</button>
          </section>, this.root);
}

App.prototype.showLogInView = function() {
  ReactDOM.render(
          <section>
          <div className="section-header">Login</div>
          <input type="text" id="emailEntry" placeholder="e-mail"/><br/>
          <input type="password" id="passwordEntry" placeholder="password"/><br/>
          <button onClick={this.submitLogInForm.bind(this)}>Login</button><br/>
          <button onClick={this.showRegisterView.bind(this)}>Register</button>
          </section>, this.root);
}

App.prototype.showMainPage = function() {
  ReactDOM.render(
          <section>
          <div className="section-header">Main Page</div>
          </section>, this.root);
}

App.prototype.showNewDeliveryPage = function() {
  ReactDOM.render(<section>
  <div className="section-header">New Delivery</div>
  </section>,this.root);
}

App.prototype.showNewPlacePage = function() {
  ReactDOM.render(<section>
  <div className="section-header">Add Place</div>
  </section>,this.root);
}

App.prototype.showErrorPage = function(text) {
  ReactDOM.render(<section><h1>Error</h1>{text}</section>, this.root);
}

/**
 * Kickstart the application.
 * @returns {undefined}
 */
App.prototype.start = function() {
  var self = this;
  console.log("Starting app");
  this.root = document.getElementById("main");
  this.showLogInView();
  
}
window.app = new App();
app.start();