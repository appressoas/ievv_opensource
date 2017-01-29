import QueryString from "../../http/QueryString";
import {UrlParser} from "../../http/UrlParser";


describe('UrlParser', () => {
  it('setQueryString', () => {
    const urlparser = new UrlParser('http://example.com/');
    expect(urlparser.queryString.isEmpty()).toBe(true);
    const querystring = new QueryString();
    querystring.set('name', 'Jane');
    urlparser.setQueryString(querystring);
    expect(urlparser.queryString.urlencode()).toBe('name=Jane');
  });

  it('buildUrl() no querystring', () => {
    const urlparser = new UrlParser('http://example.com/api/people');
    expect(urlparser.buildUrl()).toBe('http://example.com/api/people');
  });

  it('buildUrl() with querystring', () => {
    const urlparser = new UrlParser('http://example.com/api/people');
    urlparser.queryString = new QueryString('name=Jane');
    expect(urlparser.buildUrl()).toBe('http://example.com/api/people?name=Jane');
  });

  it('with scheme - get scheme http', () => {
    const urlparser = new UrlParser('http://example.com/api/people');
    expect(urlparser.scheme).toBe('http');
  });

  it('with scheme - get scheme https', () => {
    const urlparser = new UrlParser('https://example.com/api/people');
    expect(urlparser.scheme).toBe('https');
  });

  it('with scheme - get domain', () => {
    const urlparser = new UrlParser('http://example.com/api/people');
    expect(urlparser.domain).toBe('example.com');
  });

  it('with scheme - get path', () => {
    const urlparser = new UrlParser('http://example.com/api/people');
    expect(urlparser.path).toBe('/api/people');
  });

  it('with scheme, no path - get path', () => {
    const urlparser = new UrlParser('http://example.com');
    expect(urlparser.path).toBe('');
  });

  it('no scheme, with domain - get domain', () => {
    const urlparser = new UrlParser('example.com/api/people');
    expect(urlparser.domain).toBe('example.com');
  });

  it('no scheme, with domain - get path', () => {
    const urlparser = new UrlParser('example.com/api/people');
    expect(urlparser.path).toBe('/api/people');
  });

  it('no scheme, with domain, no path - get path', () => {
    const urlparser = new UrlParser('example.com');
    expect(urlparser.path).toBe('');
  });

  it('no scheme, no domain - get path', () => {
    const urlparser = new UrlParser('/api/people');
    expect(urlparser.path).toBe('/api/people');
  });

  it('no scheme, no domain, no path - get path', () => {
    const urlparser = new UrlParser('');
    expect(urlparser.path).toBe('');
  });

});
