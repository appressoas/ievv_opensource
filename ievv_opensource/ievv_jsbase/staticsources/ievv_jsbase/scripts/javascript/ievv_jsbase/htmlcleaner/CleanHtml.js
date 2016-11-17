import sanitizeHtml from "sanitize-html";


/**
 * HTML cleaner.
 *
 * @example <caption>Simple</caption>
 * new CleanHtml().clean('<a href="#" target="_blank">Test</a>') == '<a href="#">Test</a>';
 *
 * @example <caption>Override allowed tags</caption>
 * const htmlCleaner = new CleanHtml();
 * htmlCleaner.setAllowedTags(['h2', 'strong']);
 * htmlCleaner.clean('<h3>Test</h3>') == 'Test';
 * htmlCleaner.clean('<h2>Test</h2>') == '<h2>Test</h2>';
 * htmlCleaner.clean('<strong>Test</strong>') == '<strong>Test</strong>';
 *
 * @example <caption>Override allowed attributes</caption>
 * const htmlCleaner = new CleanHtml();
 * htmlCleaner.setAllowedAttributes({
 *   'a': ['href', 'target']
 * });
 *
 * @example <caption>Transform tags</caption>
 * const htmlCleaner = new CleanHtml();
 * htmlCleaner.setTransformTags({
 *   'ol': 'ul'
 * });
 * htmlCleaner.clean('<ol></ol>') == '<ul></ul>';
 */
export default class CleanHtml {
    constructor() {
        this._allowedTags = ['h2', 'h3', 'p', 'strong', 'em', 'a'];
        this._allowedAttributes = {
            a: ['href']
        };
        this._transformTags = {};
    }

    /**
     * Set allowed tags
     * @param {[]} allowedTagsArray Array of tag names. All tag
     *    names must be lowercase.
     */
    setAllowedTags(allowedTagsArray) {
        this._allowedTags = allowedTagsArray;
    }

    /**
     * Set allowed attributes.
     *
     * @param {{}} allowedAttributes Object that maps tag name
     *    name to an array of allowed attribute names.
     */
    setAllowedAttributes(allowedAttributes) {
        this._allowedAttributes = allowedAttributes;
    }

    /**
     * Set transform tag mapping.
     *
     * @param {{}} transformTags Object that maps tag name
     *    to another tagname. The key is transformed
     *    into the value.
     */
    setTransformTags(transformTags) {
        this._transformTags = transformTags;
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

    /**
     * Clean the provided html.
     *
     * @param {string} html The HTML to clean.
     * @returns {string} The cleaned HTML.
     */
    clean(html) {
        let cleanedHtml = this.preClean(html);
        cleanedHtml = sanitizeHtml(cleanedHtml, {
            allowedTags: this._allowedTags,
            allowedAttributes: this._allowedAttributes,
            transformTags: this._transformTags
        });
        cleanedHtml = this.postClean(cleanedHtml);
        return cleanedHtml;
    }
}
