class HelloMessage extends React.Component {
    render() {
      return React.createElement(
        "div",
        null,
        'Helloooo ',
        this.props.name
      );
    }
  }
  
ReactDOM.render(React.createElement(HelloMessage, { name: "Taylorrrr" }), document.getElementById('hello-example'));