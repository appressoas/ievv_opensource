import CleanHtml from "../CleanHtml";

describe('CleanHtml', () => {
    it('sanity', () => {
        const htmlCleaner = new CleanHtml();
        expect(htmlCleaner.clean('<p class="test">Test</p>')).toEqual(
            '<p>Test</p>');
    });

    it('allows a href', () => {
        const htmlCleaner = new CleanHtml();
        expect(htmlCleaner.clean('<a href="http://example.com">Test</a>')).toEqual(
            '<a href="http://example.com">Test</a>');
    });

    it('transform tag', () => {
        const htmlCleaner = new CleanHtml();
        htmlCleaner.setTransformTags({
            'div': 'p'
        });
        expect(htmlCleaner.clean('<div>Test</div>')).toEqual(
            '<p>Test</p>');
    });

    it('setAllowedAttributes', () => {
        const htmlCleaner = new CleanHtml();
        htmlCleaner.setAllowedAttributes({
            'a': ['target']
        });
        expect(htmlCleaner.clean('<a href="#" target="_blank">Test</a>')).toEqual(
            '<a target="_blank">Test</a>');
    });

});
