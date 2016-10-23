import HttpRequest from '../../http/HttpRequest';


export class XMLHttpRequestMock {
    constructor(requestEventMethodName, resultingRequest) {
        this.requestEventMethodName = requestEventMethodName;
        this.onerror = null;
        this.onload = null;
        this.headers = [];
        this.sentData = null;
        this.resultingRequest = resultingRequest;
    }

    open() {}

    setRequestHeader(header, value) {
        this.headers.push({
            header: header,
            value: value
        });
    }

    send(data) {
        this.sentData = data;
        Object.assign(this, this.resultingRequest);
        this[this.requestEventMethodName]();
    }
}

describe('HttpRequest', () => {

    it('Connection error', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onerror', {
            status: 0
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(0);
            expect(response.isConnectionRefused()).toBe(true);
        });
    });

    it('5xx response', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 500
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(500);
            expect(response.isServerError()).toBe(true);
        });
    });

    it('4xx response', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 400
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(400);
            expect(response.isClientError()).toBe(true);
        });
    });

    it('3xx response', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 301
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(301);
            expect(response.isRedirect()).toBe(true);
        });
    });

    it('Successful request', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200
        });
        return httprequest.post('test').then(function(response) {
            expect(response.status).toBe(200);
            expect(response.isSuccess()).toBe(true);
        }, function(response) {
            throw new Error('This should not be called!');
        });
    });

    it('3xx response treatRedirectResponseAsError=false', () => {
        const httprequest = new HttpRequest(null, false);
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 301
        });
        return httprequest.post('test').then(function(response) {
            expect(response.status).toBe(301);
            expect(response.isRedirect()).toBe(true);
        }, function(response) {
        });
    });

    it('Successful request body', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200,
            responseText: 'test'
        });
        return httprequest.post('test').then(function(response) {
            expect(response.body).toBe('test');
        });
    });
});
