import LoggerSingleton from "../../log/LoggerSingleton";
import LOGLEVEL from "../../log/loglevel";
import Logger from "../../log/Logger";


describe('LoggerSingleton', () => {
    beforeEach(() => {
        new LoggerSingleton().reset();
    });

    it('LoggerSingleton() constructor', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(loggerSingleton._logLevel).toBe(LOGLEVEL.WARNING);
        expect(loggerSingleton._loggerMap.size).toBe(0);
    });

    it('LoggerSingleton().getDefaultLogLevel() default', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(loggerSingleton.getDefaultLogLevel()).toBe(LOGLEVEL.WARNING);
    });

    it('LoggerSingleton().setDefaultLogLevel() updates _logLevel', () => {
        let loggerSingleton = new LoggerSingleton();
        loggerSingleton.setDefaultLogLevel(LOGLEVEL.DEBUG);
        expect(loggerSingleton._logLevel).toBe(LOGLEVEL.DEBUG);
    });

    it('LoggerSingleton().setDefaultLogLevel() invalid logLevel', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(() => loggerSingleton.setDefaultLogLevel(10)).toThrowError(RangeError);
    });

    it('LoggerSingleton().setDefaultLogLevel() updates changes getDefaultLogLevel() output', () => {
        let loggerSingleton = new LoggerSingleton();
        loggerSingleton.setDefaultLogLevel(LOGLEVEL.DEBUG);
        expect(loggerSingleton.getDefaultLogLevel()).toBe(LOGLEVEL.DEBUG);
    });

    it('LoggerSingleton().getLogger() return type', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(loggerSingleton.getLogger('test')).toBeInstanceOf(Logger);
    });

    it('LoggerSingleton().getLogger() AbstractLogger configured correctly', () => {
        let loggerSingleton = new LoggerSingleton();
        let logger = loggerSingleton.getLogger('test');
        expect(logger.name).toBe('test');
        expect(logger._logLevel).toBe(null);
        expect(logger._loggerSingleton).toBe(loggerSingleton);
    });

    it('LoggerSingleton().getLogger() updates _loggerMap on first call', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(loggerSingleton._loggerMap.size).toBe(0);
        let logger = loggerSingleton.getLogger('test');
        expect(loggerSingleton._loggerMap.size).toBe(1);
        expect(loggerSingleton._loggerMap.get('test')).toBeInstanceOf(Logger);
        expect(loggerSingleton._loggerMap.get('test')).toBe(logger);
    });

    it('LoggerSingleton().getLogger() get from _loggerMap on subsequent calls', () => {
        let loggerSingleton = new LoggerSingleton();
        expect(loggerSingleton._loggerMap.size).toBe(0);
        let logger = loggerSingleton.getLogger('test');
        loggerSingleton.getLogger('test');
        loggerSingleton.getLogger('test');
        expect(loggerSingleton._loggerMap.size).toBe(1);
        expect(loggerSingleton._loggerMap.get('test')).toBe(logger);
    });
});
