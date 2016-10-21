import HttpJsonRequest from "./HttpJsonRequest";
import HttpCookies from "./HttpCookies";


class HttpDjangoJsonRequest extends HttpJsonRequest {
    setDefaultRequestHeaders(method) {
        super.setDefaultRequestHeaders(method);
        let shouldAddCsrfToken = !(method === 'GET' || method == 'HEAD');
        if(shouldAddCsrfToken) {
            let cookies = new HttpCookies();
            this.setRequestHeader("X-CSRFToken", cookies.getValue('csrftoken'));
        }
    }
}

export default HttpDjangoJsonRequest;
