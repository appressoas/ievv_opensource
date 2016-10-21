import makeCustomError from "../makeCustomError";


export let HttpCookieNotFoundError = makeCustomError('HttpCookieNotFoundError');


class HttpCookies {
    constructor(rawCookies) {
        this.rawCookies = rawCookies || document.cookie;
        this.cookies = this.__parse();
    }

    __parse() {
        let cookies = {};
        if (this.rawCookies && this.rawCookies !== '') {
            let cookiesArray = this.rawCookies.split(';');
            for (let i = 0; i < cookiesArray.length; i++) {
                let cookie = cookiesArray[i].trim();
                let cookieArray = cookie.split('=', 2);
                if(cookieArray.length === 2) {
                    let name = cookieArray[0];
                    let value = cookieArray[1];
                    cookies[name.trim()] = value.trim();
                }
            }
        }
        return cookies;
    }

    get(cookieName, fallback) {
        let value = this.cookies[cookieName];
        if(typeof value === 'undefined') {
            return fallback;
        } else {
            return value;
        }
    }

    getStrict(cookieName) {
        let value = this.get(cookieName);
        if(typeof value === 'undefined') {
            throw new HttpCookieNotFoundError(`Cookie not found: "${cookieName}".`);
        }
    }

    contains(cookieName) {
        return typeof this.cookies[cookieName] !== 'undefined';
    }
}

export default HttpCookies;
