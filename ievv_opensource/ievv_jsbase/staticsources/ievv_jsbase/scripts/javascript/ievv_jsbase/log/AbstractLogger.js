/**
 */
export default class AbstractLogger {
    LEVEL_DEBUG = 4;
    LEVEL_LOG = 3;
    LEVEL_WARN = 2;
    LEVEL_ERROR = 1;
    LEVEL_SILENT = 0;

    constructor() {
        this.logLevel = this.LEVEL_ERROR;
    }

    getLogLevel() {
        throw new Error('Must be overridden in subclasses.');
    }

    /**
     * Send a message to one of the target loggers.
     *
     * @param targetLog Must be one of ``log``, ``warn`` or ``error``.
     * @param args Arguments for the logger.
     *
     * @example
     * let data = {a: 10};
     * message('error', 'This is a test. Data:', data);
     */
    message(targetLog, ...args) {
        this[targetLog](...args);
    }

    /**
     * exposes console.log. Will only print if current level is higher than LEVEL_LOG
     * @returns {any} console.log
     */
    get log() {
        if (this.logLevel >= this.LEVEL_LOG) {
            return console.log.bind(console);
        }
    }

    /**
     * exposes console.warn. Will only print if current level is higher than LEVEL_WARN
     * @returns {any} console.warn
     */
    get warn() {
        if(this.logLevel >= this.LEVEL_WARN) {
            return console.warn.bind(console);
        }
    }

    /**
     * exposes console.error. Will only print if current level is higher than LEVEL_ERROR
     * @returns {any} console.error
     */
    get error() {
        if (this.logLevel >= this.LEVEL_ERROR) {
            return console.error.bind(console);
        }
    }
}
