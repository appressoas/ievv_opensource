import HttpJsonRequest from "./HttpJsonRequest";
import HttpCookies from "./HttpCookies";


export default class HttpDjangoJsonRequest extends HttpJsonRequest {
    setDefaultRequestHeaders(method) {
        super.setDefaultRequestHeaders(method);
        method = method.toUpperCase();
        let shouldAddCsrfToken = !(method === 'GET' || method == 'HEAD');
        if(shouldAddCsrfToken) {
            let cookies = new HttpCookies();
            this.setRequestHeader("X-CSRFToken", cookies.getValue('csrftoken'));
        }
    }
}
