import htmlparser from "htmlparser2";
import {makeHtmlStartTag, makeHtmlEndTag} from "./utils";
import {isInlineTag} from "./utils";
import CleanHtml from "./CleanHtml";


export class PostCleanContentEditableHtml {
    constructor(html, wrapperTagName='p', wrapperTagAttributes={}) {
        this._wrapperTagName = wrapperTagName;
        this._wrapperTagAttributes = wrapperTagAttributes;
        this._currentBlockElementLevel = 0;
        this._currentInlineElementLevel = 0;
        this._resultHtml = '';
        this._isWrapping = false;
        this._parse(html);
        if(this._isWrapping) {
            this.endWrapping();
        }
    }

    _parse(html) {
        const parser = new htmlparser.Parser({
            onopentag: (...args) => {
                this._onOpenTag(...args);
            },
            ontext: (...args) => {
                this._onText(...args);
            },
            onclosetag: (...args) => {
                this._onCloseTag(...args);
            }
        }, {decodeEntities: true});
        parser.write(html);
        parser.end();
    }

    startWrapping() {
        this._resultHtml += makeHtmlStartTag(this._wrapperTagName, this._wrapperTagAttributes);
        this._isWrapping = true;
    }

    endWrapping() {
        this._resultHtml += makeHtmlEndTag(this._wrapperTagName);
        this._isWrapping = false;
    }

    _shouldWrap() {
        return this._currentBlockElementLevel == 0 && !this._isWrapping;
    }

    _onOpenInlineTag(tagName, attributes) {
        if(this._shouldWrap()) {
            this.startWrapping();
        }
        this._currentInlineElementLevel ++;
        this._resultHtml += makeHtmlStartTag(tagName, attributes);
    }

    _onOpenBlockTag(tagName, attributes) {
        if(this._currentInlineElementLevel == 0) {
            if(this._currentBlockElementLevel == 0 && this._isWrapping) {
                this.endWrapping();
            }
            this._currentBlockElementLevel++;
            this._resultHtml += makeHtmlStartTag(tagName, attributes);
        }
    }

    _onOpenTag(tagName, attributes) {
        if(isInlineTag(tagName)) {
            this._onOpenInlineTag(tagName, attributes);
        } else {
            this._onOpenBlockTag(tagName, attributes);
        }
    }

    _onText(text) {
        if(this._shouldWrap()) {
            this.startWrapping();
        }
        this._resultHtml += text;
    }

    _onCloseInlineTag(tagName) {
        this._currentInlineElementLevel --;
        this._resultHtml += makeHtmlEndTag(tagName);
    }

    _onCloseBlockTag(tagName) {
        if(this._currentInlineElementLevel == 0) {
            this._currentBlockElementLevel --;
            this._resultHtml += makeHtmlEndTag(tagName);
        }
    }

    _onCloseTag(tagName) {
        if(isInlineTag(tagName)) {
            this._onCloseInlineTag(tagName);
        } else {
            this._onCloseBlockTag(tagName);
        }
    }

    toString() {
        return this._resultHtml;
    }
}


/**
 * HTML cleaner with extra post cleaning that makes it
 * suitable for cleaning input typed and pasted into
 * contenteditable editors.
 */
export default class CleanContentEditableHtml extends CleanHtml {
    setInlineWithoutParentWrapperTag(tagName, tagAttributes={}) {
        this._inlineWithoutParentWrapperTagName = tagName;
        this._inlineWithoutParentWrapperTagAttributes = tagAttributes;
    }

    postClean(html) {
        return new PostCleanContentEditableHtml(
            html,
            this._inlineWithoutParentWrapperTagName,
            this._inlineWithoutParentWrapperTagAttributes).toString();
    }
}
