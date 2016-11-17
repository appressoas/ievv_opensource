import SignalHandlerSingleton from "./SignalHandlerSingleton";
import WidgetRegistrySingleton from "./widget/WidgetRegistrySingleton";
import LoggerSingleton from "./log/LoggerSingleton";
import arrayFromPolyfill from "./polyfill/arrayFromPolyfill";


// Array.from polyfill for IE11 compatibility
arrayFromPolyfill();

window.ievv_jsbase_core = {
    SignalHandlerSingleton: SignalHandlerSingleton,
    WidgetRegistrySingleton: WidgetRegistrySingleton,
    LoggerSingleton: LoggerSingleton
};
