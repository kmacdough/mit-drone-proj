window.ListItem = React.createClass({
  render: function() {
    return (
      <a className="list-item" href="javascript:" onClick={this.props.action}>
       {this.props.text}
      </a>
    );
  }
});

window.ListBox = React.createClass({
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

