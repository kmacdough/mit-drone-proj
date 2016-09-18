var ListItem = React.createClass({
  render: function() {
    return (
      <a class="list-item" href="javascript:" onClick={this.props.action}>
       {this.props.text}
      </a>
    );
  }
});

var ListBox = React.createClass({
  render: function() {
    var listNodes = this.props.data.map(function(item) {
      return (
        <ListItem key={item.key} action={item.action} text={item.text} />
      );
    });
    return (
      <div class="list">
        <div class="list-header">
          {this.props.name}
        </div>
        {listNodes}
      </div>
    );
  }
});