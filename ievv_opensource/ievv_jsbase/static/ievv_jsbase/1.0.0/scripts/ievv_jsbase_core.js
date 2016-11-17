(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.SentSignalInfo = exports.ReceivedSignalInfo = exports.DuplicateReceiverNameForSignal = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _makeCustomError = require("./makeCustomError");

var _makeCustomError2 = _interopRequireDefault(_makeCustomError);

var _PrettyFormat = require("./utils/PrettyFormat");

var _PrettyFormat2 = _interopRequireDefault(_PrettyFormat);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Exception raised by {@link HttpCookies#getStrict} when the cookie is not found.
 *
 * @type {Error}
 */
var DuplicateReceiverNameForSignal = exports.DuplicateReceiverNameForSignal = (0, _makeCustomError2.default)('DuplicateReceiverNameForSignal');

/**
 * Represents information about the received signal.
 *
 * An object of this class is sent to the ``callback``
 * of all signal receivers.
 *
 * The data sent by the signal is available in
 * {@link ReceivedSignalInfo.data}.
 */

var ReceivedSignalInfo = exports.ReceivedSignalInfo = function () {
    function ReceivedSignalInfo(data, signalName, receiverName) {
        _classCallCheck(this, ReceivedSignalInfo);

        /**
         * The data sent by {@link SignalHandlerSingleton#send}.
         */
        this.data = data;

        /**
         * The signal name.
         *
         * @type {string}
         */
        this.signalName = signalName;

        /**
         * The receiver name.
         *
         * @type {string}
         */
        this.receiverName = receiverName;
    }

    /**
     * Get a string with debug information about the received signal.
     */


    _createClass(ReceivedSignalInfo, [{
        key: "toString",
        value: function toString() {
            var prettyData = new _PrettyFormat2.default(this.data).toString(2);
            return "signalName=\"" + this.signalName + "\", " + ("receiverName=\"" + this.receiverName + "\", ") + ("data=" + prettyData);
        }
    }]);

    return ReceivedSignalInfo;
}();

/**
 * Private class used by {@link _SignalReceivers} to represent
 * a single receiver listening for a single signal.
 */


var _SignalReceiver = function () {
    function _SignalReceiver(signal, name, callback) {
        _classCallCheck(this, _SignalReceiver);

        this.signal = signal;
        this.name = name;
        this.callback = callback;
    }

    /**
     * Asynchronously trigger the receiver callback.
     * @param data The signal data (the data argument provided for
     *    {@link SignalHandlerSingleton#send}.
     */


    _createClass(_SignalReceiver, [{
        key: "trigger",
        value: function trigger(data) {
            var _this = this;

            setTimeout(function () {
                _this.callback(new ReceivedSignalInfo(data, _this.signal.name, _this.name));
            }, 0);
        }
    }]);

    return _SignalReceiver;
}();

/**
 * Object containing debugging information about a sent
 * signal.
 */


var SentSignalInfo = exports.SentSignalInfo = function () {
    function SentSignalInfo(signalName) {
        _classCallCheck(this, SentSignalInfo);

        /**
         * The signal name.
         *
         * @type {string}
         */
        this.signalName = signalName;

        /**
         * Array of triggered receiver names.
         *
         * @type {Array}
         */
        this.triggeredReceiverNames = [];
    }

    _createClass(SentSignalInfo, [{
        key: "_addReceiverName",
        value: function _addReceiverName(receiverName) {
            this.triggeredReceiverNames.push(receiverName);
        }

        /**
         * Get a string representation of the sent signal info.
         *
         * @returns {string}
         */

    }, {
        key: "toString",
        value: function toString() {
            var receivers = this.triggeredReceiverNames.join(', ');
            if (receivers === '') {
                receivers = 'NO RECEIVERS';
            }
            return "Signal: " + this.signalName + " was sent to: " + receivers;
        }
    }]);

    return SentSignalInfo;
}();

/**
 * Private class used by {@link SignalHandlerSingleton}
 * to represent all receivers for a single signal.
 */


var _SignalReceivers = function () {
    function _SignalReceivers(name) {
        _classCallCheck(this, _SignalReceivers);

        this.name = name;
        this.receiverMap = new Map();
    }

    /**
     * Add a receiver.
     *
     * @throw DuplicateReceiverNameForSignal If the receiver is already registered for the signal.
     */


    _createClass(_SignalReceivers, [{
        key: "addReceiver",
        value: function addReceiver(receiverName, callback) {
            if (this.receiverMap.has(receiverName)) {
                throw new DuplicateReceiverNameForSignal("The \"" + receiverName + "\" receiver is already registered for the \"" + this.name + "\" signal");
            }
            this.receiverMap.set(receiverName, new _SignalReceiver(this, receiverName, callback));
        }

        /**
         * Remove a receiver.
         *
         * If the receiver is not registered for the signal,
         * nothing happens.
         */

    }, {
        key: "removeReceiver",
        value: function removeReceiver(receiverName) {
            if (this.receiverMap.has(receiverName)) {
                this.receiverMap.delete(receiverName);
            }
        }

        /**
         * Check if we have a specific receiver for this signal.
         */

    }, {
        key: "hasReceiver",
        value: function hasReceiver(receiverName) {
            return this.receiverMap.has(receiverName);
        }

        /**
         * Get the number of receivers registered for the signal.
         */

    }, {
        key: "receiverCount",
        value: function receiverCount() {
            return this.receiverMap.size;
        }

        /**
         * Send the signal.
         *
         * @param data The data sent with the signal. Forwarded to
         *      the signal receiver callback.
         * @param {SentSignalInfo} info If this is provided, we add the
         *      name of all receivers the signal was sent to.
         */

    }, {
        key: "send",
        value: function send(data, info) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this.receiverMap.values()[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var receiver = _step.value;

                    receiver.trigger(data);
                    if (info) {
                        info._addReceiverName(receiver.name);
                    }
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }
    }]);

    return _SignalReceivers;
}();

/**
 * The instance of the {@link SignalHandlerSingleton}.
 */


var _instance = null;

/**
 * Signal handler singleton for global communication.
 *
 * @example <caption>Basic example</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MyReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received. Data:', receivedSignalInfo.data);
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'});
 *
 *
 * @example <caption>Recommended signal and receiver naming</caption>
 *
 * // In myapp/menu/MenuComponent.js
 * class MenuComponent {
 *     constructor(menuName) {
 *         this.menuName = menuName;
 *         let signalHandler = new SignalHandlerSingleton();
 *         signalHandler.addReceiver(
 *             `toggleMenu#${this.menuName}`,
 *             'myapp.menu.MenuComponent',
 *             (receivedSignalInfo) => {
 *                  this.toggle();
 *             }
 *         );
 *     }
 *     toggle() {
 *         // Toggle the menu
 *     }
 * }
 *
 * // In myotherapp/widgets/MenuToggle.js
 * class MenuToggle {
 *     constructor(menuName) {
 *         this.menuName = menuName;
 *     }
 *     toggle() {
 *         let signalHandler = new SignalHandlerSingleton();
 *         signalHandler.send(`toggleMenu#${this.menuName}`);
 *     }
 * }
 *
 * @example <caption>Multiple receivers</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MyFirstReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received by receiver 1!');
 * });
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MySecondReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received by receiver 1!');
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'});
 *
 *
 * @example <caption>Debugging</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('mysignal', 'MyReceiver', (receivedSignalInfo) => {
 *     console.log('received signal:', receivedSignalInfo.toString());
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'}, (sentSignalInfo) => {
 *     console.log('sent signal info:', sentSignalInfo.toString());
 * });
 *
 */

var SignalHandlerSingleton = function () {
    function SignalHandlerSingleton() {
        _classCallCheck(this, SignalHandlerSingleton);

        if (!_instance) {
            _instance = this;
            this._signalMap = new Map();
        }
        return _instance;
    }

    /**
     * Remove all receivers for all signals.
     *
     * Useful for debugging and tests, but should not be
     * used for production code.
     */


    _createClass(SignalHandlerSingleton, [{
        key: "clearAllReceiversForAllSignals",
        value: function clearAllReceiversForAllSignals() {
            this._signalMap.clear();
        }

        /**
         * Add a receiver for a specific signal.
         *
         * @param {string} signalName The name of the signal.
         *      Typically something like ``toggleMenu`` or ``myapp.toggleMenu``.
         *
         *      What if we have multiple objects listening for this ``toggleMenu``
         *      signal, and we only want to toggle a specific menu? You need
         *      to ensure the signalName is unique for each menu. We recommend
         *      that you do this by adding ``#<context>``. For example
         *      ``toggleMenu#mainmenu``. This is shown in one of the examples
         *      above.
         * @param {string} receiverName The name of the receiver.
         *      Must be unique for the signal.
         *      We recommend that you use a very explicit name for your signals.
         *      It should normally be the full path to the method or function receiving
         *      the signal. So if you have a class named ``myapp/menu/MenuComponent.js``
         *      that receives a signal to toggle the menu, the receiverName should be
         *      ``myapp.menu.MenuComponent``.
         * @param callback The callback to call when the signal is sent.
         *      The callback is called with a single argument - a
         *      {@link ReceivedSignalInfo} object.
         */

    }, {
        key: "addReceiver",
        value: function addReceiver(signalName, receiverName, callback) {
            if (typeof callback === 'undefined') {
                throw new TypeError('The callback argument for addReceiver() is required.');
            }
            if (!this._signalMap.has(signalName)) {
                this._signalMap.set(signalName, new _SignalReceivers(signalName));
            }
            var signal = this._signalMap.get(signalName);
            signal.addReceiver(receiverName, callback);
        }

        /**
         * Remove a receiver for a signal added with {@link SignalHandlerSingleton#addReceiver}.
         *
         * @param {string} signalName The name of the signal.
         * @param {string} receiverName The name of the receiver.
         */

    }, {
        key: "removeReceiver",
        value: function removeReceiver(signalName, receiverName) {
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                signal.removeReceiver(receiverName);
                if (signal.receiverCount() === 0) {
                    this._signalMap.delete(signalName);
                }
            }
        }

        /**
         * Check if a signal has a specific receiver.
         *
         * @param {string} signalName The name of the signal.
         * @param {string} receiverName The name of the receiver.
         */

    }, {
        key: "hasReceiver",
        value: function hasReceiver(signalName, receiverName) {
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                return signal.hasReceiver(receiverName);
            } else {
                return false;
            }
        }

        /**
         * Remove all receivers for a specific signal.
         *
         * @param {string} signalName The name of the signal to remove.
         */

    }, {
        key: "clearAllReceiversForSignal",
        value: function clearAllReceiversForSignal(signalName) {
            if (this._signalMap.has(signalName)) {
                this._signalMap.delete(signalName);
            }
        }

        /**
         * Send a signal.
         *
         * @param {string} signalName The name of the signal to send.
         * @param data Data to send to the callback of all receivers registered
         *      for the signal.
         * @param infoCallback An optional callback that receives information
         *      about the signal. Useful for debugging what actually received
         *      the signal. The ``infoCallback`` is called with a single
         *      argument - a {@link SentSignalInfo} object.
         */

    }, {
        key: "send",
        value: function send(signalName, data, infoCallback) {
            var info = null;
            if (infoCallback) {
                info = new SentSignalInfo(signalName);
            }
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                signal.send(data, info);
            }
            if (infoCallback) {
                infoCallback(info);
            }
        }
    }]);

    return SignalHandlerSingleton;
}();

exports.default = SignalHandlerSingleton;

},{"./makeCustomError":7,"./utils/PrettyFormat":8}],2:[function(require,module,exports){
"use strict";

var _SignalHandlerSingleton = require("./SignalHandlerSingleton");

var _SignalHandlerSingleton2 = _interopRequireDefault(_SignalHandlerSingleton);

var _WidgetRegistrySingleton = require("./widget/WidgetRegistrySingleton");

var _WidgetRegistrySingleton2 = _interopRequireDefault(_WidgetRegistrySingleton);

var _LoggerSingleton = require("./log/LoggerSingleton");

var _LoggerSingleton2 = _interopRequireDefault(_LoggerSingleton);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

window.ievv_jsbase_core = {
    SignalHandlerSingleton: _SignalHandlerSingleton2.default,
    WidgetRegistrySingleton: _WidgetRegistrySingleton2.default,
    LoggerSingleton: _LoggerSingleton2.default
};

},{"./SignalHandlerSingleton":1,"./log/LoggerSingleton":5,"./widget/WidgetRegistrySingleton":10}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 */
var AbstractLogger = function () {
    function AbstractLogger() {
        _classCallCheck(this, AbstractLogger);
    }

    _createClass(AbstractLogger, [{
        key: "getLogLevel",
        value: function getLogLevel() {
            throw new Error('Must be overridden in subclasses.');
        }
    }, {
        key: "_noOutput",
        value: function _noOutput() {}

        /**
         * Exposes console.log. Will only print if current level is
         * higher than {@link LogLevels#DEBUG}.
         * @returns {Function} console.log
         */

    }, {
        key: "debug",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.DEBUG) {
                return console.log.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.log. Will only print if current level is
         * higher than {@link LogLevels#INFO}.
         * @returns {Function} console.log
         */

    }, {
        key: "info",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.INFO) {
                return console.log.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.warn. Will only print if current level is
         * higher than {@link LogLevels#WARNING}.
         * @returns {Function} console.warn
         */

    }, {
        key: "warning",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.WARNING) {
                return console.warn.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.error. Will only print if current level is
         * higher than {@link LogLevels#ERROR}.
         * @returns {Function} console.error
         */

    }, {
        key: "error",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.ERROR) {
                return console.error.bind(console);
            }
            return this._noOutput;
        }
    }]);

    return AbstractLogger;
}();

exports.default = AbstractLogger;

},{"./loglevel":6}],4:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _AbstractLogger2 = require("./AbstractLogger");

