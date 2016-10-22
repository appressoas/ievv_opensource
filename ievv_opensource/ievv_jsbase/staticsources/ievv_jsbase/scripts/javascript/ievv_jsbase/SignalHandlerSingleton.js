import makeCustomError from "./makeCustomError";

/**
 * Exception raised by {@link HttpCookies#getStrict} when the cookie is not found.
 *
 * @type {Error}
 */
export let DuplicateReceiverNameForSignal = makeCustomError('DuplicateReceiverNameForSignal');


class SignalReceiver {
    constructor(signal, name, callback) {
        this.signal = signal;
        this.name = name;
        this.callback = callback;
    }

    trigger(data) {
        setTimeout(() => {
            this.callback(data, {
                signalName: this.signal.name,
                receiverName: this.name
            });
        }, 0);
    }
}


class SignalSendInfo {
    constructor(signal) {
        this.signal = signal;
        this.triggeredReceivers = [];
    }

    addReceiver(receiverName) {
        this.triggeredReceivers.push(receiverName);
    }

    toString() {
        let receivers = this.triggeredReceivers.join(', ');
        if(receivers === '') {
            receivers = 'NO RECEIVERS';
        }
        return `Signal: ${this.signal.name} was sent do: ${receivers}`;
    }
}


class Signal {
    constructor(name) {
        this.name = name;
        this.receiverMap = new Map();
    }

    addReceiver(receiverName, callback) {
        if(this.receiverMap.has(receiverName)) {
            throw new DuplicateReceiverNameForSignal(
                `The "${receiverName}" receiver is already registered for the "${this.name}" signal`);
        }
        this.receiverMap.set(
            receiverName,
            new SignalReceiver(this, receiverName, callback));
    }

    removeReceiver(receiverName) {
        if(this.receiverMap.has(receiverName)) {
            this.receiverMap.delete(receiverName);
        }
    }

    hasReceiver(receiverName) {
        return this.receiverMap.has(receiverName);
    }

    receiverCount() {
        return this.receiverMap.size;
    }

    send(data, info) {
        for(let receiver of this.receiverMap.values()) {
            receiver.trigger(data);
            if(info) {
                info.addReceiver(receiver.name);
            }
        }
    }
}


let _instance = null;

/**
 * Signal handler singleton for global communication.
 *
 * @example
 * let signal = new SignalHandlerSingleton();
 * signal.addReceiver('myapp.mysignal', 'myotherapp.myreceiver', (data, signalDebugInfo) => {
 *      console.log('Signal received');
 *      console.log('Signal data:', data);
 *      console.log('Signal debug info:', signalDebugInfo);
 * });
 * signal.send('myapp.mysignal', {'the': 'data'});
 */
export default class SignalHandlerSingleton {

    constructor() {
        if(!_instance) {
            _instance = this;
        }
        this._signalMap = new Map();
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
     * @param {string} receiverName The name of the receiver. Must be unique for the signal.
     * @param callback The callback to call when the signal is sent.
     */
    addReceiver(signalName, receiverName, callback) {
        if(!this._signalMap.has(signalName)) {
            this._signalMap.set(signalName, new Signal(signalName));
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
     *      the signal.
     */
    send(signalName, data, infoCallback) {
        let info = null;
        if(infoCallback) {
            info = new SignalSendInfo();
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
