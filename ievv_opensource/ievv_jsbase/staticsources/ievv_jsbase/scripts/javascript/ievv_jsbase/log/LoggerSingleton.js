import Logger from "./Logger";
import LOGLEVEL from "./loglevel";

let _instance = null;


/**
 * A logging system.
 *
 * @example <caption>Create and use a logger</caption>
 * import LoggerSingleton from 'ievv_jsbase/log/LoggerSingleton';
 * let mylogger = new LoggerSingleton().loggerSingleton.getLogger('myproject.MyClass');
 * mylogger.debug('Hello debug world');
 * mylogger.info('Hello info world');
 * mylogger.warning('Hello warning world');
 * mylogger.error('Hello error world');
 *
 * @example <caption>Set a default loglevel for all loggers</caption>
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * new LoggerSingleton().setDefaultLogLevel(LOGLEVEL.DEBUG);
 *
 * @example <caption>Set a custom loglevel for a single logger</caption>
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * new LoggerSingleton().getLogger('mylogger').setLoglevel(LOGLEVEL.DEBUG);
 */
export default class LoggerSingleton {
    /**
     * Get an instance of the singleton.
     *
     * The first time this is called, we create a new instance.
     * For all subsequent calls, we return the instance that was
     * created on the first call.
     */
    constructor() {
        if(!_instance) {
            _instance = this;
        }
        this._loggerMap = new Map();
        this.reset();
        return _instance;
    }

    /**
     * Reset to default log level, and clear all
     * custom loggers.
     */
    reset() {
        this._logLevel = LOGLEVEL.WARNING;
        this._loggerMap.clear();
    }

    /**
     * Get the default log level.
     *
     * Defaults to {@link LogLevels#WARNING} if not overridden
     * with {@LoggerSingleton#setDefaultLogLevel}.
     *
     * @returns {int} One of the loglevels defined in {@link LogLevels}
     */
    getDefaultLogLevel() {
        return this._logLevel;
    }

    /**
     * Set the default loglevel.
     *
     * All loggers use this by default unless
     * you override their loglevel.
     *
     * @example <caption>Override loglevel of a specific logger</caption>
     * import LoggerSingleton from 'ievv_jsbase/log/LoggerSingleton';
     * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
     * let loggerSingleton = new LoggerSingleton();
     * loggerSingleton.getLogger('mylogger').setLogLevel(LOGLEVEL.DEBUG);
     *
     * @param logLevel The log level. Must be one of the loglevels
     *      defined in {@link LogLevels}.
     * @throws {RangeError} if {@link LogLevels#validateLogLevel} fails.
     */
    setDefaultLogLevel(logLevel) {
        LOGLEVEL.validateLogLevel(logLevel);
        this._logLevel = logLevel;
    }

    /**
     * Get a logger.
     *
     * @param {string} name A name for the logger. Should be a unique name,
     *      so typically the full import path of the class/function using
     *      the logger.
     * @returns {Logger}
     */
    getLogger(name) {
        if(!this._loggerMap.has(name)) {
            this._loggerMap.set(name, new Logger(name, this));
        }
        return this._loggerMap.get(name);
    }
}
