/**
 * Parse the provided HTML returning it as a DOM Element.
 *
 * @param htmlString The HTML string to parse.
 * @returns {Element}
 */
export default function parseHtml(htmlString) {
    var tempDocument = document.implementation.createHTMLDocument();
    tempDocument.body.innerHTML = htmlString;
    return tempDocument.body;
}
