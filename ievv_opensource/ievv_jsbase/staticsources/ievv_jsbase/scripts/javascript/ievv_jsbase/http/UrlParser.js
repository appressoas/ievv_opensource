import QueryString from "./QueryString";


/**
 * URL parser.
 *
 * @example
 * const urlparser = new UrlParser('http://example.com/api/people?name=Jane');
 * querystring.queryString.set('search', 'doe');
 * // urlparser.buildUrl() === 'http://example.com/api/people?name=Jane&search=doe'
 */
export class UrlParser {
  constructor(url) {
    if(typeof url !== 'string') {
      throw new TypeError('url must be a string.');
    }
    const urlSplit = url.split('?');
    this._baseUrl = urlSplit[0];
    this._parsedBaseUrl = this._parseBaseUrl();

    /**
     * The query-string of the the URL.
     * @type {QueryString}
     */
    this.queryString = null;

    if(urlSplit.length > 1) {
      this.setQueryString(new QueryString(urlSplit[1]));
    } else {
      this.setQueryString(new QueryString());
    }
  }

  _splitDomainAndPath(domainAndPath) {
    let split = domainAndPath.split('/');
    let domain = split.shift();
    let path = '';
    if(split.length > 0) {
      path = `/${split.join('/')}`;
    }
    return {
      domain: domain,
      path: path
    }
  }

  _parseBaseUrl() {
    let parsedBaseUrl = {
      scheme: null,
      path: '',
      domain: null
    };
    if(this._baseUrl.match(/^[a-zA-Z0-9]+:\/\//)) {
      // We have a full URL (<scheme>://<domain><path>)
      let split = this._baseUrl.split('://');
      parsedBaseUrl.scheme = split.shift();
      let remaining = split.join('://');
      let domainAndPath = this._splitDomainAndPath(remaining);
      parsedBaseUrl.domain = domainAndPath.domain;
      parsedBaseUrl.path = domainAndPath.path;
    } else if(this._baseUrl.length > 0 && this._baseUrl.substring(0, 1) == '/') {
      // We have path only
      parsedBaseUrl.path = `${this._baseUrl}`;
    } else {
      // We have domain and path, but no scheme (<domain><path>)
      let domainAndPath = this._splitDomainAndPath(this._baseUrl);
      parsedBaseUrl.domain = domainAndPath.domain;
      parsedBaseUrl.path = domainAndPath.path;
    }
    return parsedBaseUrl;
  }

  get scheme() {
    return this._parsedBaseUrl.scheme;
  }

  get path() {
    return this._parsedBaseUrl.path;
  }

  get domain() {
    return this._parsedBaseUrl.domain;
  }

  /**
   * Build the URL.
   * @returns {String} The built URL.
   */
  buildUrl() {
    let url = this._baseUrl;
    if(!this.queryString.isEmpty()) {
      url = `${url}?${this.queryString.urlencode()}`;
    }
    return url;
  }

  /**
   * Set/replace the query-string.
   *
   * @param {QueryString} queryStringObject The QueryString object
   *      to replace the current query-string with.
   *
   * @example
   * const urlparser = UrlParser('http://example.com/api/people');
   * const querystring = new QueryString();
   * querystring.set('search', 'doe');
   * urlparser.setQueryString(querystring);
   * // urlparser.buildUrl() === 'http://example.com/api/people?search=doe'
   */
  setQueryString(queryStringObject) {
    this.queryString = queryStringObject;
  }
}
