import Cookies from '../../http/Cookies';
import {CookieNotFoundError} from '../../http/Cookies';


describe('Cookies', () => {
    it('Cookies.contains()', () => {
        const cookies = new Cookies('other=othervalue;test=testvalue;evenanother=evenanothervalue');
        expect(cookies.contains('test')).toBe(true);
        expect(cookies.contains('other')).toBe(true);
        expect(cookies.contains('evenanother')).toBe(true);
    });

    it('Cookies.get() simple', () => {
        const cookies = new Cookies('test=testvalue');
        expect(cookies.get('test')).toBe('testvalue');
    });

    it('Cookies.get() from document', () => {
        document.cookie = 'fromdocument=fromdocumentvalue';
        const cookies = new Cookies();
        expect(cookies.get('fromdocument')).toBe('fromdocumentvalue');
    });

    it('Cookies.get() multiple cookies', () => {
        const cookies = new Cookies('other=othervalue;test=testvalue;evenanother=evenanothervalue');
        expect(cookies.get('test')).toBe('testvalue');
        expect(cookies.get('other')).toBe('othervalue');
        expect(cookies.get('evenanother')).toBe('evenanothervalue');
    });

    it('Cookies.get() fallback', () => {
        const cookies = new Cookies('test=testvalue');
        expect(cookies.get('test2', 'thefallbackvalue')).toBe('thefallbackvalue');
    });

    it('Cookies.getStrict()', () => {
        const cookies = new Cookies('test=testvalue');
        expect(() => cookies.getStrict('test2')).toThrowError(CookieNotFoundError);
        expect(() => cookies.getStrict('test2')).toThrowError('Cookie not found: "test2".');
    });
});