var _AbstractLogger3 = _interopRequireDefault(_AbstractLogger2);

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Logger = function (_AbstractLogger) {
    _inherits(Logger, _AbstractLogger);

    /**
     *
     * @param {string} name The name of the logger.
     * @param {LoggerSingleton} loggerSingleton The logger singleton
     *      this logger belongs to.
     */
    function Logger(name, loggerSingleton) {
        _classCallCheck(this, Logger);

        var _this = _possibleConstructorReturn(this, (Logger.__proto__ || Object.getPrototypeOf(Logger)).call(this));

        _this._name = name;
        _this._logLevel = null;
        _this._loggerSingleton = loggerSingleton;
        return _this;
    }

    /**
     * Get the name of this logger.
     * @returns {string}
     */


    _createClass(Logger, [{
        key: "setLogLevel",


        /**
         * Set the loglevel for this logger.
         *
         * @param {int} logLevel The log level. Must be one of the loglevels
         *      defined in {@link LogLevels}.
         * @throws {RangeError} if {@link LogLevels#validateLogLevel} fails.
         */
        value: function setLogLevel(logLevel) {
            _loglevel2.default.validateLogLevel(logLevel);
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

    }, {
        key: "getLogLevel",
        value: function getLogLevel() {
            if (this._logLevel == null) {
                return this._loggerSingleton.getDefaultLogLevel();
            }
            return this._logLevel;
        }

        /**
         * Get textual name for the log level. If the logger
         * does not have a logLevel (if it inherits it from the LoggerSingleton)
         * a string with information about this and the default logLevel for the
         * LoggerSingleton is returned.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getTextualNameForLogLevel",
        value: function getTextualNameForLogLevel() {
            if (this._logLevel == null) {
                return '[default for LoggerSingleton - ' + (this._loggerSingleton.getTextualNameForDefaultLogLevel() + "]");
            }
            return _loglevel2.default.getTextualNameForLogLevel(this.getLogLevel());
        }
    }, {
        key: "getDebugInfoString",
        value: function getDebugInfoString() {
            return this.name + ": " + this.getTextualNameForLogLevel();
        }
    }, {
        key: "name",
        get: function get() {
            return this._name;
        }
    }]);

    return Logger;
}(_AbstractLogger3.default);

exports.default = Logger;

},{"./AbstractLogger":3,"./loglevel":6}],5:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _Logger = require("./Logger");

var _Logger2 = _interopRequireDefault(_Logger);

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var _instance = null;

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

var LoggerSingleton = function () {
    /**
     * Get an instance of the singleton.
     *
     * The first time this is called, we create a new instance.
     * For all subsequent calls, we return the instance that was
     * created on the first call.
     */
    function LoggerSingleton() {
        _classCallCheck(this, LoggerSingleton);

        if (!_instance) {
            _instance = this;
        }
        this._loggerMap = new Map();
        this.reset();
        return _instance;
    }

    /**
     * Get the number of loggers registered using
     * {@link getLogger}.
     *
     * @returns {number} The number of loggers.
     */


    _createClass(LoggerSingleton, [{
        key: "getLoggerCount",
        value: function getLoggerCount() {
            return this._loggerMap.size;
        }

        /**
         * Reset to default log level, and clear all
         * custom loggers.
         */

    }, {
        key: "reset",
        value: function reset() {
            this._logLevel = _loglevel2.default.WARNING;
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

    }, {
        key: "getDefaultLogLevel",
        value: function getDefaultLogLevel() {
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

    }, {
        key: "setDefaultLogLevel",
        value: function setDefaultLogLevel(logLevel) {
            _loglevel2.default.validateLogLevel(logLevel);
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

    }, {
        key: "getLogger",
        value: function getLogger(name) {
            if (!this._loggerMap.has(name)) {
                this._loggerMap.set(name, new _Logger2.default(name, this));
            }
            return this._loggerMap.get(name);
        }

        /**
         * Get the names of all the registered loggers.
         *
         * @returns {Array} Sorted array with the same of the loggers.
         */

    }, {
        key: "getLoggerNameArray",
        value: function getLoggerNameArray() {
            var loggerNames = Array.from(this._loggerMap.keys());
            loggerNames.sort();
            return loggerNames;
        }

        /**
         * Get textual name for the default log level.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getTextualNameForDefaultLogLevel",
        value: function getTextualNameForDefaultLogLevel() {
            return _loglevel2.default.getTextualNameForLogLevel(this.getDefaultLogLevel());
        }

        /**
         * Get a string that summarize information about all the
         * loggers. The string has a list of loglevels with
         * their loglevel. Perfect for debugging.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getDebugInfoString",
        value: function getDebugInfoString() {
            var loggerInfoString = "Default logLevel: " + (this.getTextualNameForDefaultLogLevel() + "\n") + "Loggers:\n";
            if (this.getLoggerCount() === 0) {
                loggerInfoString += '(no loggers)\n';
            } else {
                var _iteratorNormalCompletion = true;
                var _didIteratorError = false;
                var _iteratorError = undefined;

                try {
                    for (var _iterator = this.getLoggerNameArray()[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                        var loggerName = _step.value;

                        var logger = this.getLogger(loggerName);
                        loggerInfoString += " - " + logger.getDebugInfoString() + "\n";
                    }
                } catch (err) {
                    _didIteratorError = true;
                    _iteratorError = err;
                } finally {
                    try {
                        if (!_iteratorNormalCompletion && _iterator.return) {
                            _iterator.return();
                        }
                    } finally {
                        if (_didIteratorError) {
                            throw _iteratorError;
                        }
                    }
                }
            }
            return loggerInfoString;
        }
    }]);

    return LoggerSingleton;
}();

exports.default = LoggerSingleton;

},{"./Logger":4,"./loglevel":6}],6:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

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
var LogLevels = exports.LogLevels = function () {
    function LogLevels() {
        _classCallCheck(this, LogLevels);

        this._prettyLogLevelNames = {};
        this._prettyLogLevelNames[this.DEBUG] = 'DEBUG';
        this._prettyLogLevelNames[this.INFO] = 'INFO';
        this._prettyLogLevelNames[this.WARNING] = 'WARNING';
        this._prettyLogLevelNames[this.ERROR] = 'ERROR';
        this._prettyLogLevelNames[this.SILENT] = 'SILENT';
    }

    /**
     * Get the number for log level DEBUG.
     * @returns {number}
     */


    _createClass(LogLevels, [{
        key: 'validateLogLevel',


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
        value: function validateLogLevel(logLevel) {
            if (logLevel > this.DEBUG || logLevel < this.SILENT) {
                throw new RangeError('Invalid log level: ' + logLevel + ', must be between ' + (this.SILENT + ' (SILENT) and ' + this.DEBUG + ' (DEBUG)'));
            }
        }

        /**
         * Get the textual name for a log level.
         *
         * @param {number} logLevel The log level to get a textual name for.
         * @returns {string}
         *
         * @example
         * const infoText = LOGLEVEL.getTextualNameForLogLevel(LOGLEVEL.INFO);
         * // infoText === 'INFO'
         */

    }, {
        key: 'getTextualNameForLogLevel',
        value: function getTextualNameForLogLevel(logLevel) {
            return this._prettyLogLevelNames[logLevel];
        }
    }, {
        key: 'DEBUG',
        get: function get() {
            return 4;
        }

        /**
         * Get the number for log level INFO.
         * @returns {number}
         */

    }, {
        key: 'INFO',
        get: function get() {
            return 3;
        }

        /**
         * Get the number for log level WARNING.
         * @returns {number}
         */

    }, {
        key: 'WARNING',
        get: function get() {
            return 2;
        }

        /**
         * Get the number for log level ERROR.
         * @returns {number}
         */

    }, {
        key: 'ERROR',
        get: function get() {
            return 1;
        }

        /**
         * Get the number for log level SILENT.
         * @returns {number}
         */

    }, {
        key: 'SILENT',
        get: function get() {
            return 0;
        }
    }]);

    return LogLevels;
}();

var LOGLEVEL = new LogLevels();
exports.default = LOGLEVEL;

},{}],7:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.default = makeCustomError;
/**
 * Make a custom error "class".
 *
 * Makes an old style prototype based error class.
 *
 * @example <caption>Typical usage</caption>
 * // In myerrors.js
 * export let MyCustomError = makeCustomError('MyCustomError');
 *
 * // Using the error
 * import {MyCustomError} from './myerrors';
 * throw new MyCustomError('The message');
 *
 * @example <caption>Throwing the error - complete example</caption>
 * try {
 *     throw new MyCustomError('The message', {
 *          code: 'stuff_happened',
 *          details: {
 *              size: 10
 *          }
 *     });
 * } catch(e) {
 *     if(e instanceof MyCustomError) {
 *         console.error(`${e.toString()} -- Code: ${e.code}. Size: ${e.details.size}`);
 *     }
 * }
 *
 * @example <caption>Define an error that extends Error</caption>
 * let NotFoundError = makeCustomError('NotFoundError');
 * // error instanceof NotFoundError === true
 * // error instanceof Error === true
 *
 * @example <caption>Define an error that extends a built in error</caption>
 * let MyValueError = makeCustomError('MyValueError', TypeError);
 * let error = new MyValueError();
 * // error instanceof MyValueError === true
 * // error instanceof TypeError === true
 * // error instanceof Error === true
 *
 * @example <caption>Define an error that extends another custom error</caption>
 * let MySuperError = makeCustomError('MySuperError', TypeError);
 * let MySubError = makeCustomError('MySubError', MySuperError);
 * let error = new MySubError();
 * // error instanceof MySubError === true
 * // error instanceof MySuperError === true
 * // error instanceof TypeError === true
 * // error instanceof Error === true
 *
 * @param {string} name The name of the error class.
 * @param {Error} extendsError An optional Error to extend.
 *      Defaults to {@link Error}. Can be a built in error
 *      or a custom error created by this function.
 * @returns {Error} The created error class.
 */
function makeCustomError(name, extendsError) {
    extendsError = extendsError || Error;
    var CustomError = function CustomError(message, properties) {
        this.message = message;
        var last_part = new extendsError().stack.match(/[^\s]+$/);
        this.stack = this.name + " at " + last_part;
        if (typeof properties !== 'undefined') {
            Object.assign(this, properties);
        }
    };
    Object.setPrototypeOf(CustomError, extendsError);
    CustomError.prototype = Object.create(extendsError.prototype);
    CustomError.prototype.constructor = CustomError;
    CustomError.prototype.message = "";
    CustomError.prototype.name = name;
    return CustomError;
}

},{}],8:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _typeDetect = require('./typeDetect');

var _typeDetect2 = _interopRequireDefault(_typeDetect);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Pretty format any javascript object.
 *
 * Handles the following types:
 *
 * - null
 * - undefined
 * - Number
 * - Boolean
 * - String
 * - Array
 * - Map
 * - Set
 * - Function
 * - Class (detected as a Function, so pretty formatted just like a function)
 * - Object
 *
 * @example <caption>Without indentation</caption>
 * new PrettyFormat([1, 2]).toString();
 *
 * @example <caption>With indentation (indent by 2 spaces)</caption>
 * new PrettyFormat([1, 2]).toString(2);
 *
 * @example <caption>Simple examples</caption>
 * new PrettyFormat(true).toString() === 'true';
 * new PrettyFormat(null).toString() === 'null';
 * new PrettyFormat([1, 2]).toString() === '[1, 2]';
 * new PrettyFormat({name: "John", age: 29}).toString() === '{"age": 29, "name": John}';
 *
 * @example <caption>Complex example</caption>
 * let map = new Map();
 * map.set('a', [10, 20]);
 * map.set('b', [30, 40, 50]);
 * function testFunction() {}
 * let obj = {
 *     theMap: map,
 *     aSet: new Set(['one', 'two']),
 *     theFunction: testFunction
 * };
 * const prettyFormatted = new PrettyFormat(obj).toString(2);
 */
var PrettyFormat = function () {
    function PrettyFormat(obj) {
        _classCallCheck(this, PrettyFormat);

        this._obj = obj;
    }

    _createClass(PrettyFormat, [{
        key: '_indentString',
        value: function _indentString(str, indent, indentLevel) {
            if (indent === 0) {
                return str;
            }
            return '' + ' '.repeat(indent * indentLevel) + str;
        }
    }, {
        key: '_objectToMap',
        value: function _objectToMap(obj) {
            var map = new Map();
            var sortedKeys = Array.from(Object.keys(obj));
            sortedKeys.sort();
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = sortedKeys[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var key = _step.value;

                    map.set(key, obj[key]);
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }

            return map;
        }
    }, {
        key: '_prettyFormatFlatIterable',
        value: function _prettyFormatFlatIterable(flatIterable, size, indent, indentLevel, prefix, suffix) {
            var output = prefix;
            var itemSuffix = ', ';
            if (indent) {
                output = prefix + '\n';
                itemSuffix = ',';
            }
            var index = 1;
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = flatIterable[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var item = _step2.value;

                    var prettyItem = this._prettyFormat(item, indent, indentLevel + 1);
                    if (index !== size) {
                        prettyItem += itemSuffix;
                    }
                    output += this._indentString(prettyItem, indent, indentLevel + 1);
                    if (indent) {
                        output += '\n';
                    }
                    index++;
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }

            output += this._indentString('' + suffix, indent, indentLevel);
            return output;
        }
    }, {
        key: '_prettyFormatMap',
        value: function _prettyFormatMap(map, indent, indentLevel, prefix, suffix, keyValueSeparator) {
            var output = prefix;
            var itemSuffix = ', ';
            if (indent) {
                output = prefix + '\n';
                itemSuffix = ',';
            }
            var index = 1;
            var _iteratorNormalCompletion3 = true;
            var _didIteratorError3 = false;
            var _iteratorError3 = undefined;

            try {
                for (var _iterator3 = map[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                    var _step3$value = _slicedToArray(_step3.value, 2);

                    var key = _step3$value[0];
                    var value = _step3$value[1];

                    var prettyKey = this._prettyFormat(key, indent, indentLevel + 1);
                    var prettyValue = this._prettyFormat(value, indent, indentLevel + 1);
                    var prettyItem = '' + prettyKey + keyValueSeparator + prettyValue;
                    if (index !== map.size) {
                        prettyItem += itemSuffix;
                    }
                    output += this._indentString(prettyItem, indent, indentLevel + 1);
                    if (indent) {
                        output += '\n';
                    }
                    index++;
                }
            } catch (err) {
                _didIteratorError3 = true;
                _iteratorError3 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion3 && _iterator3.return) {
                        _iterator3.return();
                    }
                } finally {
                    if (_didIteratorError3) {
                        throw _iteratorError3;
                    }
                }
            }

            output += this._indentString('' + suffix, indent, indentLevel);
            return output;
        }
    }, {
        key: '_prettyFormatFunction',
        value: function _prettyFormatFunction(fn) {
            return '[Function: ' + fn.name + ']';
        }
    }, {
        key: '_prettyFormat',
        value: function _prettyFormat(obj, indent, indentLevel) {
            var typeString = (0, _typeDetect2.default)(obj);
            var output = '';
            if (typeString === 'string') {
                output = '"' + obj + '"';
            } else if (typeString === 'number' || typeString === 'boolean' || typeString === 'undefined' || typeString === 'null') {
                output = '' + obj;
            } else if (typeString === 'array') {
                output = this._prettyFormatFlatIterable(obj, obj.length, indent, indentLevel, '[', ']');
            } else if (typeString === 'set') {
                output = this._prettyFormatFlatIterable(obj, obj.size, indent, indentLevel, 'Set(', ')');
            } else if (typeString === 'map') {
                output = this._prettyFormatMap(obj, indent, indentLevel, 'Map(', ')', ' => ');
            } else if (typeString === 'function') {
                output = this._prettyFormatFunction(obj);
            } else {
                output = this._prettyFormatMap(this._objectToMap(obj), indent, indentLevel, '{', '}', ': ');
            }
            return output;
        }

        /**
         * Get the results as a string, optionally indented.
         *
         * @param {number} indent The number of spaces to indent by. Only
         *    child objects are indented, and they are indented recursively.
         * @returns {string}
         */

    }, {
        key: 'toString',
        value: function toString(indent) {
            indent = indent || 0;
            return this._prettyFormat(this._obj, indent, 0);
        }
    }]);

    return PrettyFormat;
}();

exports.default = PrettyFormat;

},{"./typeDetect":9}],9:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

exports.default = typeDetect;
/**
 * Detect the type of an object and return the
 * result as a string.
 *
 * Handles the following types:
 *
 * - null  (returned as ``"null"``).
 * - undefined  (returned as ``"undefined"``).
 * - Number  (returned as ``"number"``).
 * - Boolean  (returned as ``"boolean"``).
 * - String  (returned as ``"string"``).
 * - Array  (returned as ``"array"``).
 * - Map  (returned as ``"map"``).
 * - Set  (returned as ``"set"``).
 * - Function  (returned as ``"function"``).
 * - Object  (returned as ``"object"``).
 *
 * We do not handle classes - they are returned as ``"function"``.
 * We could handle classes, but for Babel classes that will require
 * a fairly expensive and error prone regex.
 *
 * @param obj An object to detect the type for.
 * @returns {string}
 */
function typeDetect(obj) {
    if (obj === null) {
        return 'null';
    }
    var typeOf = typeof obj === 'undefined' ? 'undefined' : _typeof(obj);
    if (typeOf === 'undefined') {
        return 'undefined';
    }
    if (typeOf === 'number') {
        return 'number';
    }
    if (typeOf === 'boolean') {
        return 'boolean';
    }
    if (typeOf === 'string') {
        return 'string';
    }
    if (typeOf === 'function') {
        return 'function';
    }
    if (Array.isArray(obj)) {
        return 'array';
    }
    if (obj instanceof Map) {
        return 'map';
    }
    if (obj instanceof Set) {
        return 'set';
    }
    return 'object';
}

},{}],10:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.ElementIsNotInitializedAsWidget = exports.InvalidWidgetAliasError = exports.ElementIsNotWidgetError = exports.ElementHasNoWidgetInstanceIdError = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _makeCustomError = require('../makeCustomError');

var _makeCustomError2 = _interopRequireDefault(_makeCustomError);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The instance of the {@link WidgetRegistrySingleton}.
 */
var _instance = null;

/**
 * Exception thrown when an element where we expect the
 * ``data-ievv-jsbase-widget-instanceid`` attribute does
 * not have this attribute.
 *
 * @type {Error}
 */
var ElementHasNoWidgetInstanceIdError = exports.ElementHasNoWidgetInstanceIdError = (0, _makeCustomError2.default)('ElementHasNoWidgetInstanceIdError');

/**
 * Exception thrown when an element that we expect to have
 * the ``data-ievv-jsbase-widget`` attribute does not have
 * this attribute.
 *
 * @type {Error}
 */
var ElementIsNotWidgetError = exports.ElementIsNotWidgetError = (0, _makeCustomError2.default)('ElementIsNotWidgetError');

/**
 * Exception thrown when an element has a
 * ``data-ievv-jsbase-widget`` with a value that
 * is not an alias registered in the {@link WidgetRegistrySingleton}.
 *
 * @type {Error}
 */
var InvalidWidgetAliasError = exports.InvalidWidgetAliasError = (0, _makeCustomError2.default)('InvalidWidgetAliasError');

/**
 * Exception thrown when an element with the
 * ``data-ievv-jsbase-widget-instanceid=<widgetInstanceId>`` attribute is not in
 * the {@link WidgetRegistrySingleton} with ``<widgetInstanceId>``.
 *
 * @type {Error}
 */
var ElementIsNotInitializedAsWidget = exports.ElementIsNotInitializedAsWidget = (0, _makeCustomError2.default)('ElementIsNotInitializedAsWidget');

/**
 * A very lightweight widget system.
 *
 * Basic example below - see {@link AbstractWidget} for more examples.
 *
 * @example <caption>Create a very simple widget</caption>
 * export default class OpenMenuWidget extends AbstractWidget {
 *     constructor(element) {
 *          super(element);
 *          this._onClickBound = (...args) => {
 *              this._onClick(...args);
 *          };
 *          this.element.addEventListener('click', this._onClickBound);
 *     }
 *
 *     _onClick = (e) => {
 *          e.preventDefault();
 *          console.log('I should have opened the menu here');
 *     }
 *
 *     destroy() {
 *          this.element.removeEventListener('click', this._onClickBound);
 *     }
 * }
 *
 * @example <caption>Use the widget</caption>
 * <button data-ievv-jsbase-widget="open-menu-button" type="button">
 *     Open menu
 * </button>
 *
 * @example <caption>Register and load widgets</caption>
 * // Somewhere that is called after all the widgets are rendered
 * // - typically at the end of the <body>
 * import WidgetRegistrySingleton from 'ievv_jsbase/widget/WidgetRegistrySingleton';
 * import OpenMenuWidget from 'path/to/OpenMenuWidget';
 * const widgetRegistry = new WidgetRegistrySingleton();
 * widgetRegistry.registerWidgetClass('open-menu-button', OpenMenuWidget);
 * widgetRegistry.initializeAllWidgetsWithinElement(document.body);
 *
 */

var WidgetRegistrySingleton = function () {
    function WidgetRegistrySingleton() {
        _classCallCheck(this, WidgetRegistrySingleton);

        if (!_instance) {
            _instance = this;
            this._initialize();
        }
        return _instance;
    }

    _createClass(WidgetRegistrySingleton, [{
        key: '_initialize',
        value: function _initialize() {
            this._widgetAttribute = 'data-ievv-jsbase-widget';
            this._widgetInstanceIdAttribute = 'data-ievv-jsbase-widget-instanceid';
            this._widgetClassMap = new Map();
            this._widgetInstanceMap = new Map();
            this._widgetInstanceCounter = 0;
        }
    }, {
        key: 'clear',
        value: function clear() {
            // TODO: Call destroyAllWidgetsWithinDocumentBody()
            this._widgetClassMap.clear();
            this._widgetInstanceMap.clear();
            this._widgetInstanceCounter = 0;
        }

        /**
         * Register a widget class in the registry.
         *
         * @param {string} alias The alias for the widget. This is the string that
         *      is used as the attribute value with the ``data-ievv-jsbase-widget``
         *      DOM element attribute.
         * @param {AbstractWidget} WidgetClass The widget class.
         */

    }, {
        key: 'registerWidgetClass',
        value: function registerWidgetClass(alias, WidgetClass) {
            this._widgetClassMap.set(alias, WidgetClass);
        }

        /**
         * Remove widget class from registry.
         *
         * @param alias The alias that the widget class was registered with
         *      by using {@link WidgetRegistrySingleton#registerWidgetClass}.
         */

    }, {
        key: 'removeWidgetClass',
        value: function removeWidgetClass(alias) {
            this._widgetClassMap.delete(alias);
        }

        /**
         * Initialize the provided element as a widget.
         *
         * @param {Element} element The DOM element to initalize as a widget.
         *
         * @throws {ElementIsNotWidgetError} If the element does not have
         *      the ``data-ievv-jsbase-widget`` attribute.
         * @throws {InvalidWidgetAliasError} If the widget alias is not in this registry.
         */

    }, {
        key: 'initializeWidget',
        value: function initializeWidget(element) {
            var alias = element.getAttribute(this._widgetAttribute);
            if (!alias) {
                throw new ElementIsNotWidgetError('The\n\n' + element.outerHTML + '\n\nelement has no or empty' + (this._widgetAttribute + ' attribute.'));
            }
            if (!this._widgetClassMap.has(alias)) {
                throw new InvalidWidgetAliasError('No WidgetClass registered with the "' + alias + '" alias.');
            }
            var WidgetClass = this._widgetClassMap.get(alias);
            var widget = new WidgetClass(element);
            this._widgetInstanceCounter++;
            var widgetInstanceId = this._widgetInstanceCounter.toString();
            this._widgetInstanceMap.set(widgetInstanceId, widget);
            element.setAttribute(this._widgetInstanceIdAttribute, widgetInstanceId);
            return widget;
        }
    }, {
        key: '_getAllWidgetElementsWithinElement',
        value: function _getAllWidgetElementsWithinElement(element) {
            return Array.from(element.querySelectorAll('[' + this._widgetAttribute + ']'));
        }

        /**
         * Initialize all widgets within the provided element.
         *
         * @param {Element} element A DOM element.
         */

    }, {
        key: 'initializeAllWidgetsWithinElement',
        value: function initializeAllWidgetsWithinElement(element) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this._getAllWidgetElementsWithinElement(element)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var widgetElement = _step.value;

                    this.initializeWidget(widgetElement);
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }

        /**
         * Get the value of the ``data-ievv-jsbase-widget-instanceid`` attribute
         * of the provided element.
         *
         * @param {Element} element A DOM element.
         * @returns {null|string}
         */

    }, {
        key: 'getWidgetInstanceIdFromElement',
        value: function getWidgetInstanceIdFromElement(element) {
            return element.getAttribute(this._widgetInstanceIdAttribute);
        }

        /**
         * Get a widget instance by its widget instance id.
         *
         * @param widgetInstanceId A widget instance id.
         * @returns {AbstractWidget} A widget instance or ``null``.
         */

    }, {
        key: 'getWidgetInstanceByInstanceId',
        value: function getWidgetInstanceByInstanceId(widgetInstanceId) {
            return this._widgetInstanceMap.get(widgetInstanceId);
        }

        /**
         * Destroy the widget on the provided element.
         *
         * @param {Element} element A DOM element that has been initialized by
         *      {@link WidgetRegistrySingleton#initializeWidget}.
         *
         * @throws {ElementHasNoWidgetInstanceIdError} If the element has
         *      no ``data-ievv-jsbase-widget-instanceid`` attribute or the
         *      attribute value is empty. This normally means that
         *      the element is not a widget, or that the widget
         *      is not initialized.
         * @throws {ElementIsNotInitializedAsWidget} If the element
         *      has the ``data-ievv-jsbase-widget-instanceid`` attribute
         *      but the value of the attribute is not a valid widget instance
         *      id. This should not happen unless you manipulate the
         *      attribute manually or use the private members of this registry.
         */

    }, {
        key: 'destroyWidget',
        value: function destroyWidget(element) {
            var widgetInstanceId = this.getWidgetInstanceIdFromElement(element);
            if (widgetInstanceId) {
                var widgetInstance = this.getWidgetInstanceByInstanceId(widgetInstanceId);
                if (widgetInstance) {
                    widgetInstance.destroy();
                    this._widgetInstanceMap.delete(widgetInstanceId);
                    element.removeAttribute(this._widgetInstanceIdAttribute);
                } else {
                    throw new ElementIsNotInitializedAsWidget('Element\n\n' + element.outerHTML + '\n\nhas the ' + (this._widgetInstanceIdAttribute + ' attribute, but the id is ') + 'not in the widget registry.');
                }
            } else {
                throw new ElementHasNoWidgetInstanceIdError('Element\n\n' + element.outerHTML + '\n\nhas no or empty ' + (this._widgetInstanceIdAttribute + ' attribute.'));
            }
        }
    }, {
        key: '_getAllInstanciatedWidgetElementsWithinElement',
        value: function _getAllInstanciatedWidgetElementsWithinElement(element) {
            return Array.from(element.querySelectorAll('[' + this._widgetInstanceIdAttribute + ']'));
        }

        /**
         * Destroy all widgets within the provided element.
         * Only destroys widgets on elements that is a child of the element.
         *
         * @param {Element} element The DOM Element.
         */

    }, {
        key: 'destroyAllWidgetsWithinElement',
        value: function destroyAllWidgetsWithinElement(element) {
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = this._getAllInstanciatedWidgetElementsWithinElement(element)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var widgetElement = _step2.value;

                    this.destroyWidget(widgetElement);
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }
        }
    }]);

    return WidgetRegistrySingleton;
}();

