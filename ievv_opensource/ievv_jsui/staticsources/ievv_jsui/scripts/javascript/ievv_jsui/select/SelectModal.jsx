import React from "react";
import IevvSearch from "../IevvSearch";


export default class SelectModal extends React.Component {
  render() {
    return <div className={this.props.modalCssClass}>
      <div className={this.props.backdropCssClass}></div>

      <div className={this.props.contentCssClass}>
        <div className={this.props.closeWrapperCssClass}>
          <button type="button" aria-label={this.props.closeButtonAriaLabel}
                  onClick={() => this.close()}>
            <i className={this.props.closeIconCssClass}></i>
          </button>
        </div>

        <IevvSearch/>
      </div>
    </div>;
  }

  close() {
    this.props.closeCallback();
  }
}
