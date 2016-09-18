var App = function() {
  // do app initialization here;
  this.dataService = new ApiProvider();
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

var ListItem = React.createClass({
  render: function() {
    return (
      <a className="list-item" href="javascript:" onClick={this.props.action}>
       {this.props.text}
      </a>
    );
  }
});
console.log("Widgets are actually being loaded");
var ListBox = React.createClass({
  render: function() {
    var listNodes = this.props.data.map(function(item) {
      return (
        <ListItem key={item.key} action={item.action} text={item.text} />
      );
    });
    return (
      <div className="list">
        <div className="list-header">
          {this.props.name}
        </div>
        {listNodes}
      </div>
    );
  }
});

new App().start();