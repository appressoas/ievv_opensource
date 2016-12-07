import DateTimePicker from "ievv_jsui/DateTimePicker";
import SelectModalWidget from "ievv_jsui/widgets/SelectModalWidget.jsx";

export default class JsUiDemo {
  constructor() {
    this.logger = new window.ievv_jsbase_core.LoggerSingleton().getLogger("ievv_jsui_demoapp.JsUiDemo");
    this.logger.setLogLevel(window.ievv_jsbase_core.LOGLEVEL.DEBUG);
    this.logger.debug(`I am a JsUiDemo, and I am aliiiiive!`);

    const widgetRegistry = new window.ievv_jsbase_core.WidgetRegistrySingleton();
    widgetRegistry.registerWidgetClass('jsui-datetime-picker', DateTimePicker);
    widgetRegistry.registerWidgetClass('jsui-select-modal', SelectModalWidget);
    widgetRegistry.initializeAllWidgetsWithinElement(document.body);
  }
}

new JsUiDemo();
