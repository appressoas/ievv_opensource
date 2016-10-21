import HttpJsonRequest from "./HttpJsonRequest";
import HttpCookies from "./HttpCookies";


class HttpDjangoJsonRequest extends HttpJsonRequest {
    constructor(...args) {
        super(...args);
        let cookies = new HttpCookies();
        this.csrftoken = cookies.getStrict('csrftoken');
    }

    setDefaultRequestHeaders(method) {
        super.setDefaultRequestHeaders(method);
        let shouldAddCsrfToken = !(method === 'GET' || method == 'HEAD');
        if(shouldAddCsrfToken) {
            this.setRequestHeader("X-CSRFToken", this.csrftoken);
        }
    }
}

export default HttpDjangoJsonRequest;
