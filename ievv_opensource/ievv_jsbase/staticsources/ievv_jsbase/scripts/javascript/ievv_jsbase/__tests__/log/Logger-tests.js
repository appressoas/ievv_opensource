import Logger from "../../log/Logger";
import LOGLEVEL from "../../log/loglevel";


describe('Logger', () => {
    it('Logger() constructor', () => {
        let loggerSingleton = jest.fn();
        let logger = new Logger('test', loggerSingleton);
        expect(logger._name).toBe('test');
        expect(logger._logLevel).toBe(null);
        expect(logger._loggerSingleton).toBe(loggerSingleton);
    });

    it('Logger() name', () => {
        let logger = new Logger('test');
        expect(logger.name).toBe('test');
    });

    it('Logger() getLogLevel - _logLevel is null - uses loggerSingleton.getDefaultLogLevel', () => {
        let loggerSingleton = jest.fn();
        loggerSingleton.getDefaultLogLevel = jest.fn(() => 'mocklevel');
        let logger = new Logger('test', loggerSingleton);
        let logLevel = logger.getLogLevel();
        expect(loggerSingleton.getDefaultLogLevel).toHaveBeenCalledTimes(1);
        expect(logLevel).toBe('mocklevel');
    });

    it('Logger() getLogLevel - _logLevel is NOT null', () => {
        let logger = new Logger('test');
        logger._logLevel = 'mocklevel';
        expect(logger.getLogLevel()).toBe('mocklevel');
    });

    it('Logger() setLogLevel', () => {
        let logger = new Logger('test');
        logger.setLogLevel(LOGLEVEL.DEBUG);
        expect(logger._logLevel).toBe(LOGLEVEL.DEBUG);
    });

    it('Logger() setLogLevel invalid logLevel', () => {
        let logger = new Logger('test');
        expect(() => logger.setLogLevel(10)).toThrowError(RangeError);
    });
});