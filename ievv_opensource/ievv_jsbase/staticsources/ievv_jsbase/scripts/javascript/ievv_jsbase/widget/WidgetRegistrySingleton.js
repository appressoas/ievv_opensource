/**
 * The instance of the {@link WidgetRegistrySingleton}.
 */
let _instance = null;


export default class WidgetRegistrySingleton {
    constructor() {
        if (!_instance) {
            _instance = this;
            this._widgetMap = new Map();
        }
        return _instance;
    }

    clearAllWidgets() {
        this._widgetMap.clear();
    }

    setWidget(alias, WidgetClass) {
        this._widgetMap.set(alias, WidgetClass);
    }

    removeWidget(alias) {
        this._widgetMap.delete(alias);
    }

    initializeWidget(alias, element) {
        let WidgetClass = this._widgetMap.get(alias);
        return new WidgetClass(element);
    }
}
