import {HttpRequest} from '../http/HttpRequest';


class XMLHttpRequestMock {
    constructor(requestEventMethodName, resultingRequest) {
        this.requestEventMethodName = requestEventMethodName;
        this.onerror = null;
        this.onload = null;
        this.resultingRequest = resultingRequest;
    }

    open() {
    }

    send() {
        Object.assign(this, this.resultingRequest);
        this[this.requestEventMethodName]();
    }
}

describe('HttpRequest', () => {
    it('Unsuccessful request that reached server', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 400
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(400);
            expect(response.connectionRefused).toBe(false);
        });
    });

    it('Unsuccessful request that did not reach server', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onerror', {
            status: 0
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(0);
            expect(response.connectionRefused).toBe(true);
        });
    });

    it('Successful request', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200
        });
        return httprequest.post('test').then(function(response) {
            expect(response.status).toBe(200);
        }, function(response) {
            throw new Error('This should not be called!');
        });
    });

    it('Successful request text', () => {
        const httprequest = new HttpRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200,
            responseText: 'test'
        });
        return httprequest.post('test').then(function(response) {
            expect(response.text).toBe('test');
        });
    });
});
