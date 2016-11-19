import htmlparser from "htmlparser2";
import {makeHtmlStartTag, makeHtmlEndTag} from "./utils";
import {isInlineTag} from "./utils";
import CleanHtml from "./CleanHtml";
import ObjectManager from "../utils/ObjectManager";


/*
Handle paste:

    <p>Hello PASTEHERE</p>
    <ul>
        <li>Item PASTEHERE</li>
    </ul>

Handle force single parent element (ul).
Handle &nbsp; (should be removed)

2 options:
- Clean everything after paste, and handle invalid nesting in the cleaner.
- Know where we are cleaning.

*/

export class CleanHtmlParser {
    constructor(html, options) {
        this.options = options;
        this._currentBlockElementLevel = 0;
        this._currentInlineElementLevel = 0;
        this._isWrappingStandaloneInline = false;
        this._resultHtml = '';
        this._path = [];
        this._parse(html);
        if(this._isWrappingStandaloneInline) {
            this.endWrappingStandaloneInline();
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

    isAllowedTag(tagName) {
        const isAllowedTagName = this.options.allowedTags.indexOf(tagName) != -1;
        if(!isAllowedTagName) {
            return false;
        }
        const tagWithSameNameIndex = this._path.indexOf(tagName);
        const hasParentWithSameTagName = tagWithSameNameIndex != -1
            && tagWithSameNameIndex != (this._path.length - 1);
        if(hasParentWithSameTagName) {
            return this.options.allowSelfNested.indexOf(tagName) != -1;
        }
        return true;
    }

    startWrappingStandaloneInline() {
        this._resultHtml += makeHtmlStartTag(
            this.options.wrapStandaloneInlineTags.tagName,
            this.options.wrapStandaloneInlineTags.tagAttributes);
        this._isWrappingStandaloneInline = true;
    }

    endWrappingStandaloneInline() {
        this._resultHtml += makeHtmlEndTag(this.options.wrapStandaloneInlineTags.tagName);
        this._isWrappingStandaloneInline = false;
    }

    _shouldWrap() {
        return this.options.wrapStandaloneInlineTags
            && this._currentBlockElementLevel == 0
            && !this._isWrappingStandaloneInline;
    }

    _onOpenInlineTag(tagName, attributes) {
        if(this._shouldWrap()) {
            this.startWrappingStandaloneInline();
        }
        this._currentInlineElementLevel ++;
        this._resultHtml += makeHtmlStartTag(tagName, attributes);
    }

    _isAllowedAttributeForTagName(tagName, attributeName) {
        const allowedAttributesForTagName = this.options.allowedAttributes[tagName];
        if(typeof allowedAttributesForTagName == 'undefined') {
            return false;
        }
        return allowedAttributesForTagName.indexOf(attributeName) != -1;
    }

    _cleanAttributes(tagName, attributes) {
        const cleanedAttributes = {};
        for(let attributeName of Object.keys(attributes)) {
            if(this._isAllowedAttributeForTagName(tagName, attributeName)) {
                cleanedAttributes[attributeName] = attributes[attributeName];
            }
        }
        return cleanedAttributes;
    }

    _onOpenBlockTag(tagName, attributes) {
        if(this._currentInlineElementLevel == 0) {
            if(this._currentBlockElementLevel == 0 && this._isWrappingStandaloneInline) {
                this.endWrappingStandaloneInline();
            }
            this._currentBlockElementLevel++;
            this._resultHtml += makeHtmlStartTag(tagName, attributes);
        }
    }

    _transformTagName(tagName) {
        const newTagName = this.options.transformTags[tagName];
        if(typeof newTagName == 'undefined') {
            return tagName;
        }
        return newTagName;
    }

    _onOpenTag(tagName, attributes) {
        tagName = this._transformTagName(tagName);
        this._path.push(tagName);
        if(this.isAllowedTag(tagName)) {
            let cleanedAttributes = this._cleanAttributes(tagName, attributes);
            if(isInlineTag(tagName)) {
                this._onOpenInlineTag(tagName, cleanedAttributes);
            } else {
                this._onOpenBlockTag(tagName, cleanedAttributes);
            }
        }
    }

    _onText(text) {
        if(this._shouldWrap()) {
            this.startWrappingStandaloneInline();
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
        tagName = this._transformTagName(tagName);
        if(this.isAllowedTag(tagName)) {
            if (isInlineTag(tagName)) {
                this._onCloseInlineTag(tagName);
            } else {
                this._onCloseBlockTag(tagName);
            }
        }
        this._path.pop();
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
export default class CleanHtml2 {
    constructor(options={}) {
        this.options = ObjectManager.mergeAndClone(this.getDefaultOptions(), options);
    }

    getDefaultOptions() {
        return {
            allowedTags: ['h2', 'h3', 'p', 'strong', 'em', 'a'],
            allowSelfNested: [],
            flattenNestedLists: false,
            wrapStandaloneInlineTags: {
                tagName: 'p'
            },
            allowedAttributes: {
                a: ['href']
            },
            transformTags: {}
        }
    }

        /**
     * Called at the beginning of {@link CleanHtml#clean}
     * before performing the default cleaning.
     *
     * Subclasses can override this to perform additional
     * cleaning pre-cleaning.
     *
     * @param {string} html The HTML to pre-clean.
     * @returns {string} The pre-cleaned HTML. Defaults to returning
     *    the provided ``html`` unchanged.
     */
    preClean(html) {
        return html;
    }


    /**
     * Called at the end of {@link CleanHtml#clean}
     * after performing the default cleaning.
     *
     * Subclasses can override this to perform additional
     * cleaning post-cleaning.
     *
     * @param {string} html The HTML to post-clean.
     * @returns {string} The cleaned HTML. Defaults to returning
     *    the provided ``html`` unchanged.
     */
    postClean(html) {
        return html;
    }

    _clean(html) {
        return new CleanHtmlParser(html, this.options).toString();
    }

    /**
     * Clean the provided html.
     *
     * @param {string} html The HTML to clean.
     * @returns {string} The cleaned HTML.
     */
    clean(html) {
        let cleanedHtml = this.preClean(html);
        cleanedHtml = this._clean(cleanedHtml);
        cleanedHtml = this.postClean(cleanedHtml);
        return cleanedHtml;
    }
}
