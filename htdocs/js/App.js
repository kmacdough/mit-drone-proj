var data = [{
    key: "Hey",
    action: function(el){},
    text: "Test text 1"
}, {
    key: "Hey",
    action: function(el){},
    text: "Test text 2"
}];
var name = "Cool List Box";
ReactDOM.render(<ListBox name={name} data={data} />, document.getElementById("main"));