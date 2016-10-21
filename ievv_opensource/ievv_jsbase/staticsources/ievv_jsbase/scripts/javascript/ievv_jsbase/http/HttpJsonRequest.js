import HttpJsonResponse from "./HttpJsonResponse";


export default class JsonHttpRequest extends HttpRequest {
    makeRequestBody(data) {
        return JSON.stringify(data);
    }

    makeResponse() {
        return new HttpJsonResponse(this.request);
    }

    setDefaultRequestHeaders(method) {
        super.setDefaultRequestHeaders(method);
        this.setRequestHeader('Content-Type', `application/json; charset=UTF-8`);
    }
}
