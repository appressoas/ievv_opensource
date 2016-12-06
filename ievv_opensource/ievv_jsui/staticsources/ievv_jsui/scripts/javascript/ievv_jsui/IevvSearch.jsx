import React from "react";


export default class IevvSearch extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = {value: ''};
  }

  handleChange(event) {
    this._cancelInputTimeout();
    this.setState({value: event.target.value});
    this._timeoutId = setTimeout(
      () => {this._onChangeDelayed()},
      200);
  }

  _cancelInputTimeout() {
    if(this._timeoutId != undefined) {
      clearTimeout(this._timeoutId);
    }
  }

  _onChangeDelayed(value) {
    console.log('INPUT:', this.state.value);
  }

  render() {
    return <input type="search" placeholder="Search ..." className="input input--outlined"
                  value={this.state.value}
                  onChange={this.handleChange} />;
  }
}
