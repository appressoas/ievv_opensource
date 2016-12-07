import React from "react";
import IevvSearch from "./IevvSearch";
import IevvModal from "./IevvModal";


export default class IevvSelectModal extends IevvModal {
  renderModalContent() {
    const searchSignalName = `${this.props.signalNamePrefix}.search`;
    new window.ievv_jsbase_core.SignalHandlerSingleton().addReceiver(
      searchSignalName,
      this.props.signalNamePrefix,
      (receivedSignalInfo) => {
        console.log(receivedSignalInfo.toString());
      }
    );
    return <IevvSearch changeSignalName={searchSignalName} />;
  }
}
