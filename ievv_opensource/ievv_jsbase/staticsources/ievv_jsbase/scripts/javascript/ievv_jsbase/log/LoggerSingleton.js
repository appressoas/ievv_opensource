import AbstractLogger from "./AbstractLogger";

let _instance = null;

/**
 */
export default class LoggerSingleton extends AbstractLogger {
    constructor() {
        if(!_instance) {
            _instance = this;
        }
        this.logLevel = this.LEVEL_ERROR;
        return _instance;
    }

    getLogLevel() {
        return this.logLevel;
    }

    /**
     * Set the loglevel.
     *
     * @param logLevel
     */
    setLogLevel(logLevel) {
        if (logLevel > this.LEVEL_LOG || logLevel < 0) {
            console.error(
                "Cannot set log level to %d, must be between %d (silent) and %d (everything)",
                logLevel, this.LEVEL_SILENT, this.LEVEL_DEBUG);
        } else {
            this.logLevel = logLevel;
        }
    }
}