exports.default = WidgetRegistrySingleton;

},{"../makeCustomError":7}]},{},[2])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvU2lnbmFsSGFuZGxlclNpbmdsZXRvbi5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS9pZXZ2X2pzYmFzZV9jb3JlLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL2xvZy9BYnN0cmFjdExvZ2dlci5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS9sb2cvTG9nZ2VyLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL2xvZy9Mb2dnZXJTaW5nbGV0b24uanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvbG9nL2xvZ2xldmVsLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL21ha2VDdXN0b21FcnJvci5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS91dGlscy9QcmV0dHlGb3JtYXQuanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvdXRpbHMvdHlwZURldGVjdC5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS93aWRnZXQvV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24uanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7Ozs7Ozs7Ozs7QUNBQTs7OztBQUNBOzs7Ozs7OztBQUVBOzs7OztBQUtPLElBQUksMEVBQWlDLCtCQUFnQixnQ0FBaEIsQ0FBckM7O0FBR1A7Ozs7Ozs7Ozs7SUFTYSxrQixXQUFBLGtCO0FBQ1QsZ0NBQVksSUFBWixFQUFrQixVQUFsQixFQUE4QixZQUE5QixFQUE0QztBQUFBOztBQUN4Qzs7O0FBR0EsYUFBSyxJQUFMLEdBQVksSUFBWjs7QUFFQTs7Ozs7QUFLQSxhQUFLLFVBQUwsR0FBa0IsVUFBbEI7O0FBRUE7Ozs7O0FBS0EsYUFBSyxZQUFMLEdBQW9CLFlB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QjtBQUNBLGdCQUFHLGdCQUFILEVBQXFCO0FBQ2pCLG9CQUFJLGlCQUFpQixLQUFLLDZCQUFMLENBQW1DLGdCQUFuQyxDQUFyQjtBQUNBLG9CQUFHLGNBQUgsRUFBbUI7QUFDZixtQ0FBZSxPQUFmO0FBQ0EseUJBQUssa0JBQUwsQ0FBd0IsTUFBeEIsQ0FBK0IsZ0JBQS9CO0FBQ0EsNEJBQVEsZUFBUixDQUF3QixLQUFLLDBCQUE3QjtBQUNILGlCQUpELE1BSU87QUFDSCwwQkFBTSxJQUFJLCtCQUFKLENBQ0YsZ0JBQWMsUUFBUSxTQUF0QixxQkFDRyxLQUFLLDBCQURSLGdFQURFLENBQU47QUFJQztBQUNSLGFBWkQsTUFZTztBQUNILHNCQUFNLElBQUksaUNBQUosQ0FDRixnQkFBYyxRQUFRLFNBQXRCLDZCQUNHLEtBQUssMEJBRFIsaUJBREUsQ0FBTjtBQUdIO0FBQ0o7Ozt1RUFFOEMsTyxFQUFTO0FBQ3BELG1CQUFPLE1BQU0sSUFBTixDQUFXLFFBQVEsZ0JBQVIsT0FBNkIsS0FBSywwQkFBbEMsT0FBWCxDQUFQO0FBQ0g7O0FBRUQ7Ozs7Ozs7Ozt1REFNK0IsTyxFQUFTO0FBQUE7QUFBQTtBQUFBOztBQUFBO0FBQ3BDLHNDQUF5QixLQUFLLDhDQUFMLENBQW9ELE9BQXBELENBQXpCLG1JQUF1RjtBQUFBLHdCQUEvRSxhQUErRTs7QUFDbkYseUJBQUssYUFBTCxDQUFtQixhQUFuQjtBQUNIO0FBSG1DO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFJdkM7Ozs7OztrQkFsS2dCLHVCIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gZSh0LG4scil7ZnVuY3Rpb24gcyhvLHUpe2lmKCFuW29dKXtpZighdFtvXSl7dmFyIGE9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtpZighdSYmYSlyZXR1cm4gYShvLCEwKTtpZihpKXJldHVybiBpKG8sITApO3ZhciBmPW5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIrbytcIidcIik7dGhyb3cgZi5jb2RlPVwiTU9EVUxFX05PVF9GT1VORFwiLGZ9dmFyIGw9bltvXT17ZXhwb3J0czp7fX07dFtvXVswXS5jYWxsKGwuZXhwb3J0cyxmdW5jdGlvbihlKXt2YXIgbj10W29dWzFdW2VdO3JldHVybiBzKG4/bjplKX0sbCxsLmV4cG9ydHMsZSx0LG4scil9cmV0dXJuIG5bb10uZXhwb3J0c312YXIgaT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2Zvcih2YXIgbz0wO288ci5sZW5ndGg7bysrKXMocltvXSk7cmV0dXJuIHN9KSIsImltcG9ydCBtYWtlQ3VzdG9tRXJyb3IgZnJvbSBcIi4vbWFrZUN1c3RvbUVycm9yXCI7XG5pbXBvcnQgUHJldHR5Rm9ybWF0IGZyb20gXCIuL3V0aWxzL1ByZXR0eUZvcm1hdFwiO1xuXG4vKipcbiAqIEV4Y2VwdGlvbiByYWlzZWQgYnkge0BsaW5rIEh0dHBDb29raWVzI2dldFN0cmljdH0gd2hlbiB0aGUgY29va2llIGlzIG5vdCBmb3VuZC5cbiAqXG4gKiBAdHlwZSB7RXJyb3J9XG4gKi9cbmV4cG9ydCBsZXQgRHVwbGljYXRlUmVjZWl2ZXJOYW1lRm9yU2lnbmFsID0gbWFrZUN1c3RvbUVycm9yKCdEdXBsaWNhdGVSZWNlaXZlck5hbWVGb3JTaWduYWwnKTtcblxuXG4vKipcbiAqIFJlcHJlc2VudHMgaW5mb3JtYXRpb24gYWJvdXQgdGhlIHJlY2VpdmVkIHNpZ25hbC5cbiAqXG4gKiBBbiBvYmplY3Qgb2YgdGhpcyBjbGFzcyBpcyBzZW50IHRvIHRoZSBgYGNhbGxiYWNrYGBcbiAqIG9mIGFsbCBzaWduYWwgcmVjZWl2ZXJzLlxuICpcbiAqIFRoZSBkYXRhIHNlbnQgYnkgdGhlIHNpZ25hbCBpcyBhdmFpbGFibGUgaW5cbiAqIHtAbGluayBSZWNlaXZlZFNpZ25hbEluZm8uZGF0YX0uXG4gKi9cbmV4cG9ydCBjbGFzcyBSZWNlaXZlZFNpZ25hbEluZm8ge1xuICAgIGNvbnN0cnVjdG9yKGRhdGEsIHNpZ25hbE5hbWUsIHJlY2VpdmVyTmFtZSkge1xuICAgICAgICAvKipcbiAgICAgICAgICogVGhlIGRhdGEgc2VudCBieSB7QGxpbmsgU2lnbmFsSGFuZGxlclNpbmdsZXRvbiNzZW5kfS5cbiAgICAgICAgICovXG4gICAgICAgIHRoaXMuZGF0YSA9IGRhdGE7XG5cbiAgICAgICAgLyoqXG4gICAgICAgICAqIFRoZSBzaWduYWwgbmFtZS5cbiAgICAgICAgICpcbiAgICAgICAgICogQHR5cGUge3N0cmluZ31cbiAgICAgICAgICovXG4gICAgICAgIHRoaXMuc2lnbmFsTmFtZSA9IHNpZ25hbE5hbWU7XG5cbiAgICAgICAgLyoqXG4gICAgICAgICAqIFRoZSByZWNlaXZlciBuYW1lLlxuICAgICAgICAgKlxuICAgICAgICAgKiBAdHlwZSB7c3RyaW5nfVxuICAgICAgICAgKi9cbiAgICAgICAgdGhpcy5yZWNlaXZlck5hbWUgPSByZWNlaXZlck5hbWU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGEgc3RyaW5nIHdpdGggZGVidWcgaW5mb3JtYXRpb24gYWJvdXQgdGhlIHJlY2VpdmVkIHNpZ25hbC5cbiAgICAgKi9cbiAgICB0b1N0cmluZygpIHtcbiAgICAgICAgbGV0IHByZXR0eURhdGEgPSBuZXcgUHJldHR5Rm9ybWF0KHRoaXMuZGF0YSkudG9TdHJpbmcoMik7XG4gICAgICAgIHJldHVybiBgc2lnbmFsTmFtZT1cIiR7dGhpcy5zaWduYWxOYW1lfVwiLCBgICtcbiAgICAgICAgICAgIGByZWNlaXZlck5hbWU9XCIke3RoaXMucmVjZWl2ZXJOYW1lfVwiLCBgICtcbiAgICAgICAgICAgIGBkYXRhPSR7cHJldHR5RGF0YX1gO1xuICAgIH1cbn1cblxuXG4vKipcbiAqIFByaXZhdGUgY2xhc3MgdXNlZCBieSB7QGxpbmsgX1NpZ25hbFJlY2VpdmVyc30gdG8gcmVwcmVzZW50XG4gKiBhIHNpbmdsZSByZWNlaXZlciBsaXN0ZW5pbmcgZm9yIGEgc2luZ2xlIHNpZ25hbC5cbiAqL1xuY2xhc3MgX1NpZ25hbFJlY2VpdmVyIHtcbiAgICBjb25zdHJ1Y3RvcihzaWduYWwsIG5hbWUsIGNhbGxiYWNrKSB7XG4gICAgICAgIHRoaXMuc2lnbmFsID0gc2lnbmFsO1xuICAgICAgICB0aGlzLm5hbWUgPSBuYW1lO1xuICAgICAgICB0aGlzLmNhbGxiYWNrID0gY2FsbGJhY2s7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQXN5bmNocm9ub3VzbHkgdHJpZ2dlciB0aGUgcmVjZWl2ZXIgY2FsbGJhY2suXG4gICAgICogQHBhcmFtIGRhdGEgVGhlIHNpZ25hbCBkYXRhICh0aGUgZGF0YSBhcmd1bWVudCBwcm92aWRlZCBmb3JcbiAgICAgKiAgICB7QGxpbmsgU2lnbmFsSGFuZGxlclNpbmdsZXRvbiNzZW5kfS5cbiAgICAgKi9cbiAgICB0cmlnZ2VyKGRhdGEpIHtcbiAgICAgICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICAgICAgICB0aGlzLmNhbGxiYWNrKG5ldyBSZWNlaXZlZFNpZ25hbEluZm8oZGF0YSwgdGhpcy5zaWduYWwubmFtZSwgdGhpcy5uYW1lKSk7XG4gICAgICAgIH0sIDApO1xuICAgIH1cbn1cblxuXG4vKipcbiAqIE9iamVjdCBjb250YWluaW5nIGRlYnVnZ2luZyBpbmZvcm1hdGlvbiBhYm91dCBhIHNlbnRcbiAqIHNpZ25hbC5cbiAqL1xuZXhwb3J0IGNsYXNzIFNlbnRTaWduYWxJbmZvIHtcbiAgICBjb25zdHJ1Y3RvcihzaWduYWxOYW1lKSB7XG4gICAgICAgIC8qKlxuICAgICAgICAgKiBUaGUgc2lnbmFsIG5hbWUuXG4gICAgICAgICAqXG4gICAgICAgICAqIEB0eXBlIHtzdHJpbmd9XG4gICAgICAgICAqL1xuICAgICAgICB0aGlzLnNpZ25hbE5hbWUgPSBzaWduYWxOYW1lO1xuXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBBcnJheSBvZiB0cmlnZ2VyZWQgcmVjZWl2ZXIgbmFtZXMuXG4gICAgICAgICAqXG4gICAgICAgICAqIEB0eXBlIHtBcnJheX1cbiAgICAgICAgICovXG4gICAgICAgIHRoaXMudHJpZ2dlcmVkUmVjZWl2ZXJOYW1lcyA9IFtdO1xuICAgIH1cblxuICAgIF9hZGRSZWNlaXZlck5hbWUocmVjZWl2ZXJOYW1lKSB7XG4gICAgICAgIHRoaXMudHJpZ2dlcmVkUmVjZWl2ZXJOYW1lcy5wdXNoKHJlY2VpdmVyTmFtZSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGEgc3RyaW5nIHJlcHJlc2VudGF0aW9uIG9mIHRoZSBzZW50IHNpZ25hbCBpbmZvLlxuICAgICAqXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cbiAgICB0b1N0cmluZygpIHtcbiAgICAgICAgbGV0IHJlY2VpdmVycyA9IHRoaXMudHJpZ2dlcmVkUmVjZWl2ZXJOYW1lcy5qb2luKCcsICcpO1xuICAgICAgICBpZihyZWNlaXZlcnMgPT09ICcnKSB7XG4gICAgICAgICAgICByZWNlaXZlcnMgPSAnTk8gUkVDRUlWRVJTJztcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gYFNpZ25hbDogJHt0aGlzLnNpZ25hbE5hbWV9IHdhcyBzZW50IHRvOiAke3JlY2VpdmVyc31gO1xuICAgIH1cbn1cblxuXG4vKipcbiAqIFByaXZhdGUgY2xhc3MgdXNlZCBieSB7QGxpbmsgU2lnbmFsSGFuZGxlclNpbmdsZXRvbn1cbiAqIHRvIHJlcHJlc2VudCBhbGwgcmVjZWl2ZXJzIGZvciBhIHNpbmdsZSBzaWduYWwuXG4gKi9cbmNsYXNzIF9TaWduYWxSZWNlaXZlcnMge1xuICAgIGNvbnN0cnVjdG9yKG5hbWUpIHtcbiAgICAgICAgdGhpcy5uYW1lID0gbmFtZTtcbiAgICAgICAgdGhpcy5yZWNlaXZlck1hcCA9IG5ldyBNYXAoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBZGQgYSByZWNlaXZlci5cbiAgICAgKlxuICAgICAqIEB0aHJvdyBEdXBsaWNhdGVSZWNlaXZlck5hbWVGb3JTaWduYWwgSWYgdGhlIHJlY2VpdmVyIGlzIGFscmVhZHkgcmVnaXN0ZXJlZCBmb3IgdGhlIHNpZ25hbC5cbiAgICAgKi9cbiAgICBhZGRSZWNlaXZlcihyZWNlaXZlck5hbWUsIGNhbGxiYWNrKSB7XG4gICAgICAgIGlmKHRoaXMucmVjZWl2ZXJNYXAuaGFzKHJlY2VpdmVyTmFtZSkpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBEdXBsaWNhdGVSZWNlaXZlck5hbWVGb3JTaWduYWwoXG4gICAgICAgICAgICAgICAgYFRoZSBcIiR7cmVjZWl2ZXJOYW1lfVwiIHJlY2VpdmVyIGlzIGFscmVhZHkgcmVnaXN0ZXJlZCBmb3IgdGhlIFwiJHt0aGlzLm5hbWV9XCIgc2lnbmFsYCk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5yZWNlaXZlck1hcC5zZXQoXG4gICAgICAgICAgICByZWNlaXZlck5hbWUsXG4gICAgICAgICAgICBuZXcgX1NpZ25hbFJlY2VpdmVyKHRoaXMsIHJlY2VpdmVyTmFtZSwgY2FsbGJhY2spKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW1vdmUgYSByZWNlaXZlci5cbiAgICAgKlxuICAgICAqIElmIHRoZSByZWNlaXZlciBpcyBub3QgcmVnaXN0ZXJlZCBmb3IgdGhlIHNpZ25hbCxcbiAgICAgKiBub3RoaW5nIGhhcHBlbnMuXG4gICAgICovXG4gICAgcmVtb3ZlUmVjZWl2ZXIocmVjZWl2ZXJOYW1lKSB7XG4gICAgICAgIGlmKHRoaXMucmVjZWl2ZXJNYXAuaGFzKHJlY2VpdmVyTmFtZSkpIHtcbiAgICAgICAgICAgIHRoaXMucmVjZWl2ZXJNYXAuZGVsZXRlKHJlY2VpdmVyTmFtZSk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDaGVjayBpZiB3ZSBoYXZlIGEgc3BlY2lmaWMgcmVjZWl2ZXIgZm9yIHRoaXMgc2lnbmFsLlxuICAgICAqL1xuICAgIGhhc1JlY2VpdmVyKHJlY2VpdmVyTmFtZSkge1xuICAgICAgICByZXR1cm4gdGhpcy5yZWNlaXZlck1hcC5oYXMocmVjZWl2ZXJOYW1lKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG51bWJlciBvZiByZWNlaXZlcnMgcmVnaXN0ZXJlZCBmb3IgdGhlIHNpZ25hbC5cbiAgICAgKi9cbiAgICByZWNlaXZlckNvdW50KCkge1xuICAgICAgICByZXR1cm4gdGhpcy5yZWNlaXZlck1hcC5zaXplO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNlbmQgdGhlIHNpZ25hbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBkYXRhIFRoZSBkYXRhIHNlbnQgd2l0aCB0aGUgc2lnbmFsLiBGb3J3YXJkZWQgdG9cbiAgICAgKiAgICAgIHRoZSBzaWduYWwgcmVjZWl2ZXIgY2FsbGJhY2suXG4gICAgICogQHBhcmFtIHtTZW50U2lnbmFsSW5mb30gaW5mbyBJZiB0aGlzIGlzIHByb3ZpZGVkLCB3ZSBhZGQgdGhlXG4gICAgICogICAgICBuYW1lIG9mIGFsbCByZWNlaXZlcnMgdGhlIHNpZ25hbCB3YXMgc2VudCB0by5cbiAgICAgKi9cbiAgICBzZW5kKGRhdGEsIGluZm8pIHtcbiAgICAgICAgZm9yKGxldCByZWNlaXZlciBvZiB0aGlzLnJlY2VpdmVyTWFwLnZhbHVlcygpKSB7XG4gICAgICAgICAgICByZWNlaXZlci50cmlnZ2VyKGRhdGEpO1xuICAgICAgICAgICAgaWYoaW5mbykge1xuICAgICAgICAgICAgICAgIGluZm8uX2FkZFJlY2VpdmVyTmFtZShyZWNlaXZlci5uYW1lKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cbn1cblxuXG4vKipcbiAqIFRoZSBpbnN0YW5jZSBvZiB0aGUge0BsaW5rIFNpZ25hbEhhbmRsZXJTaW5nbGV0b259LlxuICovXG5sZXQgX2luc3RhbmNlID0gbnVsbDtcblxuLyoqXG4gKiBTaWduYWwgaGFuZGxlciBzaW5nbGV0b24gZm9yIGdsb2JhbCBjb21tdW5pY2F0aW9uLlxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkJhc2ljIGV4YW1wbGU8L2NhcHRpb24+XG4gKiBsZXQgc2lnbmFsSGFuZGxlciA9IG5ldyBTaWduYWxIYW5kbGVyU2luZ2xldG9uKCk7XG4gKiBzaWduYWxIYW5kbGVyLmFkZFJlY2VpdmVyKCdteWFwcC5teXNpZ25hbCcsICdteW90aGVyYXBwLk15UmVjZWl2ZXInLCAocmVjZWl2ZWRTaWduYWxJbmZvKSA9PiB7XG4gKiAgICAgY29uc29sZS5sb2coJ1NpZ25hbCByZWNlaXZlZC4gRGF0YTonLCByZWNlaXZlZFNpZ25hbEluZm8uZGF0YSk7XG4gKiB9KTtcbiAqIHNpZ25hbEhhbmRsZXIuc2VuZCgnbXlhcHAubXlzaWduYWwnLCB7J3RoZSc6ICdkYXRhJ30pO1xuICpcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5SZWNvbW1lbmRlZCBzaWduYWwgYW5kIHJlY2VpdmVyIG5hbWluZzwvY2FwdGlvbj5cbiAqXG4gKiAvLyBJbiBteWFwcC9tZW51L01lbnVDb21wb25lbnQuanNcbiAqIGNsYXNzIE1lbnVDb21wb25lbnQge1xuICogICAgIGNvbnN0cnVjdG9yKG1lbnVOYW1lKSB7XG4gKiAgICAgICAgIHRoaXMubWVudU5hbWUgPSBtZW51TmFtZTtcbiAqICAgICAgICAgbGV0IHNpZ25hbEhhbmRsZXIgPSBuZXcgU2lnbmFsSGFuZGxlclNpbmdsZXRvbigpO1xuICogICAgICAgICBzaWduYWxIYW5kbGVyLmFkZFJlY2VpdmVyKFxuICogICAgICAgICAgICAgYHRvZ2dsZU1lbnUjJHt0aGlzLm1lbnVOYW1lfWAsXG4gKiAgICAgICAgICAgICAnbXlhcHAubWVudS5NZW51Q29tcG9uZW50JyxcbiAqICAgICAgICAgICAgIChyZWNlaXZlZFNpZ25hbEluZm8pID0+IHtcbiAqICAgICAgICAgICAgICAgICAgdGhpcy50b2dnbGUoKTtcbiAqICAgICAgICAgICAgIH1cbiAqICAgICAgICAgKTtcbiAqICAgICB9XG4gKiAgICAgdG9nZ2xlKCkge1xuICogICAgICAgICAvLyBUb2dnbGUgdGhlIG1lbnVcbiAqICAgICB9XG4gKiB9XG4gKlxuICogLy8gSW4gbXlvdGhlcmFwcC93aWRnZXRzL01lbnVUb2dnbGUuanNcbiAqIGNsYXNzIE1lbnVUb2dnbGUge1xuICogICAgIGNvbnN0cnVjdG9yKG1lbnVOYW1lKSB7XG4gKiAgICAgICAgIHRoaXMubWVudU5hbWUgPSBtZW51TmFtZTtcbiAqICAgICB9XG4gKiAgICAgdG9nZ2xlKCkge1xuICogICAgICAgICBsZXQgc2lnbmFsSGFuZGxlciA9IG5ldyBTaWduYWxIYW5kbGVyU2luZ2xldG9uKCk7XG4gKiAgICAgICAgIHNpZ25hbEhhbmRsZXIuc2VuZChgdG9nZ2xlTWVudSMke3RoaXMubWVudU5hbWV9YCk7XG4gKiAgICAgfVxuICogfVxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPk11bHRpcGxlIHJlY2VpdmVyczwvY2FwdGlvbj5cbiAqIGxldCBzaWduYWxIYW5kbGVyID0gbmV3IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24oKTtcbiAqIHNpZ25hbEhhbmRsZXIuYWRkUmVjZWl2ZXIoJ215YXBwLm15c2lnbmFsJywgJ215b3RoZXJhcHAuTXlGaXJzdFJlY2VpdmVyJywgKHJlY2VpdmVkU2lnbmFsSW5mbykgPT4ge1xuICogICAgIGNvbnNvbGUubG9nKCdTaWduYWwgcmVjZWl2ZWQgYnkgcmVjZWl2ZXIgMSEnKTtcbiAqIH0pO1xuICogc2lnbmFsSGFuZGxlci5hZGRSZWNlaXZlcignbXlhcHAubXlzaWduYWwnLCAnbXlvdGhlcmFwcC5NeVNlY29uZFJlY2VpdmVyJywgKHJlY2VpdmVkU2lnbmFsSW5mbykgPT4ge1xuICogICAgIGNvbnNvbGUubG9nKCdTaWduYWwgcmVjZWl2ZWQgYnkgcmVjZWl2ZXIgMSEnKTtcbiAqIH0pO1xuICogc2lnbmFsSGFuZGxlci5zZW5kKCdteWFwcC5teXNpZ25hbCcsIHsndGhlJzogJ2RhdGEnfSk7XG4gKlxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkRlYnVnZ2luZzwvY2FwdGlvbj5cbiAqIGxldCBzaWduYWxIYW5kbGVyID0gbmV3IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24oKTtcbiAqIHNpZ25hbEhhbmRsZXIuYWRkUmVjZWl2ZXIoJ215c2lnbmFsJywgJ015UmVjZWl2ZXInLCAocmVjZWl2ZWRTaWduYWxJbmZvKSA9PiB7XG4gKiAgICAgY29uc29sZS5sb2coJ3JlY2VpdmVkIHNpZ25hbDonLCByZWNlaXZlZFNpZ25hbEluZm8udG9TdHJpbmcoKSk7XG4gKiB9KTtcbiAqIHNpZ25hbEhhbmRsZXIuc2VuZCgnbXlhcHAubXlzaWduYWwnLCB7J3RoZSc6ICdkYXRhJ30sIChzZW50U2lnbmFsSW5mbykgPT4ge1xuICogICAgIGNvbnNvbGUubG9nKCdzZW50IHNpZ25hbCBpbmZvOicsIHNlbnRTaWduYWxJbmZvLnRvU3RyaW5nKCkpO1xuICogfSk7XG4gKlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBTaWduYWxIYW5kbGVyU2luZ2xldG9uIHtcblxuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBpZighX2luc3RhbmNlKSB7XG4gICAgICAgICAgICBfaW5zdGFuY2UgPSB0aGlzO1xuICAgICAgICAgICAgdGhpcy5fc2lnbmFsTWFwID0gbmV3IE1hcCgpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBfaW5zdGFuY2U7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVtb3ZlIGFsbCByZWNlaXZlcnMgZm9yIGFsbCBzaWduYWxzLlxuICAgICAqXG4gICAgICogVXNlZnVsIGZvciBkZWJ1Z2dpbmcgYW5kIHRlc3RzLCBidXQgc2hvdWxkIG5vdCBiZVxuICAgICAqIHVzZWQgZm9yIHByb2R1Y3Rpb24gY29kZS5cbiAgICAgKi9cbiAgICBjbGVhckFsbFJlY2VpdmVyc0ZvckFsbFNpZ25hbHMoKSB7XG4gICAgICAgIHRoaXMuX3NpZ25hbE1hcC5jbGVhcigpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEFkZCBhIHJlY2VpdmVyIGZvciBhIHNwZWNpZmljIHNpZ25hbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBzaWduYWxOYW1lIFRoZSBuYW1lIG9mIHRoZSBzaWduYWwuXG4gICAgICogICAgICBUeXBpY2FsbHkgc29tZXRoaW5nIGxpa2UgYGB0b2dnbGVNZW51YGAgb3IgYGBteWFwcC50b2dnbGVNZW51YGAuXG4gICAgICpcbiAgICAgKiAgICAgIFdoYXQgaWYgd2UgaGF2ZSBtdWx0aXBsZSBvYmplY3RzIGxpc3RlbmluZyBmb3IgdGhpcyBgYHRvZ2dsZU1lbnVgYFxuICAgICAqICAgICAgc2lnbmFsLCBhbmQgd2Ugb25seSB3YW50IHRvIHRvZ2dsZSBhIHNwZWNpZmljIG1lbnU/IFlvdSBuZWVkXG4gICAgICogICAgICB0byBlbnN1cmUgdGhlIHNpZ25hbE5hbWUgaXMgdW5pcXVlIGZvciBlYWNoIG1lbnUuIFdlIHJlY29tbWVuZFxuICAgICAqICAgICAgdGhhdCB5b3UgZG8gdGhpcyBieSBhZGRpbmcgYGAjPGNvbnRleHQ+YGAuIEZvciBleGFtcGxlXG4gICAgICogICAgICBgYHRvZ2dsZU1lbnUjbWFpbm1lbnVgYC4gVGhpcyBpcyBzaG93biBpbiBvbmUgb2YgdGhlIGV4YW1wbGVzXG4gICAgICogICAgICBhYm92ZS5cbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gcmVjZWl2ZXJOYW1lIFRoZSBuYW1lIG9mIHRoZSByZWNlaXZlci5cbiAgICAgKiAgICAgIE11c3QgYmUgdW5pcXVlIGZvciB0aGUgc2lnbmFsLlxuICAgICAqICAgICAgV2UgcmVjb21tZW5kIHRoYXQgeW91IHVzZSBhIHZlcnkgZXhwbGljaXQgbmFtZSBmb3IgeW91ciBzaWduYWxzLlxuICAgICAqICAgICAgSXQgc2hvdWxkIG5vcm1hbGx5IGJlIHRoZSBmdWxsIHBhdGggdG8gdGhlIG1ldGhvZCBvciBmdW5jdGlvbiByZWNlaXZpbmdcbiAgICAgKiAgICAgIHRoZSBzaWduYWwuIFNvIGlmIHlvdSBoYXZlIGEgY2xhc3MgbmFtZWQgYGBteWFwcC9tZW51L01lbnVDb21wb25lbnQuanNgYFxuICAgICAqICAgICAgdGhhdCByZWNlaXZlcyBhIHNpZ25hbCB0byB0b2dnbGUgdGhlIG1lbnUsIHRoZSByZWNlaXZlck5hbWUgc2hvdWxkIGJlXG4gICAgICogICAgICBgYG15YXBwLm1lbnUuTWVudUNvbXBvbmVudGBgLlxuICAgICAqIEBwYXJhbSBjYWxsYmFjayBUaGUgY2FsbGJhY2sgdG8gY2FsbCB3aGVuIHRoZSBzaWduYWwgaXMgc2VudC5cbiAgICAgKiAgICAgIFRoZSBjYWxsYmFjayBpcyBjYWxsZWQgd2l0aCBhIHNpbmdsZSBhcmd1bWVudCAtIGFcbiAgICAgKiAgICAgIHtAbGluayBSZWNlaXZlZFNpZ25hbEluZm99IG9iamVjdC5cbiAgICAgKi9cbiAgICBhZGRSZWNlaXZlcihzaWduYWxOYW1lLCByZWNlaXZlck5hbWUsIGNhbGxiYWNrKSB7XG4gICAgICAgIGlmKHR5cGVvZiBjYWxsYmFjayA9PT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBUeXBlRXJyb3IoJ1RoZSBjYWxsYmFjayBhcmd1bWVudCBmb3IgYWRkUmVjZWl2ZXIoKSBpcyByZXF1aXJlZC4nKTtcbiAgICAgICAgfVxuICAgICAgICBpZighdGhpcy5fc2lnbmFsTWFwLmhhcyhzaWduYWxOYW1lKSkge1xuICAgICAgICAgICAgdGhpcy5fc2lnbmFsTWFwLnNldChzaWduYWxOYW1lLCBuZXcgX1NpZ25hbFJlY2VpdmVycyhzaWduYWxOYW1lKSk7XG4gICAgICAgIH1cbiAgICAgICAgbGV0IHNpZ25hbCA9IHRoaXMuX3NpZ25hbE1hcC5nZXQoc2lnbmFsTmFtZSk7XG4gICAgICAgIHNpZ25hbC5hZGRSZWNlaXZlcihyZWNlaXZlck5hbWUsIGNhbGxiYWNrKVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSBhIHJlY2VpdmVyIGZvciBhIHNpZ25hbCBhZGRlZCB3aXRoIHtAbGluayBTaWduYWxIYW5kbGVyU2luZ2xldG9uI2FkZFJlY2VpdmVyfS5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBzaWduYWxOYW1lIFRoZSBuYW1lIG9mIHRoZSBzaWduYWwuXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IHJlY2VpdmVyTmFtZSBUaGUgbmFtZSBvZiB0aGUgcmVjZWl2ZXIuXG4gICAgICovXG4gICAgcmVtb3ZlUmVjZWl2ZXIoc2lnbmFsTmFtZSwgcmVjZWl2ZXJOYW1lKSB7XG4gICAgICAgIGlmKHRoaXMuX3NpZ25hbE1hcC5oYXMoc2lnbmFsTmFtZSkpIHtcbiAgICAgICAgICAgIGxldCBzaWduYWwgPSB0aGlzLl9zaWduYWxNYXAuZ2V0KHNpZ25hbE5hbWUpO1xuICAgICAgICAgICAgc2lnbmFsLnJlbW92ZVJlY2VpdmVyKHJlY2VpdmVyTmFtZSk7XG4gICAgICAgICAgICBpZihzaWduYWwucmVjZWl2ZXJDb3VudCgpID09PSAwKSB7XG4gICAgICAgICAgICAgICAgdGhpcy5fc2lnbmFsTWFwLmRlbGV0ZShzaWduYWxOYW1lKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIENoZWNrIGlmIGEgc2lnbmFsIGhhcyBhIHNwZWNpZmljIHJlY2VpdmVyLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IHNpZ25hbE5hbWUgVGhlIG5hbWUgb2YgdGhlIHNpZ25hbC5cbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gcmVjZWl2ZXJOYW1lIFRoZSBuYW1lIG9mIHRoZSByZWNlaXZlci5cbiAgICAgKi9cbiAgICBoYXNSZWNlaXZlcihzaWduYWxOYW1lLCByZWNlaXZlck5hbWUpIHtcbiAgICAgICAgaWYodGhpcy5fc2lnbmFsTWFwLmhhcyhzaWduYWxOYW1lKSkge1xuICAgICAgICAgICAgbGV0IHNpZ25hbCA9IHRoaXMuX3NpZ25hbE1hcC5nZXQoc2lnbmFsTmFtZSk7XG4gICAgICAgICAgICByZXR1cm4gc2lnbmFsLmhhc1JlY2VpdmVyKHJlY2VpdmVyTmFtZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICB9XG5cblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSBhbGwgcmVjZWl2ZXJzIGZvciBhIHNwZWNpZmljIHNpZ25hbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBzaWduYWxOYW1lIFRoZSBuYW1lIG9mIHRoZSBzaWduYWwgdG8gcmVtb3ZlLlxuICAgICAqL1xuICAgIGNsZWFyQWxsUmVjZWl2ZXJzRm9yU2lnbmFsKHNpZ25hbE5hbWUpIHtcbiAgICAgICAgaWYodGhpcy5fc2lnbmFsTWFwLmhhcyhzaWduYWxOYW1lKSkge1xuICAgICAgICAgICAgdGhpcy5fc2lnbmFsTWFwLmRlbGV0ZShzaWduYWxOYW1lKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNlbmQgYSBzaWduYWwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gc2lnbmFsTmFtZSBUaGUgbmFtZSBvZiB0aGUgc2lnbmFsIHRvIHNlbmQuXG4gICAgICogQHBhcmFtIGRhdGEgRGF0YSB0byBzZW5kIHRvIHRoZSBjYWxsYmFjayBvZiBhbGwgcmVjZWl2ZXJzIHJlZ2lzdGVyZWRcbiAgICAgKiAgICAgIGZvciB0aGUgc2lnbmFsLlxuICAgICAqIEBwYXJhbSBpbmZvQ2FsbGJhY2sgQW4gb3B0aW9uYWwgY2FsbGJhY2sgdGhhdCByZWNlaXZlcyBpbmZvcm1hdGlvblxuICAgICAqICAgICAgYWJvdXQgdGhlIHNpZ25hbC4gVXNlZnVsIGZvciBkZWJ1Z2dpbmcgd2hhdCBhY3R1YWxseSByZWNlaXZlZFxuICAgICAqICAgICAgdGhlIHNpZ25hbC4gVGhlIGBgaW5mb0NhbGxiYWNrYGAgaXMgY2FsbGVkIHdpdGggYSBzaW5nbGVcbiAgICAgKiAgICAgIGFyZ3VtZW50IC0gYSB7QGxpbmsgU2VudFNpZ25hbEluZm99IG9iamVjdC5cbiAgICAgKi9cbiAgICBzZW5kKHNpZ25hbE5hbWUsIGRhdGEsIGluZm9DYWxsYmFjaykge1xuICAgICAgICBsZXQgaW5mbyA9IG51bGw7XG4gICAgICAgIGlmKGluZm9DYWxsYmFjaykge1xuICAgICAgICAgICAgaW5mbyA9IG5ldyBTZW50U2lnbmFsSW5mbyhzaWduYWxOYW1lKTtcbiAgICAgICAgfVxuICAgICAgICBpZih0aGlzLl9zaWduYWxNYXAuaGFzKHNpZ25hbE5hbWUpKSB7XG4gICAgICAgICAgICBsZXQgc2lnbmFsID0gdGhpcy5fc2lnbmFsTWFwLmdldChzaWduYWxOYW1lKTtcbiAgICAgICAgICAgIHNpZ25hbC5zZW5kKGRhdGEsIGluZm8pO1xuICAgICAgICB9XG4gICAgICAgIGlmKGluZm9DYWxsYmFjaykge1xuICAgICAgICAgICAgaW5mb0NhbGxiYWNrKGluZm8pO1xuICAgICAgICB9XG4gICAgfVxufVxuIiwiaW1wb3J0IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24gZnJvbSBcIi4vU2lnbmFsSGFuZGxlclNpbmdsZXRvblwiO1xuaW1wb3J0IFdpZGdldFJlZ2lzdHJ5U2luZ2xldG9uIGZyb20gXCIuL3dpZGdldC9XaWRnZXRSZWdpc3RyeVNpbmdsZXRvblwiO1xuaW1wb3J0IExvZ2dlclNpbmdsZXRvbiBmcm9tIFwiLi9sb2cvTG9nZ2VyU2luZ2xldG9uXCI7XG5cbndpbmRvdy5pZXZ2X2pzYmFzZV9jb3JlID0ge1xuICAgIFNpZ25hbEhhbmRsZXJTaW5nbGV0b246IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24sXG4gICAgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b246IFdpZGdldFJlZ2lzdHJ5U2luZ2xldG9uLFxuICAgIExvZ2dlclNpbmdsZXRvbjogTG9nZ2VyU2luZ2xldG9uXG59O1xuIiwiaW1wb3J0IExPR0xFVkVMIGZyb20gXCIuL2xvZ2xldmVsXCI7XG5cblxuLyoqXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIEFic3RyYWN0TG9nZ2VyIHtcbiAgICBnZXRMb2dMZXZlbCgpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdNdXN0IGJlIG92ZXJyaWRkZW4gaW4gc3ViY2xhc3Nlcy4nKTtcbiAgICB9XG5cbiAgICBfbm9PdXRwdXQoKSB7XG5cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBFeHBvc2VzIGNvbnNvbGUubG9nLiBXaWxsIG9ubHkgcHJpbnQgaWYgY3VycmVudCBsZXZlbCBpc1xuICAgICAqIGhpZ2hlciB0aGFuIHtAbGluayBMb2dMZXZlbHMjREVCVUd9LlxuICAgICAqIEByZXR1cm5zIHtGdW5jdGlvbn0gY29uc29sZS5sb2dcbiAgICAgKi9cbiAgICBnZXQgZGVidWcoKSB7XG4gICAgICAgIGlmICh0aGlzLmdldExvZ0xldmVsKCkgPj0gTE9HTEVWRUwuREVCVUcpIHtcbiAgICAgICAgICAgIHJldHVybiBjb25zb2xlLmxvZy5iaW5kKGNvbnNvbGUpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0aGlzLl9ub091dHB1dDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBFeHBvc2VzIGNvbnNvbGUubG9nLiBXaWxsIG9ubHkgcHJpbnQgaWYgY3VycmVudCBsZXZlbCBpc1xuICAgICAqIGhpZ2hlciB0aGFuIHtAbGluayBMb2dMZXZlbHMjSU5GT30uXG4gICAgICogQHJldHVybnMge0Z1bmN0aW9ufSBjb25zb2xlLmxvZ1xuICAgICAqL1xuICAgIGdldCBpbmZvKCkge1xuICAgICAgICBpZiAodGhpcy5nZXRMb2dMZXZlbCgpID49IExPR0xFVkVMLklORk8pIHtcbiAgICAgICAgICAgIHJldHVybiBjb25zb2xlLmxvZy5iaW5kKGNvbnNvbGUpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0aGlzLl9ub091dHB1dDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBFeHBvc2VzIGNvbnNvbGUud2Fybi4gV2lsbCBvbmx5IHByaW50IGlmIGN1cnJlbnQgbGV2ZWwgaXNcbiAgICAgKiBoaWdoZXIgdGhhbiB7QGxpbmsgTG9nTGV2ZWxzI1dBUk5JTkd9LlxuICAgICAqIEByZXR1cm5zIHtGdW5jdGlvbn0gY29uc29sZS53YXJuXG4gICAgICovXG4gICAgZ2V0IHdhcm5pbmcoKSB7XG4gICAgICAgIGlmKHRoaXMuZ2V0TG9nTGV2ZWwoKSA+PSBMT0dMRVZFTC5XQVJOSU5HKSB7XG4gICAgICAgICAgICByZXR1cm4gY29uc29sZS53YXJuLmJpbmQoY29uc29sZSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRoaXMuX25vT3V0cHV0O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEV4cG9zZXMgY29uc29sZS5lcnJvci4gV2lsbCBvbmx5IHByaW50IGlmIGN1cnJlbnQgbGV2ZWwgaXNcbiAgICAgKiBoaWdoZXIgdGhhbiB7QGxpbmsgTG9nTGV2ZWxzI0VSUk9SfS5cbiAgICAgKiBAcmV0dXJucyB7RnVuY3Rpb259IGNvbnNvbGUuZXJyb3JcbiAgICAgKi9cbiAgICBnZXQgZXJyb3IoKSB7XG4gICAgICAgIGlmICh0aGlzLmdldExvZ0xldmVsKCkgPj0gTE9HTEVWRUwuRVJST1IpIHtcbiAgICAgICAgICAgIHJldHVybiBjb25zb2xlLmVycm9yLmJpbmQoY29uc29sZSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRoaXMuX25vT3V0cHV0O1xuICAgIH1cbn1cbiIsImltcG9ydCBBYnN0cmFjdExvZ2dlciBmcm9tIFwiLi9BYnN0cmFjdExvZ2dlclwiO1xuaW1wb3J0IExPR0xFVkVMIGZyb20gXCIuL2xvZ2xldmVsXCI7XG5cblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgTG9nZ2VyIGV4dGVuZHMgQWJzdHJhY3RMb2dnZXIge1xuICAgIC8qKlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IG5hbWUgVGhlIG5hbWUgb2YgdGhlIGxvZ2dlci5cbiAgICAgKiBAcGFyYW0ge0xvZ2dlclNpbmdsZXRvbn0gbG9nZ2VyU2luZ2xldG9uIFRoZSBsb2dnZXIgc2luZ2xldG9uXG4gICAgICogICAgICB0aGlzIGxvZ2dlciBiZWxvbmdzIHRvLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKG5hbWUsIGxvZ2dlclNpbmdsZXRvbikge1xuICAgICAgICBzdXBlcigpO1xuICAgICAgICB0aGlzLl9uYW1lID0gbmFtZTtcbiAgICAgICAgdGhpcy5fbG9nTGV2ZWwgPSBudWxsO1xuICAgICAgICB0aGlzLl9sb2dnZXJTaW5nbGV0b24gPSBsb2dnZXJTaW5nbGV0b247XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBuYW1lIG9mIHRoaXMgbG9nZ2VyLlxuICAgICAqIEByZXR1cm5zIHtzdHJpbmd9XG4gICAgICovXG4gICAgZ2V0IG5hbWUoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9uYW1lO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNldCB0aGUgbG9nbGV2ZWwgZm9yIHRoaXMgbG9nZ2VyLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtpbnR9IGxvZ0xldmVsIFRoZSBsb2cgbGV2ZWwuIE11c3QgYmUgb25lIG9mIHRoZSBsb2dsZXZlbHNcbiAgICAgKiAgICAgIGRlZmluZWQgaW4ge0BsaW5rIExvZ0xldmVsc30uXG4gICAgICogQHRocm93cyB7UmFuZ2VFcnJvcn0gaWYge0BsaW5rIExvZ0xldmVscyN2YWxpZGF0ZUxvZ0xldmVsfSBmYWlscy5cbiAgICAgKi9cbiAgICBzZXRMb2dMZXZlbChsb2dMZXZlbCkge1xuICAgICAgICBMT0dMRVZFTC52YWxpZGF0ZUxvZ0xldmVsKGxvZ0xldmVsKTtcbiAgICAgICAgdGhpcy5fbG9nTGV2ZWwgPSBsb2dMZXZlbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIGxvZyBsZXZlbC5cbiAgICAgKlxuICAgICAqIElmIG5vIGxvZyBsZXZlbCBoYXMgYmVlbiBzZXQgd2l0aCB7QGxpbmsgTG9nZ2VyI3NldExvZ0xldmVsfSxcbiAgICAgKiB0aGlzIHJldHVybnMge0BsaW5rIExvZ2dlclNpbmdsZXRvbiNnZXREZWZhdWx0TG9nTGV2ZWx9LlxuICAgICAqXG4gICAgICogQHJldHVybnMge2ludH1cbiAgICAgKi9cbiAgICBnZXRMb2dMZXZlbCgpIHtcbiAgICAgICAgaWYodGhpcy5fbG9nTGV2ZWwgPT0gbnVsbCkge1xuICAgICAgICAgICAgcmV0dXJuIHRoaXMuX2xvZ2dlclNpbmdsZXRvbi5nZXREZWZhdWx0TG9nTGV2ZWwoKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5fbG9nTGV2ZWw7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRleHR1YWwgbmFtZSBmb3IgdGhlIGxvZyBsZXZlbC4gSWYgdGhlIGxvZ2dlclxuICAgICAqIGRvZXMgbm90IGhhdmUgYSBsb2dMZXZlbCAoaWYgaXQgaW5oZXJpdHMgaXQgZnJvbSB0aGUgTG9nZ2VyU2luZ2xldG9uKVxuICAgICAqIGEgc3RyaW5nIHdpdGggaW5mb3JtYXRpb24gYWJvdXQgdGhpcyBhbmQgdGhlIGRlZmF1bHQgbG9nTGV2ZWwgZm9yIHRoZVxuICAgICAqIExvZ2dlclNpbmdsZXRvbiBpcyByZXR1cm5lZC5cbiAgICAgKlxuICAgICAqIEludGVuZGVkIGZvciBkZWJ1Z2dpbmcuIFRoZSBmb3JtYXQgb2YgdGhlIHN0cmluZyBtYXkgY2hhbmdlLlxuICAgICAqXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cblxuICAgIGdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwoKSB7XG4gICAgICAgIGlmKHRoaXMuX2xvZ0xldmVsID09IG51bGwpIHtcbiAgICAgICAgICAgIHJldHVybiAnW2RlZmF1bHQgZm9yIExvZ2dlclNpbmdsZXRvbiAtICcgK1xuICAgICAgICAgICAgICAgIGAke3RoaXMuX2xvZ2dlclNpbmdsZXRvbi5nZXRUZXh0dWFsTmFtZUZvckRlZmF1bHRMb2dMZXZlbCgpfV1gO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBMT0dMRVZFTC5nZXRUZXh0dWFsTmFtZUZvckxvZ0xldmVsKHRoaXMuZ2V0TG9nTGV2ZWwoKSk7XG4gICAgfVxuXG4gICAgZ2V0RGVidWdJbmZvU3RyaW5nKCkge1xuICAgICAgICByZXR1cm4gYCR7dGhpcy5uYW1lfTogJHt0aGlzLmdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwoKX1gO1xuICAgIH1cbn1cbiIsImltcG9ydCBMb2dnZXIgZnJvbSBcIi4vTG9nZ2VyXCI7XG5pbXBvcnQgTE9HTEVWRUwgZnJvbSBcIi4vbG9nbGV2ZWxcIjtcblxubGV0IF9pbnN0YW5jZSA9IG51bGw7XG5cblxuLyoqXG4gKiBBIGxvZ2dpbmcgc3lzdGVtLlxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkNyZWF0ZSBhbmQgdXNlIGEgbG9nZ2VyPC9jYXB0aW9uPlxuICogaW1wb3J0IExvZ2dlclNpbmdsZXRvbiBmcm9tICdpZXZ2X2pzYmFzZS9sb2cvTG9nZ2VyU2luZ2xldG9uJztcbiAqIGxldCBteWxvZ2dlciA9IG5ldyBMb2dnZXJTaW5nbGV0b24oKS5sb2dnZXJTaW5nbGV0b24uZ2V0TG9nZ2VyKCdteXByb2plY3QuTXlDbGFzcycpO1xuICogbXlsb2dnZXIuZGVidWcoJ0hlbGxvIGRlYnVnIHdvcmxkJyk7XG4gKiBteWxvZ2dlci5pbmZvKCdIZWxsbyBpbmZvIHdvcmxkJyk7XG4gKiBteWxvZ2dlci53YXJuaW5nKCdIZWxsbyB3YXJuaW5nIHdvcmxkJyk7XG4gKiBteWxvZ2dlci5lcnJvcignSGVsbG8gZXJyb3Igd29ybGQnKTtcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5TZXQgYSBkZWZhdWx0IGxvZ2xldmVsIGZvciBhbGwgbG9nZ2VyczwvY2FwdGlvbj5cbiAqIGltcG9ydCBMT0dMRVZFTCBmcm9tICdpZXZ2X2pzYmFzZS9sb2cvbG9nbGV2ZWwnO1xuICogbmV3IExvZ2dlclNpbmdsZXRvbigpLnNldERlZmF1bHRMb2dMZXZlbChMT0dMRVZFTC5ERUJVRyk7XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+U2V0IGEgY3VzdG9tIGxvZ2xldmVsIGZvciBhIHNpbmdsZSBsb2dnZXI8L2NhcHRpb24+XG4gKiBpbXBvcnQgTE9HTEVWRUwgZnJvbSAnaWV2dl9qc2Jhc2UvbG9nL2xvZ2xldmVsJztcbiAqIG5ldyBMb2dnZXJTaW5nbGV0b24oKS5nZXRMb2dnZXIoJ215bG9nZ2VyJykuc2V0TG9nbGV2ZWwoTE9HTEVWRUwuREVCVUcpO1xuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBMb2dnZXJTaW5nbGV0b24ge1xuICAgIC8qKlxuICAgICAqIEdldCBhbiBpbnN0YW5jZSBvZiB0aGUgc2luZ2xldG9uLlxuICAgICAqXG4gICAgICogVGhlIGZpcnN0IHRpbWUgdGhpcyBpcyBjYWxsZWQsIHdlIGNyZWF0ZSBhIG5ldyBpbnN0YW5jZS5cbiAgICAgKiBGb3IgYWxsIHN1YnNlcXVlbnQgY2FsbHMsIHdlIHJldHVybiB0aGUgaW5zdGFuY2UgdGhhdCB3YXNcbiAgICAgKiBjcmVhdGVkIG9uIHRoZSBmaXJzdCBjYWxsLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBpZighX2luc3RhbmNlKSB7XG4gICAgICAgICAgICBfaW5zdGFuY2UgPSB0aGlzO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuX2xvZ2dlck1hcCA9IG5ldyBNYXAoKTtcbiAgICAgICAgdGhpcy5yZXNldCgpO1xuICAgICAgICByZXR1cm4gX2luc3RhbmNlO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIG9mIGxvZ2dlcnMgcmVnaXN0ZXJlZCB1c2luZ1xuICAgICAqIHtAbGluayBnZXRMb2dnZXJ9LlxuICAgICAqXG4gICAgICogQHJldHVybnMge251bWJlcn0gVGhlIG51bWJlciBvZiBsb2dnZXJzLlxuICAgICAqL1xuICAgIGdldExvZ2dlckNvdW50KCkge1xuICAgICAgICByZXR1cm4gdGhpcy5fbG9nZ2VyTWFwLnNpemU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVzZXQgdG8gZGVmYXVsdCBsb2cgbGV2ZWwsIGFuZCBjbGVhciBhbGxcbiAgICAgKiBjdXN0b20gbG9nZ2Vycy5cbiAgICAgKi9cbiAgICByZXNldCgpIHtcbiAgICAgICAgdGhpcy5fbG9nTGV2ZWwgPSBMT0dMRVZFTC5XQVJOSU5HO1xuICAgICAgICB0aGlzLl9sb2dnZXJNYXAuY2xlYXIoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIGRlZmF1bHQgbG9nIGxldmVsLlxuICAgICAqXG4gICAgICogRGVmYXVsdHMgdG8ge0BsaW5rIExvZ0xldmVscyNXQVJOSU5HfSBpZiBub3Qgb3ZlcnJpZGRlblxuICAgICAqIHdpdGgge0BMb2dnZXJTaW5nbGV0b24jc2V0RGVmYXVsdExvZ0xldmVsfS5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIHtpbnR9IE9uZSBvZiB0aGUgbG9nbGV2ZWxzIGRlZmluZWQgaW4ge0BsaW5rIExvZ0xldmVsc31cbiAgICAgKi9cbiAgICBnZXREZWZhdWx0TG9nTGV2ZWwoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9sb2dMZXZlbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIGRlZmF1bHQgbG9nbGV2ZWwuXG4gICAgICpcbiAgICAgKiBBbGwgbG9nZ2VycyB1c2UgdGhpcyBieSBkZWZhdWx0IHVubGVzc1xuICAgICAqIHlvdSBvdmVycmlkZSB0aGVpciBsb2dsZXZlbC5cbiAgICAgKlxuICAgICAqIEBleGFtcGxlIDxjYXB0aW9uPk92ZXJyaWRlIGxvZ2xldmVsIG9mIGEgc3BlY2lmaWMgbG9nZ2VyPC9jYXB0aW9uPlxuICAgICAqIGltcG9ydCBMb2dnZXJTaW5nbGV0b24gZnJvbSAnaWV2dl9qc2Jhc2UvbG9nL0xvZ2dlclNpbmdsZXRvbic7XG4gICAgICogaW1wb3J0IExPR0xFVkVMIGZyb20gJ2lldnZfanNiYXNlL2xvZy9sb2dsZXZlbCc7XG4gICAgICogbGV0IGxvZ2dlclNpbmdsZXRvbiA9IG5ldyBMb2dnZXJTaW5nbGV0b24oKTtcbiAgICAgKiBsb2dnZXJTaW5nbGV0b24uZ2V0TG9nZ2VyKCdteWxvZ2dlcicpLnNldExvZ0xldmVsKExPR0xFVkVMLkRFQlVHKTtcbiAgICAgKlxuICAgICAqIEBwYXJhbSBsb2dMZXZlbCBUaGUgbG9nIGxldmVsLiBNdXN0IGJlIG9uZSBvZiB0aGUgbG9nbGV2ZWxzXG4gICAgICogICAgICBkZWZpbmVkIGluIHtAbGluayBMb2dMZXZlbHN9LlxuICAgICAqIEB0aHJvd3Mge1JhbmdlRXJyb3J9IGlmIHtAbGluayBMb2dMZXZlbHMjdmFsaWRhdGVMb2dMZXZlbH0gZmFpbHMuXG4gICAgICovXG4gICAgc2V0RGVmYXVsdExvZ0xldmVsKGxvZ0xldmVsKSB7XG4gICAgICAgIExPR0xFVkVMLnZhbGlkYXRlTG9nTGV2ZWwobG9nTGV2ZWwpO1xuICAgICAgICB0aGlzLl9sb2dMZXZlbCA9IGxvZ0xldmVsO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCBhIGxvZ2dlci5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBuYW1lIEEgbmFtZSBmb3IgdGhlIGxvZ2dlci4gU2hvdWxkIGJlIGEgdW5pcXVlIG5hbWUsXG4gICAgICogICAgICBzbyB0eXBpY2FsbHkgdGhlIGZ1bGwgaW1wb3J0IHBhdGggb2YgdGhlIGNsYXNzL2Z1bmN0aW9uIHVzaW5nXG4gICAgICogICAgICB0aGUgbG9nZ2VyLlxuICAgICAqIEByZXR1cm5zIHtMb2dnZXJ9XG4gICAgICovXG4gICAgZ2V0TG9nZ2VyKG5hbWUpIHtcbiAgICAgICAgaWYoIXRoaXMuX2xvZ2dlck1hcC5oYXMobmFtZSkpIHtcbiAgICAgICAgICAgIHRoaXMuX2xvZ2dlck1hcC5zZXQobmFtZSwgbmV3IExvZ2dlcihuYW1lLCB0aGlzKSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRoaXMuX2xvZ2dlck1hcC5nZXQobmFtZSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBuYW1lcyBvZiBhbGwgdGhlIHJlZ2lzdGVyZWQgbG9nZ2Vycy5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIHtBcnJheX0gU29ydGVkIGFycmF5IHdpdGggdGhlIHNhbWUgb2YgdGhlIGxvZ2dlcnMuXG4gICAgICovXG4gICAgZ2V0TG9nZ2VyTmFtZUFycmF5KCkge1xuICAgICAgICBsZXQgbG9nZ2VyTmFtZXMgPSBBcnJheS5mcm9tKHRoaXMuX2xvZ2dlck1hcC5rZXlzKCkpO1xuICAgICAgICBsb2dnZXJOYW1lcy5zb3J0KCk7XG4gICAgICAgIHJldHVybiBsb2dnZXJOYW1lcztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGV4dHVhbCBuYW1lIGZvciB0aGUgZGVmYXVsdCBsb2cgbGV2ZWwuXG4gICAgICpcbiAgICAgKiBJbnRlbmRlZCBmb3IgZGVidWdnaW5nLiBUaGUgZm9ybWF0IG9mIHRoZSBzdHJpbmcgbWF5IGNoYW5nZS5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIHtzdHJpbmd9XG4gICAgICovXG4gICAgZ2V0VGV4dHVhbE5hbWVGb3JEZWZhdWx0TG9nTGV2ZWwoKSB7XG4gICAgICAgIHJldHVybiBMT0dMRVZFTC5nZXRUZXh0dWFsTmFtZUZvckxvZ0xldmVsKHRoaXMuZ2V0RGVmYXVsdExvZ0xldmVsKCkpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCBhIHN0cmluZyB0aGF0IHN1bW1hcml6ZSBpbmZvcm1hdGlvbiBhYm91dCBhbGwgdGhlXG4gICAgICogbG9nZ2Vycy4gVGhlIHN0cmluZyBoYXMgYSBsaXN0IG9mIGxvZ2xldmVscyB3aXRoXG4gICAgICogdGhlaXIgbG9nbGV2ZWwuIFBlcmZlY3QgZm9yIGRlYnVnZ2luZy5cbiAgICAgKlxuICAgICAqIEludGVuZGVkIGZvciBkZWJ1Z2dpbmcuIFRoZSBmb3JtYXQgb2YgdGhlIHN0cmluZyBtYXkgY2hhbmdlLlxuICAgICAqXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cbiAgICBnZXREZWJ1Z0luZm9TdHJpbmcoKSB7XG4gICAgICAgIGxldCBsb2dnZXJJbmZvU3RyaW5nID0gYERlZmF1bHQgbG9nTGV2ZWw6IGAgK1xuICAgICAgICAgICAgYCR7dGhpcy5nZXRUZXh0dWFsTmFtZUZvckRlZmF1bHRMb2dMZXZlbCgpfVxcbmAgK1xuICAgICAgICAgICAgYExvZ2dlcnM6XFxuYDtcbiAgICAgICAgaWYodGhpcy5nZXRMb2dnZXJDb3VudCgpID09PSAwKSB7XG4gICAgICAgICAgICBsb2dnZXJJbmZvU3RyaW5nICs9ICcobm8gbG9nZ2VycylcXG4nO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgZm9yIChsZXQgbG9nZ2VyTmFtZSBvZiB0aGlzLmdldExvZ2dlck5hbWVBcnJheSgpKSB7XG4gICAgICAgICAgICAgICAgbGV0IGxvZ2dlciA9IHRoaXMuZ2V0TG9nZ2VyKGxvZ2dlck5hbWUpO1xuICAgICAgICAgICAgICAgIGxvZ2dlckluZm9TdHJpbmcgKz1cbiAgICAgICAgICAgICAgICAgICAgYCAtICR7bG9nZ2VyLmdldERlYnVnSW5mb1N0cmluZygpfVxcbmA7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGxvZ2dlckluZm9TdHJpbmc7XG4gICAgfVxufVxuIiwiLyoqXG4gKiBEZWZpbmVzIHZhbGlkIGxvZyBsZXZlbHMuXG4gKlxuICogTm90IHVzZWQgZGlyZWN0bHksIGJ1dCBpbnN0ZWFkIHZpYSB0aGUgTE9HTEVWRUxcbiAqIGNvbnN0YW50IGV4cG9ydGVkIGFzIGRlZmF1bHQgYnkgdGhpcyBtb2R1bGUuXG4gKlxuICogQGV4YW1wbGVcbiAqIGltcG9ydCBMT0dMRVZFTCBmcm9tICdpZXZ2X2pzYmFzZS9sb2cvbG9nbGV2ZWwnO1xuICogY29uc29sZS5sb2coJ1RoZSBkZWJ1ZyBsb2dsZXZlbCBpczonLCBMT0dMRVZFTC5ERUJVRyk7XG4gKiBMT0dMRVZFTC52YWxpZGF0ZUxvZ0xldmVsKDEwKTtcbiAqL1xuZXhwb3J0IGNsYXNzIExvZ0xldmVscyB7XG4gICAgY29uc3RydWN0b3IoKSB7XG4gICAgICAgIHRoaXMuX3ByZXR0eUxvZ0xldmVsTmFtZXMgPSB7fTtcbiAgICAgICAgdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lc1t0aGlzLkRFQlVHXSA9ICdERUJVRyc7XG4gICAgICAgIHRoaXMuX3ByZXR0eUxvZ0xldmVsTmFtZXNbdGhpcy5JTkZPXSA9ICdJTkZPJztcbiAgICAgICAgdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lc1t0aGlzLldBUk5JTkddID0gJ1dBUk5JTkcnO1xuICAgICAgICB0aGlzLl9wcmV0dHlMb2dMZXZlbE5hbWVzW3RoaXMuRVJST1JdID0gJ0VSUk9SJztcbiAgICAgICAgdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lc1t0aGlzLlNJTEVOVF0gPSAnU0lMRU5UJztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG51bWJlciBmb3IgbG9nIGxldmVsIERFQlVHLlxuICAgICAqIEByZXR1cm5zIHtudW1iZXJ9XG4gICAgICovXG4gICAgZ2V0IERFQlVHKCkge1xuICAgICAgICByZXR1cm4gNDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG51bWJlciBmb3IgbG9nIGxldmVsIElORk8uXG4gICAgICogQHJldHVybnMge251bWJlcn1cbiAgICAgKi9cbiAgICBnZXQgSU5GTygpIHtcbiAgICAgICAgcmV0dXJuIDM7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBudW1iZXIgZm9yIGxvZyBsZXZlbCBXQVJOSU5HLlxuICAgICAqIEByZXR1cm5zIHtudW1iZXJ9XG4gICAgICovXG4gICAgZ2V0IFdBUk5JTkcoKSB7XG4gICAgICAgIHJldHVybiAyO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIGZvciBsb2cgbGV2ZWwgRVJST1IuXG4gICAgICogQHJldHVybnMge251bWJlcn1cbiAgICAgKi9cbiAgICBnZXQgRVJST1IoKSB7XG4gICAgICAgIHJldHVybiAxO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIGZvciBsb2cgbGV2ZWwgU0lMRU5ULlxuICAgICAqIEByZXR1cm5zIHtudW1iZXJ9XG4gICAgICovXG4gICAgZ2V0IFNJTEVOVCgpIHtcbiAgICAgICAgcmV0dXJuIDA7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVmFsaWRhdGUgYSBsb2cgbGV2ZWwuXG4gICAgICpcbiAgICAgKiBTaG91bGQgYmUgdXNlZCBieSBhbGwgZnVuY3Rpb25zL21ldGhvZHMgdGhhdCBzZXQgYSBsb2cgbGV2ZWwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gbG9nTGV2ZWwgVGhlIGxvZ2xldmVsLlxuICAgICAqIEB0aHJvd3Mge1JhbmdlRXJyb3J9IElmIGBgbG9nTGV2ZWxgYCBpcyBub3Qgb25lXG4gICAgICogICBvZjpcbiAgICAgKlxuICAgICAqICAgLSB7QGxpbmsgTG9nTGV2ZWxzI0RFQlVHfVxuICAgICAqICAgLSB7QGxpbmsgTG9nTGV2ZWxzI0lORk99XG4gICAgICogICAtIHtAbGluayBMb2dMZXZlbHMjV0FSTklOR31cbiAgICAgKiAgIC0ge0BsaW5rIExvZ0xldmVscyNFUlJPUn1cbiAgICAgKiAgIC0ge0BsaW5rIExvZ0xldmVscyNTSUxFTlR9XG4gICAgICovXG4gICAgdmFsaWRhdGVMb2dMZXZlbChsb2dMZXZlbCkge1xuICAgICAgICBpZiAobG9nTGV2ZWwgPiB0aGlzLkRFQlVHIHx8IGxvZ0xldmVsIDwgdGhpcy5TSUxFTlQpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBSYW5nZUVycm9yKFxuICAgICAgICAgICAgICAgIGBJbnZhbGlkIGxvZyBsZXZlbDogJHtsb2dMZXZlbH0sIG11c3QgYmUgYmV0d2VlbiBgICtcbiAgICAgICAgICAgICAgICBgJHt0aGlzLlNJTEVOVH0gKFNJTEVOVCkgYW5kICR7dGhpcy5ERUJVR30gKERFQlVHKWApO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSB0ZXh0dWFsIG5hbWUgZm9yIGEgbG9nIGxldmVsLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtudW1iZXJ9IGxvZ0xldmVsIFRoZSBsb2cgbGV2ZWwgdG8gZ2V0IGEgdGV4dHVhbCBuYW1lIGZvci5cbiAgICAgKiBAcmV0dXJucyB7c3RyaW5nfVxuICAgICAqXG4gICAgICogQGV4YW1wbGVcbiAgICAgKiBjb25zdCBpbmZvVGV4dCA9IExPR0xFVkVMLmdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwoTE9HTEVWRUwuSU5GTyk7XG4gICAgICogLy8gaW5mb1RleHQgPT09ICdJTkZPJ1xuICAgICAqL1xuICAgIGdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwobG9nTGV2ZWwpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX3ByZXR0eUxvZ0xldmVsTmFtZXNbbG9nTGV2ZWxdO1xuICAgIH1cbn1cblxuY29uc3QgTE9HTEVWRUwgPSBuZXcgTG9nTGV2ZWxzKCk7XG5leHBvcnQgZGVmYXVsdCBMT0dMRVZFTDtcbiIsIi8qKlxuICogTWFrZSBhIGN1c3RvbSBlcnJvciBcImNsYXNzXCIuXG4gKlxuICogTWFrZXMgYW4gb2xkIHN0eWxlIHByb3RvdHlwZSBiYXNlZCBlcnJvciBjbGFzcy5cbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5UeXBpY2FsIHVzYWdlPC9jYXB0aW9uPlxuICogLy8gSW4gbXllcnJvcnMuanNcbiAqIGV4cG9ydCBsZXQgTXlDdXN0b21FcnJvciA9IG1ha2VDdXN0b21FcnJvcignTXlDdXN0b21FcnJvcicpO1xuICpcbiAqIC8vIFVzaW5nIHRoZSBlcnJvclxuICogaW1wb3J0IHtNeUN1c3RvbUVycm9yfSBmcm9tICcuL215ZXJyb3JzJztcbiAqIHRocm93IG5ldyBNeUN1c3RvbUVycm9yKCdUaGUgbWVzc2FnZScpO1xuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPlRocm93aW5nIHRoZSBlcnJvciAtIGNvbXBsZXRlIGV4YW1wbGU8L2NhcHRpb24+XG4gKiB0cnkge1xuICogICAgIHRocm93IG5ldyBNeUN1c3RvbUVycm9yKCdUaGUgbWVzc2FnZScsIHtcbiAqICAgICAgICAgIGNvZGU6ICdzdHVmZl9oYXBwZW5lZCcsXG4gKiAgICAgICAgICBkZXRhaWxzOiB7XG4gKiAgICAgICAgICAgICAgc2l6ZTogMTBcbiAqICAgICAgICAgIH1cbiAqICAgICB9KTtcbiAqIH0gY2F0Y2goZSkge1xuICogICAgIGlmKGUgaW5zdGFuY2VvZiBNeUN1c3RvbUVycm9yKSB7XG4gKiAgICAgICAgIGNvbnNvbGUuZXJyb3IoYCR7ZS50b1N0cmluZygpfSAtLSBDb2RlOiAke2UuY29kZX0uIFNpemU6ICR7ZS5kZXRhaWxzLnNpemV9YCk7XG4gKiAgICAgfVxuICogfVxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkRlZmluZSBhbiBlcnJvciB0aGF0IGV4dGVuZHMgRXJyb3I8L2NhcHRpb24+XG4gKiBsZXQgTm90Rm91bmRFcnJvciA9IG1ha2VDdXN0b21FcnJvcignTm90Rm91bmRFcnJvcicpO1xuICogLy8gZXJyb3IgaW5zdGFuY2VvZiBOb3RGb3VuZEVycm9yID09PSB0cnVlXG4gKiAvLyBlcnJvciBpbnN0YW5jZW9mIEVycm9yID09PSB0cnVlXG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+RGVmaW5lIGFuIGVycm9yIHRoYXQgZXh0ZW5kcyBhIGJ1aWx0IGluIGVycm9yPC9jYXB0aW9uPlxuICogbGV0IE15VmFsdWVFcnJvciA9IG1ha2VDdXN0b21FcnJvcignTXlWYWx1ZUVycm9yJywgVHlwZUVycm9yKTtcbiAqIGxldCBlcnJvciA9IG5ldyBNeVZhbHVlRXJyb3IoKTtcbiAqIC8vIGVycm9yIGluc3RhbmNlb2YgTXlWYWx1ZUVycm9yID09PSB0cnVlXG4gKiAvLyBlcnJvciBpbnN0YW5jZW9mIFR5cGVFcnJvciA9PT0gdHJ1ZVxuICogLy8gZXJyb3IgaW5zdGFuY2VvZiBFcnJvciA9PT0gdHJ1ZVxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkRlZmluZSBhbiBlcnJvciB0aGF0IGV4dGVuZHMgYW5vdGhlciBjdXN0b20gZXJyb3I8L2NhcHRpb24+XG4gKiBsZXQgTXlTdXBlckVycm9yID0gbWFrZUN1c3RvbUVycm9yKCdNeVN1cGVyRXJyb3InLCBUeXBlRXJyb3IpO1xuICogbGV0IE15U3ViRXJyb3IgPSBtYWtlQ3VzdG9tRXJyb3IoJ015U3ViRXJyb3InLCBNeVN1cGVyRXJyb3IpO1xuICogbGV0IGVycm9yID0gbmV3IE15U3ViRXJyb3IoKTtcbiAqIC8vIGVycm9yIGluc3RhbmNlb2YgTXlTdWJFcnJvciA9PT0gdHJ1ZVxuICogLy8gZXJyb3IgaW5zdGFuY2VvZiBNeVN1cGVyRXJyb3IgPT09IHRydWVcbiAqIC8vIGVycm9yIGluc3RhbmNlb2YgVHlwZUVycm9yID09PSB0cnVlXG4gKiAvLyBlcnJvciBpbnN0YW5jZW9mIEVycm9yID09PSB0cnVlXG4gKlxuICogQHBhcmFtIHtzdHJpbmd9IG5hbWUgVGhlIG5hbWUgb2YgdGhlIGVycm9yIGNsYXNzLlxuICogQHBhcmFtIHtFcnJvcn0gZXh0ZW5kc0Vycm9yIEFuIG9wdGlvbmFsIEVycm9yIHRvIGV4dGVuZC5cbiAqICAgICAgRGVmYXVsdHMgdG8ge0BsaW5rIEVycm9yfS4gQ2FuIGJlIGEgYnVpbHQgaW4gZXJyb3JcbiAqICAgICAgb3IgYSBjdXN0b20gZXJyb3IgY3JlYXRlZCBieSB0aGlzIGZ1bmN0aW9uLlxuICogQHJldHVybnMge0Vycm9yfSBUaGUgY3JlYXRlZCBlcnJvciBjbGFzcy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gbWFrZUN1c3RvbUVycm9yKG5hbWUsIGV4dGVuZHNFcnJvcikge1xuICAgIGV4dGVuZHNFcnJvciA9IGV4dGVuZHNFcnJvciB8fCBFcnJvcjtcbiAgICBsZXQgQ3VzdG9tRXJyb3IgPSBmdW5jdGlvbihtZXNzYWdlLCBwcm9wZXJ0aWVzKSB7XG4gICAgICAgIHRoaXMubWVzc2FnZSA9IG1lc3NhZ2U7XG4gICAgICAgIHZhciBsYXN0X3BhcnQgPSBuZXcgZXh0ZW5kc0Vycm9yKCkuc3RhY2subWF0Y2goL1teXFxzXSskLyk7XG4gICAgICAgIHRoaXMuc3RhY2sgPSBgJHt0aGlzLm5hbWV9IGF0ICR7bGFzdF9wYXJ0fWA7XG4gICAgICAgIGlmKHR5cGVvZiBwcm9wZXJ0aWVzICE9PSAndW5kZWZpbmVkJykge1xuICAgICAgICAgICAgT2JqZWN0LmFzc2lnbih0aGlzLCBwcm9wZXJ0aWVzKTtcbiAgICAgICAgfVxuICAgIH07XG4gICAgT2JqZWN0LnNldFByb3RvdHlwZU9mKEN1c3RvbUVycm9yLCBleHRlbmRzRXJyb3IpO1xuICAgIEN1c3RvbUVycm9yLnByb3RvdHlwZSA9IE9iamVjdC5jcmVhdGUoZXh0ZW5kc0Vycm9yLnByb3RvdHlwZSk7XG4gICAgQ3VzdG9tRXJyb3IucHJvdG90eXBlLmNvbnN0cnVjdG9yID0gQ3VzdG9tRXJyb3I7XG4gICAgQ3VzdG9tRXJyb3IucHJvdG90eXBlLm1lc3NhZ2UgPSBcIlwiO1xuICAgIEN1c3RvbUVycm9yLnByb3RvdHlwZS5uYW1lID0gbmFtZTtcbiAgICByZXR1cm4gQ3VzdG9tRXJyb3I7XG59XG4iLCJpbXBvcnQgdHlwZURldGVjdCBmcm9tIFwiLi90eXBlRGV0ZWN0XCI7XG5cbi8qKlxuICogUHJldHR5IGZvcm1hdCBhbnkgamF2YXNjcmlwdCBvYmplY3QuXG4gKlxuICogSGFuZGxlcyB0aGUgZm9sbG93aW5nIHR5cGVzOlxuICpcbiAqIC0gbnVsbFxuICogLSB1bmRlZmluZWRcbiAqIC0gTnVtYmVyXG4gKiAtIEJvb2xlYW5cbiAqIC0gU3RyaW5nXG4gKiAtIEFycmF5XG4gKiAtIE1hcFxuICogLSBTZXRcbiAqIC0gRnVuY3Rpb25cbiAqIC0gQ2xhc3MgKGRldGVjdGVkIGFzIGEgRnVuY3Rpb24sIHNvIHByZXR0eSBmb3JtYXR0ZWQganVzdCBsaWtlIGEgZnVuY3Rpb24pXG4gKiAtIE9iamVjdFxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPldpdGhvdXQgaW5kZW50YXRpb248L2NhcHRpb24+XG4gKiBuZXcgUHJldHR5Rm9ybWF0KFsxLCAyXSkudG9TdHJpbmcoKTtcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5XaXRoIGluZGVudGF0aW9uIChpbmRlbnQgYnkgMiBzcGFjZXMpPC9jYXB0aW9uPlxuICogbmV3IFByZXR0eUZvcm1hdChbMSwgMl0pLnRvU3RyaW5nKDIpO1xuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPlNpbXBsZSBleGFtcGxlczwvY2FwdGlvbj5cbiAqIG5ldyBQcmV0dHlGb3JtYXQodHJ1ZSkudG9TdHJpbmcoKSA9PT0gJ3RydWUnO1xuICogbmV3IFByZXR0eUZvcm1hdChudWxsKS50b1N0cmluZygpID09PSAnbnVsbCc7XG4gKiBuZXcgUHJldHR5Rm9ybWF0KFsxLCAyXSkudG9TdHJpbmcoKSA9PT0gJ1sxLCAyXSc7XG4gKiBuZXcgUHJldHR5Rm9ybWF0KHtuYW1lOiBcIkpvaG5cIiwgYWdlOiAyOX0pLnRvU3RyaW5nKCkgPT09ICd7XCJhZ2VcIjogMjksIFwibmFtZVwiOiBKb2hufSc7XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+Q29tcGxleCBleGFtcGxlPC9jYXB0aW9uPlxuICogbGV0IG1hcCA9IG5ldyBNYXAoKTtcbiAqIG1hcC5zZXQoJ2EnLCBbMTAsIDIwXSk7XG4gKiBtYXAuc2V0KCdiJywgWzMwLCA0MCwgNTBdKTtcbiAqIGZ1bmN0aW9uIHRlc3RGdW5jdGlvbigpIHt9XG4gKiBsZXQgb2JqID0ge1xuICogICAgIHRoZU1hcDogbWFwLFxuICogICAgIGFTZXQ6IG5ldyBTZXQoWydvbmUnLCAndHdvJ10pLFxuICogICAgIHRoZUZ1bmN0aW9uOiB0ZXN0RnVuY3Rpb25cbiAqIH07XG4gKiBjb25zdCBwcmV0dHlGb3JtYXR0ZWQgPSBuZXcgUHJldHR5Rm9ybWF0KG9iaikudG9TdHJpbmcoMik7XG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFByZXR0eUZvcm1hdCB7XG4gICAgY29uc3RydWN0b3Iob2JqKSB7XG4gICAgICAgIHRoaXMuX29iaiA9IG9iajtcbiAgICB9XG5cbiAgICBfaW5kZW50U3RyaW5nKHN0ciwgaW5kZW50LCBpbmRlbnRMZXZlbCkge1xuICAgICAgICBpZihpbmRlbnQgPT09IDApIHtcbiAgICAgICAgICAgIHJldHVybiBzdHI7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGAkeycgJy5yZXBlYXQoaW5kZW50ICogaW5kZW50TGV2ZWwpfSR7c3RyfWA7XG4gICAgfVxuXG4gICAgX29iamVjdFRvTWFwKG9iaikge1xuICAgICAgICBsZXQgbWFwID0gbmV3IE1hcCgpO1xuICAgICAgICBsZXQgc29ydGVkS2V5cyA9IEFycmF5LmZyb20oT2JqZWN0LmtleXMob2JqKSk7XG4gICAgICAgIHNvcnRlZEtleXMuc29ydCgpO1xuICAgICAgICBmb3IobGV0IGtleSBvZiBzb3J0ZWRLZXlzKSB7XG4gICAgICAgICAgICBtYXAuc2V0KGtleSwgb2JqW2tleV0pO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBtYXA7XG4gICAgfVxuXG4gICAgX3ByZXR0eUZvcm1hdEZsYXRJdGVyYWJsZShmbGF0SXRlcmFibGUsIHNpemUsIGluZGVudCwgaW5kZW50TGV2ZWwsIHByZWZpeCwgc3VmZml4KSB7XG4gICAgICAgIGxldCBvdXRwdXQgPSBwcmVmaXg7XG4gICAgICAgIGxldCBpdGVtU3VmZml4ID0gJywgJztcbiAgICAgICAgaWYoaW5kZW50KSB7XG4gICAgICAgICAgICBvdXRwdXQgPSBgJHtwcmVmaXh9XFxuYDtcbiAgICAgICAgICAgIGl0ZW1TdWZmaXggPSAnLCc7XG4gICAgICAgIH1cbiAgICAgICAgbGV0IGluZGV4ID0gMTtcbiAgICAgICAgZm9yKGxldCBpdGVtIG9mIGZsYXRJdGVyYWJsZSkge1xuICAgICAgICAgICAgbGV0IHByZXR0eUl0ZW0gPSB0aGlzLl9wcmV0dHlGb3JtYXQoaXRlbSwgaW5kZW50LCBpbmRlbnRMZXZlbCArIDEpO1xuICAgICAgICAgICAgaWYoaW5kZXggIT09IHNpemUpIHtcbiAgICAgICAgICAgICAgICBwcmV0dHlJdGVtICs9IGl0ZW1TdWZmaXg7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBvdXRwdXQgKz0gdGhpcy5faW5kZW50U3RyaW5nKHByZXR0eUl0ZW0sIGluZGVudCwgaW5kZW50TGV2ZWwgKyAxKTtcbiAgICAgICAgICAgIGlmKGluZGVudCkge1xuICAgICAgICAgICAgICAgIG91dHB1dCArPSAnXFxuJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGluZGV4ICsrO1xuICAgICAgICB9XG4gICAgICAgIG91dHB1dCArPSB0aGlzLl9pbmRlbnRTdHJpbmcoYCR7c3VmZml4fWAsIGluZGVudCwgaW5kZW50TGV2ZWwpO1xuICAgICAgICByZXR1cm4gb3V0cHV0O1xuICAgIH1cblxuICAgIF9wcmV0dHlGb3JtYXRNYXAobWFwLCBpbmRlbnQsIGluZGVudExldmVsLCBwcmVmaXgsIHN1ZmZpeCwga2V5VmFsdWVTZXBhcmF0b3IpIHtcbiAgICAgICAgbGV0IG91dHB1dCA9IHByZWZpeDtcbiAgICAgICAgbGV0IGl0ZW1TdWZmaXggPSAnLCAnO1xuICAgICAgICBpZihpbmRlbnQpIHtcbiAgICAgICAgICAgIG91dHB1dCA9IGAke3ByZWZpeH1cXG5gO1xuICAgICAgICAgICAgaXRlbVN1ZmZpeCA9ICcsJztcbiAgICAgICAgfVxuICAgICAgICBsZXQgaW5kZXggPSAxO1xuICAgICAgICBmb3IobGV0IFtrZXksIHZhbHVlXSBvZiBtYXApIHtcbiAgICAgICAgICAgIGxldCBwcmV0dHlLZXkgPSB0aGlzLl9wcmV0dHlGb3JtYXQoa2V5LCBpbmRlbnQsIGluZGVudExldmVsICsgMSk7XG4gICAgICAgICAgICBsZXQgcHJldHR5VmFsdWUgPSB0aGlzLl9wcmV0dHlGb3JtYXQodmFsdWUsIGluZGVudCwgaW5kZW50TGV2ZWwgKyAxKTtcbiAgICAgICAgICAgIGxldCBwcmV0dHlJdGVtID0gYCR7cHJldHR5S2V5fSR7a2V5VmFsdWVTZXBhcmF0b3J9JHtwcmV0dHlWYWx1ZX1gO1xuICAgICAgICAgICAgaWYoaW5kZXggIT09IG1hcC5zaXplKSB7XG4gICAgICAgICAgICAgICAgcHJldHR5SXRlbSArPSBpdGVtU3VmZml4O1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgb3V0cHV0ICs9IHRoaXMuX2luZGVudFN0cmluZyhwcmV0dHlJdGVtLCBpbmRlbnQsIGluZGVudExldmVsICsgMSk7XG4gICAgICAgICAgICBpZihpbmRlbnQpIHtcbiAgICAgICAgICAgICAgICBvdXRwdXQgKz0gJ1xcbic7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpbmRleCArKztcbiAgICAgICAgfVxuICAgICAgICBvdXRwdXQgKz0gdGhpcy5faW5kZW50U3RyaW5nKGAke3N1ZmZpeH1gLCBpbmRlbnQsIGluZGVudExldmVsKTtcbiAgICAgICAgcmV0dXJuIG91dHB1dDtcbiAgICB9XG5cbiAgICBfcHJldHR5Rm9ybWF0RnVuY3Rpb24oZm4pIHtcbiAgICAgICAgcmV0dXJuIGBbRnVuY3Rpb246ICR7Zm4ubmFtZX1dYDtcbiAgICB9XG5cbiAgICBfcHJldHR5Rm9ybWF0KG9iaiwgaW5kZW50LCBpbmRlbnRMZXZlbCkge1xuICAgICAgICBjb25zdCB0eXBlU3RyaW5nID0gdHlwZURldGVjdChvYmopO1xuICAgICAgICBsZXQgb3V0cHV0ID0gJyc7XG4gICAgICAgIGlmKHR5cGVTdHJpbmcgPT09ICdzdHJpbmcnKSB7XG4gICAgICAgICAgICBvdXRwdXQgPSBgXCIke29ian1cImA7XG4gICAgICAgIH0gZWxzZSBpZih0eXBlU3RyaW5nID09PSAnbnVtYmVyJyB8fCB0eXBlU3RyaW5nID09PSAnYm9vbGVhbicgfHxcbiAgICAgICAgICAgICAgICB0eXBlU3RyaW5nID09PSAndW5kZWZpbmVkJyB8fCB0eXBlU3RyaW5nID09PSAnbnVsbCcpIHtcbiAgICAgICAgICAgIG91dHB1dCA9IGAke29ian1gO1xuICAgICAgICB9IGVsc2UgaWYodHlwZVN0cmluZyA9PT0gJ2FycmF5Jykge1xuICAgICAgICAgICAgb3V0cHV0ID0gdGhpcy5fcHJldHR5Rm9ybWF0RmxhdEl0ZXJhYmxlKG9iaiwgb2JqLmxlbmd0aCwgaW5kZW50LCBpbmRlbnRMZXZlbCwgJ1snLCAnXScpO1xuICAgICAgICB9IGVsc2UgaWYodHlwZVN0cmluZyA9PT0gJ3NldCcpIHtcbiAgICAgICAgICAgIG91dHB1dCA9IHRoaXMuX3ByZXR0eUZvcm1hdEZsYXRJdGVyYWJsZShvYmosIG9iai5zaXplLCBpbmRlbnQsIGluZGVudExldmVsLCAnU2V0KCcsICcpJyk7XG4gICAgICAgIH0gZWxzZSBpZih0eXBlU3RyaW5nID09PSAnbWFwJykge1xuICAgICAgICAgICAgb3V0cHV0ID0gdGhpcy5fcHJldHR5Rm9ybWF0TWFwKG9iaiwgaW5kZW50LCBpbmRlbnRMZXZlbCwgJ01hcCgnLCAnKScsICcgPT4gJyk7XG4gICAgICAgIH0gZWxzZSBpZih0eXBlU3RyaW5nID09PSAnZnVuY3Rpb24nKSB7XG4gICAgICAgICAgICBvdXRwdXQgPSB0aGlzLl9wcmV0dHlGb3JtYXRGdW5jdGlvbihvYmopO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgb3V0cHV0ID0gdGhpcy5fcHJldHR5Rm9ybWF0TWFwKHRoaXMuX29iamVjdFRvTWFwKG9iaiksIGluZGVudCwgaW5kZW50TGV2ZWwsICd7JywgJ30nLCAnOiAnKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gb3V0cHV0O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgcmVzdWx0cyBhcyBhIHN0cmluZywgb3B0aW9uYWxseSBpbmRlbnRlZC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7bnVtYmVyfSBpbmRlbnQgVGhlIG51bWJlciBvZiBzcGFjZXMgdG8gaW5kZW50IGJ5LiBPbmx5XG4gICAgICogICAgY2hpbGQgb2JqZWN0cyBhcmUgaW5kZW50ZWQsIGFuZCB0aGV5IGFyZSBpbmRlbnRlZCByZWN1cnNpdmVseS5cbiAgICAgKiBAcmV0dXJucyB7c3RyaW5nfVxuICAgICAqL1xuICAgIHRvU3RyaW5nKGluZGVudCkge1xuICAgICAgICBpbmRlbnQgPSBpbmRlbnQgfHwgMDtcbiAgICAgICAgcmV0dXJuIHRoaXMuX3ByZXR0eUZvcm1hdCh0aGlzLl9vYmosIGluZGVudCwgMCk7XG4gICAgfVxufVxuIiwiLyoqXG4gKiBEZXRlY3QgdGhlIHR5cGUgb2YgYW4gb2JqZWN0IGFuZCByZXR1cm4gdGhlXG4gKiByZXN1bHQgYXMgYSBzdHJpbmcuXG4gKlxuICogSGFuZGxlcyB0aGUgZm9sbG93aW5nIHR5cGVzOlxuICpcbiAqIC0gbnVsbCAgKHJldHVybmVkIGFzIGBgXCJudWxsXCJgYCkuXG4gKiAtIHVuZGVmaW5lZCAgKHJldHVybmVkIGFzIGBgXCJ1bmRlZmluZWRcImBgKS5cbiAqIC0gTnVtYmVyICAocmV0dXJuZWQgYXMgYGBcIm51bWJlclwiYGApLlxuICogLSBCb29sZWFuICAocmV0dXJuZWQgYXMgYGBcImJvb2xlYW5cImBgKS5cbiAqIC0gU3RyaW5nICAocmV0dXJuZWQgYXMgYGBcInN0cmluZ1wiYGApLlxuICogLSBBcnJheSAgKHJldHVybmVkIGFzIGBgXCJhcnJheVwiYGApLlxuICogLSBNYXAgIChyZXR1cm5lZCBhcyBgYFwibWFwXCJgYCkuXG4gKiAtIFNldCAgKHJldHVybmVkIGFzIGBgXCJzZXRcImBgKS5cbiAqIC0gRnVuY3Rpb24gIChyZXR1cm5lZCBhcyBgYFwiZnVuY3Rpb25cImBgKS5cbiAqIC0gT2JqZWN0ICAocmV0dXJuZWQgYXMgYGBcIm9iamVjdFwiYGApLlxuICpcbiAqIFdlIGRvIG5vdCBoYW5kbGUgY2xhc3NlcyAtIHRoZXkgYXJlIHJldHVybmVkIGFzIGBgXCJmdW5jdGlvblwiYGAuXG4gKiBXZSBjb3VsZCBoYW5kbGUgY2xhc3NlcywgYnV0IGZvciBCYWJlbCBjbGFzc2VzIHRoYXQgd2lsbCByZXF1aXJlXG4gKiBhIGZhaXJseSBleHBlbnNpdmUgYW5kIGVycm9yIHByb25lIHJlZ2V4LlxuICpcbiAqIEBwYXJhbSBvYmogQW4gb2JqZWN0IHRvIGRldGVjdCB0aGUgdHlwZSBmb3IuXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiB0eXBlRGV0ZWN0KG9iaikge1xuICAgIGlmKG9iaiA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm4gJ251bGwnO1xuICAgIH1cbiAgICBjb25zdCB0eXBlT2YgPSB0eXBlb2Ygb2JqO1xuICAgIGlmKHR5cGVPZiA9PT0gJ3VuZGVmaW5lZCcpIHtcbiAgICAgICAgcmV0dXJuICd1bmRlZmluZWQnO1xuICAgIH1cbiAgICBpZih0eXBlT2YgPT09ICdudW1iZXInKSB7XG4gICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICB9XG4gICAgaWYodHlwZU9mID09PSAnYm9vbGVhbicpIHtcbiAgICAgICAgcmV0dXJuICdib29sZWFuJztcbiAgICB9XG4gICAgaWYodHlwZU9mID09PSAnc3RyaW5nJykge1xuICAgICAgICByZXR1cm4gJ3N0cmluZyc7XG4gICAgfVxuICAgIGlmKHR5cGVPZiA9PT0gJ2Z1bmN0aW9uJykge1xuICAgICAgICByZXR1cm4gJ2Z1bmN0aW9uJztcbiAgICB9XG4gICAgaWYoQXJyYXkuaXNBcnJheShvYmopKSB7XG4gICAgICAgIHJldHVybiAnYXJyYXknO1xuICAgIH1cbiAgICBpZihvYmogaW5zdGFuY2VvZiBNYXApIHtcbiAgICAgICAgcmV0dXJuICdtYXAnO1xuICAgIH1cbiAgICBpZihvYmogaW5zdGFuY2VvZiBTZXQpIHtcbiAgICAgICAgcmV0dXJuICdzZXQnO1xuICAgIH1cbiAgICByZXR1cm4gJ29iamVjdCc7XG59XG4iLCJpbXBvcnQgbWFrZUN1c3RvbUVycm9yIGZyb20gXCIuLi9tYWtlQ3VzdG9tRXJyb3JcIjtcblxuLyoqXG4gKiBUaGUgaW5zdGFuY2Ugb2YgdGhlIHtAbGluayBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbn0uXG4gKi9cbmxldCBfaW5zdGFuY2UgPSBudWxsO1xuXG5cbi8qKlxuICogRXhjZXB0aW9uIHRocm93biB3aGVuIGFuIGVsZW1lbnQgd2hlcmUgd2UgZXhwZWN0IHRoZVxuICogYGBkYXRhLWlldnYtanNiYXNlLXdpZGdldC1pbnN0YW5jZWlkYGAgYXR0cmlidXRlIGRvZXNcbiAqIG5vdCBoYXZlIHRoaXMgYXR0cmlidXRlLlxuICpcbiAqIEB0eXBlIHtFcnJvcn1cbiAqL1xuZXhwb3J0IGxldCBFbGVtZW50SGFzTm9XaWRnZXRJbnN0YW5jZUlkRXJyb3IgPSBtYWtlQ3VzdG9tRXJyb3IoJ0VsZW1lbnRIYXNOb1dpZGdldEluc3RhbmNlSWRFcnJvcicpO1xuXG5cbi8qKlxuICogRXhjZXB0aW9uIHRocm93biB3aGVuIGFuIGVsZW1lbnQgdGhhdCB3ZSBleHBlY3QgdG8gaGF2ZVxuICogdGhlIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXRgYCBhdHRyaWJ1dGUgZG9lcyBub3QgaGF2ZVxuICogdGhpcyBhdHRyaWJ1dGUuXG4gKlxuICogQHR5cGUge0Vycm9yfVxuICovXG5leHBvcnQgbGV0IEVsZW1lbnRJc05vdFdpZGdldEVycm9yID0gbWFrZUN1c3RvbUVycm9yKCdFbGVtZW50SXNOb3RXaWRnZXRFcnJvcicpO1xuXG5cbi8qKlxuICogRXhjZXB0aW9uIHRocm93biB3aGVuIGFuIGVsZW1lbnQgaGFzIGFcbiAqIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXRgYCB3aXRoIGEgdmFsdWUgdGhhdFxuICogaXMgbm90IGFuIGFsaWFzIHJlZ2lzdGVyZWQgaW4gdGhlIHtAbGluayBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbn0uXG4gKlxuICogQHR5cGUge0Vycm9yfVxuICovXG5leHBvcnQgbGV0IEludmFsaWRXaWRnZXRBbGlhc0Vycm9yID0gbWFrZUN1c3RvbUVycm9yKCdJbnZhbGlkV2lkZ2V0QWxpYXNFcnJvcicpO1xuXG5cbi8qKlxuICogRXhjZXB0aW9uIHRocm93biB3aGVuIGFuIGVsZW1lbnQgd2l0aCB0aGVcbiAqIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQtaW5zdGFuY2VpZD08d2lkZ2V0SW5zdGFuY2VJZD5gYCBhdHRyaWJ1dGUgaXMgbm90IGluXG4gKiB0aGUge0BsaW5rIFdpZGdldFJlZ2lzdHJ5U2luZ2xldG9ufSB3aXRoIGBgPHdpZGdldEluc3RhbmNlSWQ+YGAuXG4gKlxuICogQHR5cGUge0Vycm9yfVxuICovXG5leHBvcnQgbGV0IEVsZW1lbnRJc05vdEluaXRpYWxpemVkQXNXaWRnZXQgPSBtYWtlQ3VzdG9tRXJyb3IoJ0VsZW1lbnRJc05vdEluaXRpYWxpemVkQXNXaWRnZXQnKTtcblxuXG4vKipcbiAqIEEgdmVyeSBsaWdodHdlaWdodCB3aWRnZXQgc3lzdGVtLlxuICpcbiAqIEJhc2ljIGV4YW1wbGUgYmVsb3cgLSBzZWUge0BsaW5rIEFic3RyYWN0V2lkZ2V0fSBmb3IgbW9yZSBleGFtcGxlcy5cbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5DcmVhdGUgYSB2ZXJ5IHNpbXBsZSB3aWRnZXQ8L2NhcHRpb24+XG4gKiBleHBvcnQgZGVmYXVsdCBjbGFzcyBPcGVuTWVudVdpZGdldCBleHRlbmRzIEFic3RyYWN0V2lkZ2V0IHtcbiAqICAgICBjb25zdHJ1Y3RvcihlbGVtZW50KSB7XG4gKiAgICAgICAgICBzdXBlcihlbGVtZW50KTtcbiAqICAgICAgICAgIHRoaXMuX29uQ2xpY2tCb3VuZCA9ICguLi5hcmdzKSA9PiB7XG4gKiAgICAgICAgICAgICAgdGhpcy5fb25DbGljayguLi5hcmdzKTtcbiAqICAgICAgICAgIH07XG4gKiAgICAgICAgICB0aGlzLmVsZW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzLl9vbkNsaWNrQm91bmQpO1xuICogICAgIH1cbiAqXG4gKiAgICAgX29uQ2xpY2sgPSAoZSkgPT4ge1xuICogICAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xuICogICAgICAgICAgY29uc29sZS5sb2coJ0kgc2hvdWxkIGhhdmUgb3BlbmVkIHRoZSBtZW51IGhlcmUnKTtcbiAqICAgICB9XG4gKlxuICogICAgIGRlc3Ryb3koKSB7XG4gKiAgICAgICAgICB0aGlzLmVsZW1lbnQucmVtb3ZlRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzLl9vbkNsaWNrQm91bmQpO1xuICogICAgIH1cbiAqIH1cbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5Vc2UgdGhlIHdpZGdldDwvY2FwdGlvbj5cbiAqIDxidXR0b24gZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQ9XCJvcGVuLW1lbnUtYnV0dG9uXCIgdHlwZT1cImJ1dHRvblwiPlxuICogICAgIE9wZW4gbWVudVxuICogPC9idXR0b24+XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+UmVnaXN0ZXIgYW5kIGxvYWQgd2lkZ2V0czwvY2FwdGlvbj5cbiAqIC8vIFNvbWV3aGVyZSB0aGF0IGlzIGNhbGxlZCBhZnRlciBhbGwgdGhlIHdpZGdldHMgYXJlIHJlbmRlcmVkXG4gKiAvLyAtIHR5cGljYWxseSBhdCB0aGUgZW5kIG9mIHRoZSA8Ym9keT5cbiAqIGltcG9ydCBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbiBmcm9tICdpZXZ2X2pzYmFzZS93aWRnZXQvV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24nO1xuICogaW1wb3J0IE9wZW5NZW51V2lkZ2V0IGZyb20gJ3BhdGgvdG8vT3Blbk1lbnVXaWRnZXQnO1xuICogY29uc3Qgd2lkZ2V0UmVnaXN0cnkgPSBuZXcgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24oKTtcbiAqIHdpZGdldFJlZ2lzdHJ5LnJlZ2lzdGVyV2lkZ2V0Q2xhc3MoJ29wZW4tbWVudS1idXR0b24nLCBPcGVuTWVudVdpZGdldCk7XG4gKiB3aWRnZXRSZWdpc3RyeS5pbml0aWFsaXplQWxsV2lkZ2V0c1dpdGhpbkVsZW1lbnQoZG9jdW1lbnQuYm9keSk7XG4gKlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbiB7XG4gICAgY29uc3RydWN0b3IoKSB7XG4gICAgICAgIGlmICghX2luc3RhbmNlKSB7XG4gICAgICAgICAgICBfaW5zdGFuY2UgPSB0aGlzO1xuICAgICAgICAgICAgdGhpcy5faW5pdGlhbGl6ZSgpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBfaW5zdGFuY2U7XG4gICAgfVxuXG4gICAgX2luaXRpYWxpemUoKSB7XG4gICAgICAgIHRoaXMuX3dpZGdldEF0dHJpYnV0ZSA9ICdkYXRhLWlldnYtanNiYXNlLXdpZGdldCc7XG4gICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlSWRBdHRyaWJ1dGUgPSAnZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQtaW5zdGFuY2VpZCc7XG4gICAgICAgIHRoaXMuX3dpZGdldENsYXNzTWFwID0gbmV3IE1hcCgpO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZU1hcCA9IG5ldyBNYXAoKTtcbiAgICAgICAgdGhpcy5fd2lkZ2V0SW5zdGFuY2VDb3VudGVyID0gMDtcbiAgICB9XG5cbiAgICBjbGVhcigpIHtcbiAgICAgICAgLy8gVE9ETzogQ2FsbCBkZXN0cm95QWxsV2lkZ2V0c1dpdGhpbkRvY3VtZW50Qm9keSgpXG4gICAgICAgIHRoaXMuX3dpZGdldENsYXNzTWFwLmNsZWFyKCk7XG4gICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlTWFwLmNsZWFyKCk7XG4gICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlQ291bnRlciA9IDA7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVnaXN0ZXIgYSB3aWRnZXQgY2xhc3MgaW4gdGhlIHJlZ2lzdHJ5LlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IGFsaWFzIFRoZSBhbGlhcyBmb3IgdGhlIHdpZGdldC4gVGhpcyBpcyB0aGUgc3RyaW5nIHRoYXRcbiAgICAgKiAgICAgIGlzIHVzZWQgYXMgdGhlIGF0dHJpYnV0ZSB2YWx1ZSB3aXRoIHRoZSBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0YGBcbiAgICAgKiAgICAgIERPTSBlbGVtZW50IGF0dHJpYnV0ZS5cbiAgICAgKiBAcGFyYW0ge0Fic3RyYWN0V2lkZ2V0fSBXaWRnZXRDbGFzcyBUaGUgd2lkZ2V0IGNsYXNzLlxuICAgICAqL1xuICAgIHJlZ2lzdGVyV2lkZ2V0Q2xhc3MoYWxpYXMsIFdpZGdldENsYXNzKSB7XG4gICAgICAgIHRoaXMuX3dpZGdldENsYXNzTWFwLnNldChhbGlhcywgV2lkZ2V0Q2xhc3MpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSB3aWRnZXQgY2xhc3MgZnJvbSByZWdpc3RyeS5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBhbGlhcyBUaGUgYWxpYXMgdGhhdCB0aGUgd2lkZ2V0IGNsYXNzIHdhcyByZWdpc3RlcmVkIHdpdGhcbiAgICAgKiAgICAgIGJ5IHVzaW5nIHtAbGluayBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbiNyZWdpc3RlcldpZGdldENsYXNzfS5cbiAgICAgKi9cbiAgICByZW1vdmVXaWRnZXRDbGFzcyhhbGlhcykge1xuICAgICAgICB0aGlzLl93aWRnZXRDbGFzc01hcC5kZWxldGUoYWxpYXMpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEluaXRpYWxpemUgdGhlIHByb3ZpZGVkIGVsZW1lbnQgYXMgYSB3aWRnZXQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGVsZW1lbnQgVGhlIERPTSBlbGVtZW50IHRvIGluaXRhbGl6ZSBhcyBhIHdpZGdldC5cbiAgICAgKlxuICAgICAqIEB0aHJvd3Mge0VsZW1lbnRJc05vdFdpZGdldEVycm9yfSBJZiB0aGUgZWxlbWVudCBkb2VzIG5vdCBoYXZlXG4gICAgICogICAgICB0aGUgYGBkYXRhLWlldnYtanNiYXNlLXdpZGdldGBgIGF0dHJpYnV0ZS5cbiAgICAgKiBAdGhyb3dzIHtJbnZhbGlkV2lkZ2V0QWxpYXNFcnJvcn0gSWYgdGhlIHdpZGdldCBhbGlhcyBpcyBub3QgaW4gdGhpcyByZWdpc3RyeS5cbiAgICAgKi9cbiAgICBpbml0aWFsaXplV2lkZ2V0KGVsZW1lbnQpIHtcbiAgICAgICAgbGV0IGFsaWFzID0gZWxlbWVudC5nZXRBdHRyaWJ1dGUodGhpcy5fd2lkZ2V0QXR0cmlidXRlKTtcbiAgICAgICAgaWYoIWFsaWFzKSB7XG4gICAgICAgICAgICB0aHJvdyBuZXcgRWxlbWVudElzTm90V2lkZ2V0RXJyb3IoXG4gICAgICAgICAgICAgICAgYFRoZVxcblxcbiR7ZWxlbWVudC5vdXRlckhUTUx9XFxuXFxuZWxlbWVudCBoYXMgbm8gb3IgZW1wdHlgICtcbiAgICAgICAgICAgICAgICBgJHt0aGlzLl93aWRnZXRBdHRyaWJ1dGV9IGF0dHJpYnV0ZS5gKTtcbiAgICAgICAgfVxuICAgICAgICBpZighdGhpcy5fd2lkZ2V0Q2xhc3NNYXAuaGFzKGFsaWFzKSkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEludmFsaWRXaWRnZXRBbGlhc0Vycm9yKGBObyBXaWRnZXRDbGFzcyByZWdpc3RlcmVkIHdpdGggdGhlIFwiJHthbGlhc31cIiBhbGlhcy5gKTtcbiAgICAgICAgfVxuICAgICAgICBsZXQgV2lkZ2V0Q2xhc3MgPSB0aGlzLl93aWRnZXRDbGFzc01hcC5nZXQoYWxpYXMpO1xuICAgICAgICBsZXQgd2lkZ2V0ID0gbmV3IFdpZGdldENsYXNzKGVsZW1lbnQpO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZUNvdW50ZXIgKys7XG4gICAgICAgIGxldCB3aWRnZXRJbnN0YW5jZUlkID0gdGhpcy5fd2lkZ2V0SW5zdGFuY2VDb3VudGVyLnRvU3RyaW5nKCk7XG4gICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlTWFwLnNldCh3aWRnZXRJbnN0YW5jZUlkLCB3aWRnZXQpO1xuICAgICAgICBlbGVtZW50LnNldEF0dHJpYnV0ZSh0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlLCB3aWRnZXRJbnN0YW5jZUlkKTtcbiAgICAgICAgcmV0dXJuIHdpZGdldDtcbiAgICB9XG5cbiAgICBfZ2V0QWxsV2lkZ2V0RWxlbWVudHNXaXRoaW5FbGVtZW50KGVsZW1lbnQpIHtcbiAgICAgICAgcmV0dXJuIEFycmF5LmZyb20oZWxlbWVudC5xdWVyeVNlbGVjdG9yQWxsKGBbJHt0aGlzLl93aWRnZXRBdHRyaWJ1dGV9XWApKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBJbml0aWFsaXplIGFsbCB3aWRnZXRzIHdpdGhpbiB0aGUgcHJvdmlkZWQgZWxlbWVudC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RWxlbWVudH0gZWxlbWVudCBBIERPTSBlbGVtZW50LlxuICAgICAqL1xuICAgIGluaXRpYWxpemVBbGxXaWRnZXRzV2l0aGluRWxlbWVudChlbGVtZW50KSB7XG4gICAgICAgIGZvcihsZXQgd2lkZ2V0RWxlbWVudCBvZiB0aGlzLl9nZXRBbGxXaWRnZXRFbGVtZW50c1dpdGhpbkVsZW1lbnQoZWxlbWVudCkpIHtcbiAgICAgICAgICAgIHRoaXMuaW5pdGlhbGl6ZVdpZGdldCh3aWRnZXRFbGVtZW50KTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgdmFsdWUgb2YgdGhlIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQtaW5zdGFuY2VpZGBgIGF0dHJpYnV0ZVxuICAgICAqIG9mIHRoZSBwcm92aWRlZCBlbGVtZW50LlxuICAgICAqXG4gICAgICogQHBhcmFtIHtFbGVtZW50fSBlbGVtZW50IEEgRE9NIGVsZW1lbnQuXG4gICAgICogQHJldHVybnMge251bGx8c3RyaW5nfVxuICAgICAqL1xuICAgIGdldFdpZGdldEluc3RhbmNlSWRGcm9tRWxlbWVudChlbGVtZW50KSB7XG4gICAgICAgIHJldHVybiBlbGVtZW50LmdldEF0dHJpYnV0ZSh0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgYSB3aWRnZXQgaW5zdGFuY2UgYnkgaXRzIHdpZGdldCBpbnN0YW5jZSBpZC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB3aWRnZXRJbnN0YW5jZUlkIEEgd2lkZ2V0IGluc3RhbmNlIGlkLlxuICAgICAqIEByZXR1cm5zIHtBYnN0cmFjdFdpZGdldH0gQSB3aWRnZXQgaW5zdGFuY2Ugb3IgYGBudWxsYGAuXG4gICAgICovXG4gICAgZ2V0V2lkZ2V0SW5zdGFuY2VCeUluc3RhbmNlSWQod2lkZ2V0SW5zdGFuY2VJZCkge1xuICAgICAgICByZXR1cm4gdGhpcy5fd2lkZ2V0SW5zdGFuY2VNYXAuZ2V0KHdpZGdldEluc3RhbmNlSWQpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIERlc3Ryb3kgdGhlIHdpZGdldCBvbiB0aGUgcHJvdmlkZWQgZWxlbWVudC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RWxlbWVudH0gZWxlbWVudCBBIERPTSBlbGVtZW50IHRoYXQgaGFzIGJlZW4gaW5pdGlhbGl6ZWQgYnlcbiAgICAgKiAgICAgIHtAbGluayBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbiNpbml0aWFsaXplV2lkZ2V0fS5cbiAgICAgKlxuICAgICAqIEB0aHJvd3Mge0VsZW1lbnRIYXNOb1dpZGdldEluc3RhbmNlSWRFcnJvcn0gSWYgdGhlIGVsZW1lbnQgaGFzXG4gICAgICogICAgICBubyBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0LWluc3RhbmNlaWRgYCBhdHRyaWJ1dGUgb3IgdGhlXG4gICAgICogICAgICBhdHRyaWJ1dGUgdmFsdWUgaXMgZW1wdHkuIFRoaXMgbm9ybWFsbHkgbWVhbnMgdGhhdFxuICAgICAqICAgICAgdGhlIGVsZW1lbnQgaXMgbm90IGEgd2lkZ2V0LCBvciB0aGF0IHRoZSB3aWRnZXRcbiAgICAgKiAgICAgIGlzIG5vdCBpbml0aWFsaXplZC5cbiAgICAgKiBAdGhyb3dzIHtFbGVtZW50SXNOb3RJbml0aWFsaXplZEFzV2lkZ2V0fSBJZiB0aGUgZWxlbWVudFxuICAgICAqICAgICAgaGFzIHRoZSBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0LWluc3RhbmNlaWRgYCBhdHRyaWJ1dGVcbiAgICAgKiAgICAgIGJ1dCB0aGUgdmFsdWUgb2YgdGhlIGF0dHJpYnV0ZSBpcyBub3QgYSB2YWxpZCB3aWRnZXQgaW5zdGFuY2VcbiAgICAgKiAgICAgIGlkLiBUaGlzIHNob3VsZCBub3QgaGFwcGVuIHVubGVzcyB5b3UgbWFuaXB1bGF0ZSB0aGVcbiAgICAgKiAgICAgIGF0dHJpYnV0ZSBtYW51YWxseSBvciB1c2UgdGhlIHByaXZhdGUgbWVtYmVycyBvZiB0aGlzIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIGRlc3Ryb3lXaWRnZXQoZWxlbWVudCkge1xuICAgICAgICBsZXQgd2lkZ2V0SW5zdGFuY2VJZCA9IHRoaXMuZ2V0V2lkZ2V0SW5zdGFuY2VJZEZyb21FbGVtZW50KGVsZW1lbnQpO1xuICAgICAgICBpZih3aWRnZXRJbnN0YW5jZUlkKSB7XG4gICAgICAgICAgICBsZXQgd2lkZ2V0SW5zdGFuY2UgPSB0aGlzLmdldFdpZGdldEluc3RhbmNlQnlJbnN0YW5jZUlkKHdpZGdldEluc3RhbmNlSWQpO1xuICAgICAgICAgICAgaWYod2lkZ2V0SW5zdGFuY2UpIHtcbiAgICAgICAgICAgICAgICB3aWRnZXRJbnN0YW5jZS5kZXN0cm95KCk7XG4gICAgICAgICAgICAgICAgdGhpcy5fd2lkZ2V0SW5zdGFuY2VNYXAuZGVsZXRlKHdpZGdldEluc3RhbmNlSWQpO1xuICAgICAgICAgICAgICAgIGVsZW1lbnQucmVtb3ZlQXR0cmlidXRlKHRoaXMuX3dpZGdldEluc3RhbmNlSWRBdHRyaWJ1dGUpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICB0aHJvdyBuZXcgRWxlbWVudElzTm90SW5pdGlhbGl6ZWRBc1dpZGdldChcbiAgICAgICAgICAgICAgICAgICAgYEVsZW1lbnRcXG5cXG4ke2VsZW1lbnQub3V0ZXJIVE1MfVxcblxcbmhhcyB0aGUgYCArXG4gICAgICAgICAgICAgICAgICAgIGAke3RoaXMuX3dpZGdldEluc3RhbmNlSWRBdHRyaWJ1dGV9IGF0dHJpYnV0ZSwgYnV0IHRoZSBpZCBpcyBgICtcbiAgICAgICAgICAgICAgICAgICAgYG5vdCBpbiB0aGUgd2lkZ2V0IHJlZ2lzdHJ5LmApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFbGVtZW50SGFzTm9XaWRnZXRJbnN0YW5jZUlkRXJyb3IoXG4gICAgICAgICAgICAgICAgYEVsZW1lbnRcXG5cXG4ke2VsZW1lbnQub3V0ZXJIVE1MfVxcblxcbmhhcyBubyBvciBlbXB0eSBgICtcbiAgICAgICAgICAgICAgICBgJHt0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlfSBhdHRyaWJ1dGUuYCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBfZ2V0QWxsSW5zdGFuY2lhdGVkV2lkZ2V0RWxlbWVudHNXaXRoaW5FbGVtZW50KGVsZW1lbnQpIHtcbiAgICAgICAgcmV0dXJuIEFycmF5LmZyb20oZWxlbWVudC5xdWVyeVNlbGVjdG9yQWxsKGBbJHt0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlfV1gKSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogRGVzdHJveSBhbGwgd2lkZ2V0cyB3aXRoaW4gdGhlIHByb3ZpZGVkIGVsZW1lbnQuXG4gICAgICogT25seSBkZXN0cm95cyB3aWRnZXRzIG9uIGVsZW1lbnRzIHRoYXQgaXMgYSBjaGlsZCBvZiB0aGUgZWxlbWVudC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RWxlbWVudH0gZWxlbWVudCBUaGUgRE9NIEVsZW1lbnQuXG4gICAgICovXG4gICAgZGVzdHJveUFsbFdpZGdldHNXaXRoaW5FbGVtZW50KGVsZW1lbnQpIHtcbiAgICAgICAgZm9yKGxldCB3aWRnZXRFbGVtZW50IG9mIHRoaXMuX2dldEFsbEluc3RhbmNpYXRlZFdpZGdldEVsZW1lbnRzV2l0aGluRWxlbWVudChlbGVtZW50KSkge1xuICAgICAgICAgICAgdGhpcy5kZXN0cm95V2lkZ2V0KHdpZGdldEVsZW1lbnQpO1xuICAgICAgICB9XG4gICAgfVxufVxuIl19
