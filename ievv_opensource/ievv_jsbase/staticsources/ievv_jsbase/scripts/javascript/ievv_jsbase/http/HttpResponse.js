/**
 * HTTP response.
 *
 * Wraps a XMLHttpRequest to make it easier to get
 * information about the response from the server.
 */
export default class HttpResponse {
    /**
     *
     * @param request A XMLHttpRequest object.
     */
    constructor(request) {
        this.request = request;
    }

    /**
     * Returns ``true`` if {@link HttpResponse#status} is
     * 200 or larger and less than 300.
     */
    isSuccess() {
        return this.status >= 200 && this.status < 300;
    }

    /**
     * Returns ``true`` if {@link HttpResponse#status} is
     * 300 or larger and less than 400.
     */
    isRedirect() {
        return this.status >= 300 && this.status < 400;
    }

    /**
     * Returns ``true`` if {@link HttpResponse#status} is
     * 400 or larger and less than 500.
     */
    isClientError() {
        return this.status >= 400 && this.status < 500;
    }

    /**
     * Returns ``true`` if {@link HttpResponse#status} is
     * 500 or larger.
     */
    isServerError() {
        return this.status >= 500;
    }

    /**
     * Returns ``true`` if {@link HttpResponse#status} is 0.
     * Assuming the XMLHttpRequest was actually sent, this
     * means that the connection was refused.
     */
    isConnectionRefused() {
        return this.status === 0;
    }

    /**
     * Get the status code of the response (the status attribute of the XMLHttpRequest).
     */
    get status() {
        return this.request.status;
    }

    /**
     * Get the response body (the responseText attribute of the XMLHttpRequest).
     */
    get body() {
        return this.request.responseText;
    }

    /**
     * Get the response header as string.
     */
    responseHeaderToString() {
        if(this.connectionRefused) {
            return "ERROR: Connection refused";
        } else {
            return `HTTP ${this.status}\n${this.request.getAllResponseHeaders()}`;
        }
    }

    /**
     * Format as a string suitable for debugging.
     */
    toString() {
        return `${this.responseHeaderToString()}\n\n${this.body}`
    }

    /**
     * Get {@link HttpResponse#body} pretty formatted.
     *
     * By default, this just returns {@link HttpResponse#body}
     * but subclasses can override this to prettify the body
     * if they know the output format of the body.
     */
    getPrettyfiedBody() {
        return this.body;
    }

    /**
     * Format as a prettified string suitable for debugging.
     *
     * Same format as  the same as {@link HttpResponse#toString}
     * except that the body is formatted using {@link HttpResponse#getPrettyfiedBody}.
     */
    toPrettyString() {
        return `${this.responseHeaderToString()}\n\n${this.getPrettyfiedBody()}`
    }
}
