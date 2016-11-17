import {PostCleanContentEditableHtml} from "../CleanContentEditableHtml";
import CleanContentEditableHtml from "../CleanContentEditableHtml";

describe('PostCleanContentEditableHtml', () => {

    it('wraps text in root in block element', () => {
        const wrapper = new PostCleanContentEditableHtml(
            'Some text');
        expect(wrapper.toString()).toEqual(
            '<p>Some text</p>');
    });

    it('wraps text in root in block element complex', () => {
        const wrapper = new PostCleanContentEditableHtml(
            'Some text<p>In block text</p>More text');
        expect(wrapper.toString()).toEqual(
            '<p>Some text</p><p>In block text</p><p>More text</p>');
    });

    it('wraps inline elements in root in block element', () => {
        const wrapper = new PostCleanContentEditableHtml(
            '<em>Some text</em>');
        expect(wrapper.toString()).toEqual(
            '<p><em>Some text</em></p>');
    });

    it('does not wrap inline elements with parent in block element', () => {
        const wrapper = new PostCleanContentEditableHtml(
            '<div><em>Some text</em></div>');
        expect(wrapper.toString()).toEqual(
            '<div><em>Some text</em></div>');
    });

    it('wraps inline elements in root in block element compex', () => {
        const wrapper = new PostCleanContentEditableHtml(
            '<em>Some text</em><p>In <em>block</em></p><strong>More text</strong>');
        expect(wrapper.toString()).toEqual(
            '<p><em>Some text</em></p><p>In <em>block</em></p><p><strong>More text</strong></p>');
    });

    it('inline containing block element', () => {
        const wrapper = new PostCleanContentEditableHtml(
            '<em><div>Test</div></em>');
        expect(wrapper.toString()).toEqual(
            '<p><em>Test</em></p>');
    });

    it('inline containing block element deep', () => {
        const wrapper = new PostCleanContentEditableHtml(
            '<div><em><div><p>Hello</p> <p>World</p></div></em></div>');
        expect(wrapper.toString()).toEqual(
            '<div><em>Hello World</em></div>');
    });
});


describe('CleanContentEditableHtml', () => {
    it('wraps text in root in block element', () => {
        const cleanedHtml = new CleanContentEditableHtml().clean('Some text');
        expect(cleanedHtml).toEqual(
            '<p>Some text</p>');
    });

    it('removes div', () => {
        const cleanedHtml = new CleanContentEditableHtml().clean(
            '<div>Some text</div>');
        expect(cleanedHtml).toEqual(
            '<p>Some text</p>');
    });

    it('removes class', () => {
        const cleanedHtml = new CleanContentEditableHtml().clean(
            '<em class="test">Some text</em>');
        expect(cleanedHtml).toEqual(
            '<p><em>Some text</em></p>');
    });
});
