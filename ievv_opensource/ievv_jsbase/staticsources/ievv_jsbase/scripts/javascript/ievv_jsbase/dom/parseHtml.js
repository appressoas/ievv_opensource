export default function parseHtml(htmlString) {
    var tempDocument = document.implementation.createHTMLDocument();
    tempDocument.body.innerHTML = htmlString;
    return tempDocument.body;
}
