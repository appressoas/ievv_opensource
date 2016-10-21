import HttpResponse from "./HttpResponse";


export default class HttpJsonResponse extends HttpResponse {
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
