import LOGLEVEL from "./loglevel";


/**
 */
export default class AbstractLogger {
  getLogLevel() {
    throw new Error('Must be overridden in subclasses.');
  }

  _noOutput() {

  }

  /**
   * Exposes console.log. Will only print if current level is
   * higher than or equal to {@link LogLevels#DEBUG}.
   * @returns {Function} console.log
   */
  get debug() {
    if (this.getLogLevel() >= LOGLEVEL.DEBUG) {
      return console.log.bind(console);
    }
    return this._noOutput;
  }

  /**
   * Exposes console.log. Will only print if current level is
   * higher than or equal to {@link LogLevels#INFO}.
   * @returns {Function} console.log
   */
  get info() {
    if (this.getLogLevel() >= LOGLEVEL.INFO) {
      return console.log.bind(console);
    }
    return this._noOutput;
  }

  /**
   * Exposes console.warn. Will only print if current level is
   * higher than or equal to {@link LogLevels#WARNING}.
   * @returns {Function} console.warn
   */
  get warning() {
    if(this.getLogLevel() >= LOGLEVEL.WARNING) {
      return console.warn.bind(console);
    }
    return this._noOutput;
  }

  /**
   * Exposes console.error. Will only print if current level is
   * higher than or equal to {@link LogLevels#ERROR}.
   * @returns {Function} console.error
   */
  get error() {
    if (this.getLogLevel() >= LOGLEVEL.ERROR) {
      return console.error.bind(console);
    }
    return this._noOutput;
  }

  /**
   * Calls the provided function if loglevel is higher
   * than or equal to {@link LogLevels#DEBUG}.
   *
   * @param {function} callable
   */
  ifDebug(callable) {
    if (this.getLogLevel() >= LOGLEVEL.DEBUG) {
        callable();
    }
  }

  /**
   * Calls the provided function if loglevel is higher
   * than or equal to {@link LogLevels#INFO}.
   *
   * @param {function} callable
   */
  ifInfo(callable) {
    if (this.getLogLevel() >= LOGLEVEL.INFO) {
        callable();
    }
  }

  /**
   * Calls the provided function if loglevel is higher
   * than or equal to {@link LogLevels#WARNING}.
   *
   * @param {function} callable
   */
  ifWarning(callable) {
    if (this.getLogLevel() >= LOGLEVEL.WARNING) {
        callable();
    }
  }

  /**
   * Calls the provided function if loglevel is higher
   * than or equal to {@link LogLevels#ERROR}.
   *
   * @param {function} callable
   */
  ifError(callable) {
    if (this.getLogLevel() >= LOGLEVEL.ERROR) {
        callable();
    }
  }

}
