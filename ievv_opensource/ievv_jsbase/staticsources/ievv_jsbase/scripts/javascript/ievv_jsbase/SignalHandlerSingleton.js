import makeCustomError from "./makeCustomError";

/**
 * Exception raised by {@link HttpCookies#getStrict} when the cookie is not found.
 *
 * @type {Error}
 */
export let DuplicateReceiverNameForSignal = makeCustomError('DuplicateReceiverNameForSignal');


/**
 * Represents information about the received signal.
 *
 * An object of this class is sent to the ``callback``
 * of all signal receivers.
 *
 * The data sent by the signal is available in
 * {@link ReceivedSignalInfo.data}.
 */
export class ReceivedSignalInfo {
    constructor(data, signalName, receiverName) {
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
     * Log debug information about the received signal.
     *
     * @param {string} prefix An optional prefix for the log message.
     */
    logDebugInfo(prefix) {
        let infostring = `signalName="${this.signalName}", receiverName="${this.receiverName}", data=`;
        if(prefix) {
            infostring = `${prefix}: ${infostring}`;
        }
        console.log(infostring, this.data);
    }
}


/**
 * Private class used by {@link _SignalReceivers} to represent
 * a single receiver listening for a single signal.
 */
class _SignalReceiver {
    constructor(signal, name, callback) {
        this.signal = signal;
        this.name = name;
        this.callback = callback;
    }

    /**
     * Asynchronously trigger the receiver callback.
     * @param data The signal data (the data argument provided for
     *    {@link SignalHandlerSingleton#send}.
     */
    trigger(data) {
        setTimeout(() => {
            this.callback(new ReceivedSignalInfo(data, this.signal.name, this.name));
        }, 0);
    }
}


/**
 * Object containing debugging information about a sent
 * signal.
 */
export class SentSignalInfo {
    constructor(signalName) {
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

    _addReceiverName(receiverName) {
        this.triggeredReceiverNames.push(receiverName);
    }

    /**
     * Get a string representation of the sent signal info.
     *
     * @returns {string}
     */
    toString() {
        let receivers = this.triggeredReceiverNames.join(', ');
        if(receivers === '') {
            receivers = 'NO RECEIVERS';
        }
        return `Signal: ${this.signalName} was sent do: ${receivers}`;
    }

    /**
     * Log debug information about the sent signal.
     *
     * @param {string} prefix An optional prefix for the log message.
     */
    logDebugInfo(prefix) {
        let infostring = this.toString();
        if(prefix) {
            infostring = `${prefix}: ${infostring}`;
        }
        console.log(infostring);
    }
}


/**
 * Private class used by {@link SignalHandlerSingleton}
 * to represent all receivers for a single signal.
 */
class _SignalReceivers {
    constructor(name) {
        this.name = name;
        this.receiverMap = new Map();
    }

    /**
     * Add a receiver.
     *
     * @throw DuplicateReceiverNameForSignal If the receiver is already registered for the signal.
     */
    addReceiver(receiverName, callback) {
        if(this.receiverMap.has(receiverName)) {
            throw new DuplicateReceiverNameForSignal(
                `The "${receiverName}" receiver is already registered for the "${this.name}" signal`);
        }
        this.receiverMap.set(
            receiverName,
            new _SignalReceiver(this, receiverName, callback));
    }

    /**
     * Remove a receiver.
     *
     * If the receiver is not registered for the signal,
     * nothing happens.
     */
    removeReceiver(receiverName) {
        if(this.receiverMap.has(receiverName)) {
            this.receiverMap.delete(receiverName);
        }
    }

    /**
     * Check if we have a specific receiver for this signal.
     */
    hasReceiver(receiverName) {
        return this.receiverMap.has(receiverName);
    }

    /**
     * Get the number of receivers registered for the signal.
     */
    receiverCount() {
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
    send(data, info) {
        for(let receiver of this.receiverMap.values()) {
            receiver.trigger(data);
            if(info) {
                info._addReceiverName(receiver.name);
            }
        }
    }
}


/**
 * The instance of the {@link SignalHandlerSingleton}.
 */
let _instance = null;

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
 *     receivedSignalInfo.logDebugInfo();
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'}, (sentSignalInfo) => {
 *     sentSignalInfo.logDebugInfo();
 * });
 *
 */
export default class SignalHandlerSingleton {

    constructor() {
        if(!_instance) {
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
    clearAllReceiversForAllSignals() {
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
    addReceiver(signalName, receiverName, callback) {
        if(typeof callback === 'undefined') {
            throw new TypeError('The callback argument for addReceiver() is required.');
        }
        if(!this._signalMap.has(signalName)) {
            this._signalMap.set(signalName, new _SignalReceivers(signalName));
        }
        let signal = this._signalMap.get(signalName);
        signal.addReceiver(receiverName, callback)
    }

    /**
     * Remove a receiver for a signal added with {@link SignalHandlerSingleton#addReceiver}.
     *
     * @param {string} signalName The name of the signal.
     * @param {string} receiverName The name of the receiver.
     */
    removeReceiver(signalName, receiverName) {
        if(this._signalMap.has(signalName)) {
            let signal = this._signalMap.get(signalName);
            signal.removeReceiver(receiverName);
            if(signal.receiverCount() === 0) {
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
    hasReceiver(signalName, receiverName) {
        if(this._signalMap.has(signalName)) {
            let signal = this._signalMap.get(signalName);
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
    clearAllReceiversForSignal(signalName) {
        if(this._signalMap.has(signalName)) {
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
    send(signalName, data, infoCallback) {
        let info = null;
        if(infoCallback) {
            info = new SentSignalInfo(signalName);
        }
        if(this._signalMap.has(signalName)) {
            let signal = this._signalMap.get(signalName);
            signal.send(data, info);
        }
        if(infoCallback) {
            infoCallback(info);
        }
    }
}