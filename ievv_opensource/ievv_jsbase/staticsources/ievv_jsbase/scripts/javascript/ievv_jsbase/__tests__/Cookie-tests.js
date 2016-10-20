import Cookie from '../Cookie';


describe('Cookie', () => {
    it('Cookie("test").cookieName to be "test"', () => {
        const cookie = new Cookie('test');
        expect(cookie.cookieName).toBe('test');
    });

    it('Cookie.getValue() simple', () => {
        document.cookie = 'test=testvalue';
        const cookie = new Cookie('test');
        expect(cookie.getValue()).toBe('testvalue');
    });

    it('Cookie.getValue() multiple cookies', () => {
        document.cookie = 'other=othervalue;test=testvalue;evenanother=evenanothervalue';
        const cookie = new Cookie('test');
        expect(cookie.getValue()).toBe('testvalue');
    });
});
