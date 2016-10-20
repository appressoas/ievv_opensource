import Cookie from '../Cookie';


test('Cookie("test").cookieName to be "test"', () => {
    const cookie = new Cookie('test');
    expect(cookie.cookieName).toBe('test');
});
