export class SelectionPoint {
    constructor(selectionRange, node, offset) {
        this.selectionRange = selectionRange;
        if(node.nodeType == Node.TEXT_NODE) {
            this.node = node;
            this.offset = offset;
        } else {
            this.node = node.parentNode.childList[this.offset];
            this.offset = 0;
        }
    }

    getPathRelativeTo(relativeToElement) {
        let currentNode = this.node;
        let path = [];
        while (true) {
            if(currentNode == null || currentNode == relativeToElement) {
                break;
            }
            let nodeName = currentNode.nodeName.toLowerCase();
            path.unshift(nodeName);
            currentNode = currentNode.parentElement;
        }
        return path;
    }

    toString() {
        return `${this.node.nodeName}[${this.offset}]`;
    }
}

export default class SelectionRange {
    static makeFromCurrentSelection(rootElement) {
        return new SelectionRange(window.getSelection().getRangeAt(0), rootElement);
    }

    constructor(range, rootElement) {
        this.range = range;
        this.rootElement = rootElement || window.document.body;
        this.start = new SelectionPoint(this, this.range.startContainer, this.range.startOffset);
        this.end = new SelectionPoint(this, this.range.endContainer, this.range.endOffset);
    }

    startIsSameAsEnd() {
        return this.start.node == this.end.node && this.start.offset == this.end.offset;
    }

    toString() {
        return `${this.start.toString()} --> ${this.end.toString()}`;
    }
}
