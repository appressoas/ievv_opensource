import SignalHandlerSingleton from "../SignalHandlerSingleton";

export default class DOMReplace {
    constructor(elementId) {
        this.element = document.getElementById(elementId);
    }

    replaceInnerHtml(htmlString) {
        this.element.innerHTML = htmlString;
        let signalHandler = new SignalHandlerSingleton();
        signalHandler.send('ievv_jsbase.DOMReplace.replaceInnerHtml', this);
    }

    appendInnerHtml(htmlString) {
        this.element.innerHTML = this.element.innerHTML + htmlString;
        let signalHandler = new SignalHandlerSingleton();
        signalHandler.send('ievv_jsbase.DOMReplace.appendInnerHtml', this);
    }

    prependInnerHtml(htmlString) {
        this.element.innerHTML = htmlString + this.element.innerHTML;
        let signalHandler = new SignalHandlerSingleton();
        signalHandler.send('ievv_jsbase.DOMReplace.prependInnerHtml', this);
    }
}
