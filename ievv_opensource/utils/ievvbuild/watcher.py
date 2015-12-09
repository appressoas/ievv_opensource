from watchdog.events import RegexMatchingEventHandler


class EventHandler(RegexMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        self.plugin = kwargs.pop('plugin')
        super(EventHandler, self).__init__(*args, **kwargs)

    def on_any_event(self, event):
        self.plugin.run()
