import Cookies from './Cookies.js';


export class HttpResponse {
    constructor(request, options) {
        this.request = request;
        this.options = options;
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

    get text() {
        return this.request.responseText;
    }

    toString() {
        if(this.connectionRefused) {
            return "ERROR: Connection refused";
        } else {
            return `HTTP ${this.status}\n${this.text}`;
        }
    }

    toPrettyString() {
        if(this.connectionRefused) {
            return "ERROR: Connection refused";
        } else {
            let prettyBody;
            try {
                prettyBody = JSON.stringify(this.data, null, 2);
            } catch (SyntaxError) {
                prettyBody = this.text;
            }
            return `HTTP ${this.status}\n${prettyBody}`;
        }
    }
}


export class JsonHttpResponse extends HttpResponse {
    constructor(request, options) {
        super(request, options);
    }

    get data() {
        if(this.connectionRefused) {
            return null;
        } else {
            return this.parseResponseTextAsJson();
        }
    }

    parseResponseTextAsJson() {
        return JSON.parse(this.text);
    }
}


export class HttpRequest {
    constructor(url) {
        this.url = url;
        this.request = new XMLHttpRequest();
    }

    makeRequestBody(data) {
        return data;
    }

    makeResponse() {
        return new HttpResponse(this.request);
    }

    setDefaultRequestHeaders() {
    }

    open(method, data, responseCallback) {
        this.request.open(method, this.url, true);
        this.setDefaultRequestHeaders();
        this.request.onload  = () => this.onComplete(responseCallback);
        this.request.onerror = () => this.onComplete(responseCallback);
        this.request.send(this.makeRequestBody(data));
    }

    post(data, responseCallback) {
        this.open('POST', data, responseCallback);
    }

    onComplete(responseCallback) {
        responseCallback(this.makeResponse());
    }
}


export class JsonHttpRequest extends HttpRequest {
    makeRequestBody(data) {
        return JSON.stringify(data);
    }

    makeResponse() {
        return new JsonHttpResponse(this.request);
    }

    setDefaultRequestHeaders() {
        this.request.setRequestHeader('Content-Type', `application/json; charset=UTF-8`);
    }
}


export class DjangoJsonHttpRequest extends JsonHttpRequest {
    setDefaultRequestHeaders() {
        super.setDefaultRequestHeaders();
        let cookies = new Cookies();
        this.request.setRequestHeader("X-CSRFToken", cookies.getValue('csrftoken'));
    }
}
