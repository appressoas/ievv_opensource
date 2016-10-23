import DOMReplace from "./DOMReplace";
import HttpRequest from "../http/HttpRequest";


export default class DOMReplaceFromUrl extends DOMReplace {
    constructor(elementId, url) {
        super(elementId);
        this.url = url;
    }

    _makeRequest() {
        return new HttpRequest(this.url);
    }

    _replaceFromUrl(callback) {
        return new Promise((resolve, reject) => {
            let request = this._makeRequest();
            request.get().then((response) => {
                let htmlString = response.body;
                callback(htmlString);
                resolve(htmlString, response);
            }, (response) => {
                reject(response);
            });
        });
    }

    replaceInnerHtml() {
        return this._replaceFromUrl((htmlString) => {
            super.replaceInnerHtml(htmlString);
        });
    }


    appendInnerHtml() {
        return this._replaceFromUrl((htmlString) => {
            super.appendInnerHtml(htmlString);
        });
    }

    prependInnerHtml() {
        return this._replaceFromUrl((htmlString) => {
            super.prependInnerHtml(htmlString);
        });
    }
}
