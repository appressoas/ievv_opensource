import AbstractLogger from "./AbstractLogger";
import LOGLEVEL from "./loglevel";


export default class Logger extends AbstractLogger {
    /**
     *
     * @param {string} name The name of the logger.
     * @param {LoggerSingleton} loggerSingleton The logger singleton
     *      this logger belongs to.
     */
    constructor(name, loggerSingleton) {
        super();
        this._name = name;
        this._logLevel = null;
        this._loggerSingleton = loggerSingleton;
    }

    /**
     * Get the name of this logger.
     * @returns {string}
     */
    get name() {
        return this._name;
    }

    /**
     * Set the loglevel for this logger.
     *
     * @param {int} logLevel The log level. Must be one of the loglevels
     *      defined in {@link LogLevels}.
     * @throws {RangeError} if {@link LogLevels#validateLogLevel} fails.
     */
    setLogLevel(logLevel) {
        LOGLEVEL.validateLogLevel(logLevel);
        this._logLevel = logLevel;
    }

    /**
     * Get the log level.
     *
     * If no log level has been set with {@link Logger#setLogLevel},
     * this returns {@link LoggerSingleton#getDefaultLogLevel}.
     *
     * @returns {int}
     */
    getLogLevel() {
        if(this._logLevel != null) {
            return this._logLevel;
        }
        return this._loggerSingleton.getDefaultLogLevel();
    }
}
