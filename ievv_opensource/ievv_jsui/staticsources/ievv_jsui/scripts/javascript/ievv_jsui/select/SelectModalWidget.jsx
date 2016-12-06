import React from "react";
import ReactDOM from "react-dom";
import AbstractWidget from "ievv_jsbase/widget/AbstractWidget";
import SelectModal from "./SelectModal";


export default class SelectModalWidget extends AbstractWidget {
  constructor(element) {
    super(element);
    this._onClickBound = (...args) => {
      this._onClick(...args);
    };
    this.element.addEventListener('click', this._onClickBound);
  }

  getDefaultConfig() {
    return {
      modalCssClass: "modal",
      backdropCssClass: "modal__backdrop",
      contentCssClass: "modal__content",
      closeWrapperCssClass: "modal__close",
      closeIconCssClass: "icon-close",
      // titleWrapperCssClass: "modal__title",
      closeButtonAriaLabel: "Close"
    }
  }

  _onClick(e) {
    e.preventDefault();
    this.createModalElement();
  }

  destroy() {
    this.element.removeEventListener('click', this._onClickBound);
    if(this._modalElement) {
      ReactDOM.unmountComponentAtNode(this._modalElement);
      this._modalElement.remove();
    }
  }

  close() {
    ReactDOM.unmountComponentAtNode(this._modalElement);
  }

  createModalElement() {
    this._modalElement = document.createElement('div');
    document.body.appendChild(this._modalElement);
    const props = Object.assign({}, this.config);
    props.closeCallback = () => {this.close()};
    const reactElement = <SelectModal {...props} />;
    ReactDOM.render(
      reactElement,
      this._modalElement
    );
  }
}
