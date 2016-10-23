import DOMReplaceFromUrl from "./DOMReplaceFromUrl";
import parseHtml from "./parseHtml";


/**
 * Extends {@link DOMReplaceFromUrl} to replace the element
 * with the same element from the server response.
 *
 * This is ment to be used if you request a full page from the
 * server to replace a single element in your document.
 */
export default class DOMReplaceWithSameElementFromUrl extends DOMReplaceFromUrl {
    extractHtmlStringFromResponse(response) {
        let serverDocument = parseHtml(response.body);
        let serverElement = serverDocument.querySelector(`#${this.elementId}`);
        return serverElement.innerHTML.trim();
    }
}
