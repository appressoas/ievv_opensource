import HttpResponse from "./HttpResponse";
import QueryString from "./QueryString";
import {UrlParser} from "./UrlParser";


/**
 * API for performing HTTP requests.

 * @example <caption>Make a POST request</caption>
 * const request = new HttpRequest('http://example.com/api/users/');
 * request.post('Hello world')
 *     .then((response) => {
 *         // Success - response is a HttpResponse object.
 *         console.log(response.toString());
 *         if(response.isSuccess()) {
 *             console.log('Success: ', response.body);
 *         } else if (response.isRedirect) {
 *             console.log('Hmm strange, we got a redirect instead of a 2xx response.');
 *         }
 *     })
 *     .catch((error) => {
 *         // Error - response is an HttpError object.
 *         console.error(error.toString());
 *         if(error.response.isRedirect()) {
 *             // Yes - redirect is treated as an error by default.
 *             // you can change this by supplying an extra argument
 *             // to HttpResponse()
 *             console.log('We got a 3xx response!', error.response.body);
 *         } else if(error.response.isClientError()) {
 *             console.log('We got a 4xx response!', error.response.body);
 *         } else if (error.response.isServerError()) {
 *             console.log('We got a 5xx response!', error.response.body);
 *         } else if (error.response.isConnectionRefused()) {
 *             console.log('Connection refused.');
 *         }
 *     });
 *
 * @example <caption>Make a GET request with a querystring</caption>
 * const request = new HttpRequest('http://example.com/api/users/');
 * request.urlParser.queryString.set('search', 'doe');
 * request.get()
 *     .then((response) => {
 *         console.log('Success!', response.toString());
 *     })
 *     .catch((error) => {
 *         console.error('Error:', error.toString());
 *     });
 */
export default class HttpRequest {
    /**
     * @param {string} url The URL to request.
     *      If this is supplied, it is passed to
     *      {@link HttpRequest#setUrl}
     */
    constructor(url) {
        this._treatRedirectResponseAsError = true;
        this.request = new XMLHttpRequest();
        this._urlParser = null;
        if(typeof url !== 'undefined') {
            this.setUrl(url);
        }
    }

    /**
     * Get the parsed URL of the request.
     *
     * @returns {UrlParser} The UrlParser for the parsed URL.
     */
    get urlParser() {
        return this._urlParser;
    }

    /**
     * Set the URL of the request.
     *
     * @param {String} url The URL.
     */
    setUrl(url) {
        this._urlParser = new UrlParser(url);
    }

    /**
     * Set how we treat 3xx responses.
     *
     * By default they are treated as errors, but you can change
     * this behavior by calling this function.
     *
     * @param {bool} treatRedirectResponseAsError Treat 3xx responses as
     *      errors?
     *
     * @example <caption>Do not treat 3xx responses as error</caption>
     * const request = HttpRequest('http://example.com/api/');
     * request.setTreatRedirectResponseAsError(false);
     */
    setTreatRedirectResponseAsError(treatRedirectResponseAsError) {
        this._treatRedirectResponseAsError = treatRedirectResponseAsError;
    }

    /**
     * Send the request.
     *
     * @param method The HTTP method. I.e.: "get", "post", ...
     * @param data Request body data. This is sent through
     *      {@link HttpRequest#makeRequestBody} before it
     *      is sent.*
     * @return A Promise.
     *
     *      The resolve function argument is an
     *      an object of whatever {@link HttpRequest#makeResponse}
     *      returns.
     *
     *      The reject function argument is a
     *      {@link HttpResponseError} object created using
     *      {@link HttpResponse#toError}.
     */
    send(method, data) {
        method = method.toUpperCase();
        if(this._urlParser === null) {
            throw new TypeError('Can not call send() without an url.');
        }
        return new Promise((resolve, reject) => {
            this.request.open(method, this.urlParser.buildUrl(), true);
            this.setDefaultRequestHeaders(method);
            this.request.onload  = () => this._onComplete(resolve, reject);
            this.request.onerror = () => this._onComplete(resolve, reject);
            this.request.send(this.makeRequestBody(data));
        });
    }

    /**
     * Shortcut for ``send("get", data)``.
     *
     * @see {@link HttpRequest#send}
     */
    get(data) {
        return this.send('get', data);
    }

    /**
     * Shortcut for ``send("head", data)``.
     *
     * @see {@link HttpRequest#send}
     */
    head(data) {
        return this.send('head', data);
    }

    /**
     * Shortcut for ``send("post", data)``.
     *
     * @see {@link HttpRequest#send}
     */
    post(data) {
        return this.send('post', data);
    }

    /**
     * Shortcut for ``send("put", data)``.
     *
     * @see {@link HttpRequest#send}
     */
    put(data) {
        return this.send('put', data);
    }

    /**
     * Shortcut for ``send("patch", data)``.
     *
     * @see {@link HttpRequest#send}
     */
    patch(data) {
        return this.send('patch', data);
    }

    /**
     * Shortcut for ``send("delete", data)``.
     *
     * Named httpdelete to avoid crash with builtin keyword ``delete``.
     *
     * @see {@link HttpRequest#send}
     */
    httpdelete(data) {
        return this.send('delete', data);
    }

    /**
     * Make request body from the provided data.
     *
     * By default this just returns the provided data,
     * but subclasses can override this to perform automatic
     * conversion.
     *
     * Must return a string.
     */
    makeRequestBody(data) {
        return data;
    }

    /**
     * Creates a {@link HttpResponse}.
     * @returns {HttpResponse}
     */
    makeResponse() {
        return new HttpResponse(this.request);
    }

    /**
     * Set a request header.
     *
     * @param header The header name. E.g.: ``"Content-type"``.
     * @param value The header value.
     */
    setRequestHeader(header, value) {
        this.request.setRequestHeader(header, value);
    }

    /**
     * Set default request headers.
     *
     * Does nothing by default, but subclasses can override this.
     *
     * @param method The HTTP request method (GET, POST, PUT, ...).
     *      Will always be uppercase.
     */
    setDefaultRequestHeaders(method) {}

    _onComplete(resolve, reject) {
        let response = this.makeResponse();
        let isSuccess = false;
        if(this._treatRedirectResponseAsError) {
            isSuccess = response.isSuccess();
        } else {
            isSuccess = response.isSuccess() || response.isRedirect();
        }
        if(isSuccess) {
            resolve(response);
        } else {
            reject(response.toError());
        }
    }
}
