import CleanHtml2 from "../CleanHtml2";

describe('CleanHtml2', () => {
    it('sanity', () => {
        const htmlCleaner = new CleanHtml2();
        expect(htmlCleaner.clean('<p class="test">Test</p>')).toEqual(
            '<p>Test</p>');
    });

    it('only allowed tags sanity', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            allowedTags: []
        });
        expect(htmlCleaner.clean('<p class="test">Test</p>')).toEqual(
            'Test');
    });

    it('only allowed tags', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            allowedTags: ['em', 'strong']
        });
        expect(htmlCleaner.clean(
            '<p class="test"><em>Test1</em> Test 2 <i>Test 3</i> <strong>Test 4</strong></p>'))
            .toEqual('<em>Test1</em> Test 2 Test 3 <strong>Test 4</strong>');
    });

    it('only allowed attributes', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            allowedAttributes: {
                p: ['class']
            }
        });
        expect(htmlCleaner.clean('<p class="test"><em class="test">Test</em></p>')).toEqual(
            '<p class="test"><em>Test</em></p>');
    });

    it('allows a href by default', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false
        });
        expect(htmlCleaner.clean('<a href="http://example.com">Test</a>')).toEqual(
            '<a href="http://example.com">Test</a>');
    });

    it('wraps inline', () => {
        const htmlCleaner = new CleanHtml2();
        expect(htmlCleaner.clean('<em>Test</em>')).toEqual(
            '<p><em>Test</em></p>');
    });

    it('wraps inline custom tag', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: {
                tagName: 'li'
            },
        });
        expect(htmlCleaner.clean('<em>Test</em>')).toEqual(
            '<li><em>Test</em></li>');
    });

    it('wraps inline custom attributes', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: {
                tagName: 'li',
                tagAttributes: {
                    'class': 'testclass'
                }
            },
        });
        expect(htmlCleaner.clean('<em>Test</em>')).toEqual(
            '<li class="testclass"><em>Test</em></li>');
    });

    it('transforms tags simple', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            transformTags: {'div': 'p'}
        });
        expect(htmlCleaner.clean('<div>Test</div>')).toEqual(
            '<p>Test</p>');
    });

    it('transforms tags deep', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            transformTags: {
                'div': 'p',
                'i': 'em'
            }
        });
        expect(htmlCleaner.clean('<div><i>Test</i></div>')).toEqual(
            '<p><em>Test</em></p>');
    });


    it('prevent nested simple', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            allowedTags: ['div'],
            allowSelfNested: []
        });
        expect(htmlCleaner.clean('<div><div>Test</div></div>')).toEqual(
            '<div>Test</div>');
    });

    it('prevent nested very recursive', () => {
        const htmlCleaner = new CleanHtml2({
            wrapStandaloneInlineTags: false,
            allowedTags: ['div'],
            allowSelfNested: []
        });
        expect(htmlCleaner.clean(
            '<div>Pre <div><div>Test</div></div> Post</div>')).toEqual(
            '<div>Pre Test Post</div>');
    });

    // it('flatten nested list', () => {
    //     const htmlCleaner = new CleanHtml2({
    //         wrapStandaloneInlineTags: false,
    //         flattenNestedLists: true,
    //         allowedTags: ['ul', 'li'],
    //         allowSelfNested: []
    //     });
    //     const original = `
    //         <ul>
    //             <li>A</li>
    //             <li>B</li>
    //             <li>
    //                 C
    //                 <ul>
    //                     <li>C.1</li>
    //                     <li>C.2</li>
    //                 </ul>
    //             </li>
    //         </ul>
    //     `;
    //     expect(htmlCleaner.clean(original)).toEqual(
    //         '');
    // });
    //
});
