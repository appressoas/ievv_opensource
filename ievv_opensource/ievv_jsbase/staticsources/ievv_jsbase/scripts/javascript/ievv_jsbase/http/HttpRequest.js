import HttpResponse from "./HttpResponse";


/**
 * API for performing HTTP requests.
 *
 * Example - make a POST request:
 * ```
 * let request = new HttpRequest('http://example.com/api/users/');
 * request.post('Hello world').then(function(response) {
 *     // Success - response is a HttpResponse object.
 *     console.log(response.toPrettyString());
 *     if(response.isSuccess()) {
 *         console.log('Success: ', response.body);
 *     } else if (response.isRedirect) {
 *         console.log('Hmm strange, we got a redirect instead of a 2xx response.');
 *     }
 * }, function(response) {
 *     // Error - response is a HttpResponse object.
 *     console.error(response.toPrettyString());
 *     if(response.isClientError()) {
 *         console.log('We got a 4xx response!', response.body);
 *     } else if (response.isServerError()) {
 *         console.log('We got a 5xx response!', response.body);
 *     } else if (response.isConnectionRefused()) {
 *         console.log('Connection refused.');
 *     }
 * });
 * ```
 *
 * It works exactly the same for GET, PUT, PATCH and HEAD requests, just
 * use {@link HttpRequest#get}, {@link HttpRequest#put},
 * {@link HttpRequest#patch} and {@link HttpRequest#head}.
 */
class HttpRequest {
    constructor(url) {
        this.url = url;
        this.request = new window.XMLHttpRequest();
    }

    /**
     * Send the request.
     *
     * @param method The HTTP method. I.e.: "get", "post", ...
     * @param data Request body data. This is sent through
     *      {@link HttpRequest#makeRequestBody} before it
     *      is sent.
     *
     * @return A Promise where both the
     */
    send(method, data) {
        method = method.toUpperCase();
        return new Promise((resolve, reject) => {
            this.request.open(method, this.url, true);
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
     * @param name The header name. E.g.: ``"Content-type"``.
     * @param value The header value.
     */
    setRequestHeader(name, value) {
        this.request.setRequestHeader(name, value);
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
        if(response.isSuccess() || response.isRedirect()) {
            resolve(response);
        } else {
            reject(response);
        }
    }
}

export default HttpRequest;
