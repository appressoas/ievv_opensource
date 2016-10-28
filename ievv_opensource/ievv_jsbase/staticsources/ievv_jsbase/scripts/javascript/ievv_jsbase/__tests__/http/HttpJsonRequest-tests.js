import HttpJsonRequest from '../../http/HttpJsonRequest';
import {XMLHttpRequestMock} from "./HttpRequest-tests";


describe('HttpJsonRequest', () => {
    it('Unsuccessful request that reached server', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 400
        });
        return httprequest.post('test').then(function(response) {
            throw new Error('This should not be called!');
        }, function(response) {
            expect(response.status).toBe(400);
            expect(response.isConnectionRefused()).toBe(false);
        });
    });

    it('Unsuccessful request that did not reach server', () => {
        const httprequest = new HttpJsonRequest();
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

    it('Successful request', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200
        });
        return httprequest.post('test').then(function(response) {
            expect(response.status).toBe(200);
        }, function(response) {
            throw new Error('This should not be called!');
        });
    });

    it('Successful request body', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200,
            responseText: 'test'
        });
        return httprequest.post('test').then(function(response) {
            expect(response.body).toBe('test');
        });
    });

    it('Successful request bodydata', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200,
            responseText: '{"a": 10}'
        });
        return httprequest.post('test').then(function(response) {
            expect(response.bodydata.a).toBe(10);
        });
    });

    it('Sets content-type', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200
        });
        return httprequest.post('test').then(function(response) {
            expect(httprequest.request.headers.length).toBe(1);
            expect(httprequest.request.headers[0].header).toBe(
                'Content-Type');
            expect(httprequest.request.headers[0].value).toBe(
                'application/json; charset=UTF-8');
        });
    });

    it('JSON encodes input data', () => {
        const httprequest = new HttpJsonRequest();
        httprequest.request = new XMLHttpRequestMock('onload', {
            status: 200
        });
        return httprequest.post({'a': 10}).then(function(response) {
            expect(httprequest.request.sentData).toBe('{"a":10}');
        });
    });
});