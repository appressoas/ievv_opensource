import React from "react";


export default class IevvSearch extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = {value: ''};
    console.log(this.props);
  }

  static get defaultProps() {
    return {
      'changeDelay': 200,
      'placeholder': 'Search ...',
      'className': 'input input--outlined'
    }
  }

  handleChange(event) {
    this._cancelInputTimeout();
    this.setState({value: event.target.value});
    this._timeoutId = window.setTimeout(
      () => {this._onChangeDelayed()},
      this.props.changeDelay);
  }

  _cancelInputTimeout() {
    if(this._timeoutId != undefined) {
      window.clearTimeout(this._timeoutId);
    }
  }

  _onChangeDelayed() {
    new window.ievv_jsbase_core.SignalHandlerSingleton().send(
      this.props.changeSignalName,
      this.state.value
    );
  }

  render() {
    return <input type="search" placeholder={this.props.placeholder} className={this.props.className}
                  value={this.state.value}
                  onChange={this.handleChange} />;
  }
}
