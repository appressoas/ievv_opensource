import parseHtml from "../../dom/parseHtml";

describe('parseHtml', () => {
    it('parseHtml() single element', () => {
        let element = parseHtml('<p>Test</p>');
        expect(element.querySelectorAll('p').length).toBe(1);
        expect(element.querySelectorAll('p')[0].textContent).toBe('Test');
    });

    it('parseHtml() multiple elements', () => {
        let element = parseHtml('<p>Test1</p><p>Test2</p>');
        expect(element.querySelectorAll('p').length).toBe(2);
        expect(element.querySelectorAll('p')[0].textContent).toBe('Test1');
        expect(element.querySelectorAll('p')[1].textContent).toBe('Test2');
    });

    it('parseHtml() tree', () => {
        let element = parseHtml('<p><em>Test1</em><strong>Test2</strong></p>');
        expect(element.querySelectorAll('p').length).toBe(1);
        expect(element.querySelectorAll('p em')[0].textContent).toBe('Test1');
        expect(element.querySelectorAll('p strong')[0].textContent).toBe('Test2');
    });

    it('parseHtml() HTML document', () => {
        let element = parseHtml('<html><body><p>Test</p></body></html>');
        expect(element.querySelectorAll('p').length).toBe(1);
        expect(element.querySelectorAll('p')[0].textContent).toBe('Test');
    });
});
