import HttpResponse from "./HttpResponse";


class HttpJsonResponse extends HttpResponse {
    constructor(request, options) {
        super(request, options);
    }

    get bodydata() {
        if(this.isConnectionRefused()) {
            return null;
        } else {
            return this.parseResponseTextAsJson();
        }
    }

    parseResponseTextAsJson() {
        return JSON.parse(this.body);
    }

    getPrettyfiedBody() {
        let prettyBody;
        try {
            prettyBody = JSON.stringify(this.data, null, 2);
        } catch (SyntaxError) {
            prettyBody = this.body;
        }
        return prettyBody;
    }
}

export default HttpJsonResponse;
