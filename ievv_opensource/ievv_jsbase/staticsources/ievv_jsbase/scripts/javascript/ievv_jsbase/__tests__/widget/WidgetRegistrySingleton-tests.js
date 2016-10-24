import WidgetRegistrySingleton from "../../widget/WidgetRegistrySingleton";
import AbstractWidget from "../../widget/AbstractWidget";
import parseHtml from "../../dom/parseHtml";


class MockWidget extends AbstractWidget {
}


describe('WidgetRegistrySingleton', () => {
    beforeEach(() => {
        new WidgetRegistrySingleton().clearAllWidgets();
    });

    it('WidgetRegistrySingleton.setWidget()', () => {
        let mockWidget = jest.fn();
        let widgetRegistry = new WidgetRegistrySingleton();
        widgetRegistry.setWidget('test', mockWidget);
        expect(widgetRegistry._widgetMap.has('test')).toBe(true);
        expect(widgetRegistry._widgetMap.get('test')).toBe(mockWidget);
    });

    it('WidgetRegistrySingleton.setWidget() replaces', () => {
        let mockWidget1 = jest.fn();
        let mockWidget2 = jest.fn();
        let widgetRegistry = new WidgetRegistrySingleton();
        widgetRegistry.setWidget('test', mockWidget1);
        widgetRegistry.setWidget('test', mockWidget2);
        expect(widgetRegistry._widgetMap.has('test')).toBe(true);
        expect(widgetRegistry._widgetMap.get('test')).toBe(mockWidget2);
    });

    it('WidgetRegistrySingleton.removeWidget() does nothing if it does not exist', () => {
        let widgetRegistry = new WidgetRegistrySingleton();
        widgetRegistry.removeWidget('test');
    });

    it('WidgetRegistrySingleton.removeWidget() removes', () => {
        let widgetRegistry = new WidgetRegistrySingleton();
        widgetRegistry.setWidget('test', jest.fn());
        expect(widgetRegistry._widgetMap.has('test')).toBe(true);
        widgetRegistry.removeWidget('test');
        expect(widgetRegistry._widgetMap.has('test')).toBe(false);
    });

    it('WidgetRegistrySingleton.initializeWidget()', () => {
        let widgetRegistry = new WidgetRegistrySingleton();
        widgetRegistry.setWidget('test', MockWidget);
        let element = parseHtml('<div></div>');
        let widget = widgetRegistry.initializeWidget('test', element);
        expect(widget.element).toBe(element);
    });
});
