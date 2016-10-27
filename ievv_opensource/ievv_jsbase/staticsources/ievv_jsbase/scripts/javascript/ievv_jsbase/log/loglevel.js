/**
 * Defines valid log levels.
 *
 * Not used directly, but instead via the LOGLEVEL
 * constant exported as default by this module.
 *
 * @example
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * console.log('The debug loglevel is:', LOGLEVEL.DEBUG);
 * LOGLEVEL.validateLogLevel(10);
 */
export class LogLevels {
    /**
     * Get the number for log level DEBUG.
     * @returns {number}
     */
    get DEBUG() {
        return 4;
    }

    /**
     * Get the number for log level INFO.
     * @returns {number}
     */
    get INFO() {
        return 3;
    }

    /**
     * Get the number for log level WARNING.
     * @returns {number}
     */
    get WARNING() {
        return 2;
    }

    /**
     * Get the number for log level ERROR.
     * @returns {number}
     */
    get ERROR() {
        return 1;
    }

    /**
     * Get the number for log level SILENT.
     * @returns {number}
     */
    get SILENT() {
        return 0;
    }

    /**
     * Validate a log level.
     *
     * Should be used by all functions/methods that set a log level.
     *
     * @param logLevel The loglevel.
     * @throws {RangeError} If ``logLevel`` is not one
     *   of:
     *
     *   - {@link LogLevels#DEBUG}
     *   - {@link LogLevels#INFO}
     *   - {@link LogLevels#WARNING}
     *   - {@link LogLevels#ERROR}
     *   - {@link LogLevels#SILENT}
     */
    validateLogLevel(logLevel) {
        if (logLevel > this.DEBUG || logLevel < this.SILENT) {
            throw new RangeError(
                `Invalid log level: ${logLevel}, must be between ` +
                `${this.SILENT} (SILENT) and ${this.DEBUG} (DEBUG)`);
        }
    }
}

const LOGLEVEL = new LogLevels();
export default LOGLEVEL;
