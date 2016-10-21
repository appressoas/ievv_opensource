/**
 * HTTP response.
 *
 * Wraps a XMLHttpRequest to provide information about the
 * response from the server.
 */
export default class HttpResponse {
    constructor(request) {
        this.request = request;
    }

    get status() {
        return this.request.status;
    }

    get success() {
        if(this.status) {
            return this.status >= 200 && this.status < 400;
        } else {
            return false;
        }
    }

    get connectionRefused() {
        return this.status === 0;
    }

    get body() {
        return this.request.responseText;
    }

    toString() {
        if(this.connectionRefused) {
            return "ERROR: Connection refused";
        } else {
            return `HTTP ${this.status}\n${this.body}`;
        }
    }

    /**
     * Get {@link HttpRequest#body} pretty formatted.
     */
    getPrettyfiedBody() {
        // let prettyBody;
        // try {
        //     prettyBody = JSON.stringify(this.data, null, 2);
        // } catch (SyntaxError) {
        //     prettyBody = this.body;
        // }
        return this.body;
    }

    toPrettyString() {
        if(this.connectionRefused) {
            return "ERROR: Connection refused";
        } else {
            return `HTTP ${this.status}\n${getPrettyfiedBody()}`;
        }
    }
}
