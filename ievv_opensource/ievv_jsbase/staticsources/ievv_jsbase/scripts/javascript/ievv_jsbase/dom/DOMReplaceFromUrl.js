import DOMReplace from "./DOMReplace";
import HttpRequest from "../http/HttpRequest";


/**
 * Extends {@link DOMReplace} adn change the methods to
 * replace by making a request to the server.
 */
export default class DOMReplaceFromUrl extends DOMReplace {
    _makeRequest(url) {
        return new HttpRequest(url);
    }

    extractHtmlStringFromResponse(response) {
        return response.body;
    }

    _replaceFromUrl(url, callback) {
        return new Promise((resolve, reject) => {
            let request = this._makeRequest(url);
            request.get().then((response) => {
                let htmlString = this.extractHtmlStringFromResponse(response);
                callback(htmlString);
                resolve(htmlString, response);
            }, (response) => {
                reject(response);
            });
        });
    }

    replaceInnerHtml(url) {
        return this._replaceFromUrl(url, (htmlString) => {
            super.replaceInnerHtml(htmlString);
        });
    }


    appendInnerHtml(url) {
        return this._replaceFromUrl(url, (htmlString) => {
            super.appendInnerHtml(htmlString);
        });
    }

    prependInnerHtml(url) {
        return this._replaceFromUrl(url, (htmlString) => {
            super.prependInnerHtml(htmlString);
        });
    }
}
