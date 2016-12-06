from django_cradmin.viewhelpers import generic


class Overview(generic.StandaloneBaseTemplateView):
    template_name = 'ievv_jsui_demoapp/overview.django.html'


class DateTimePickerDemo(generic.StandaloneBaseTemplateView):
    template_name = 'ievv_jsui_demoapp/ievv-jsui-datetimepicker-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['ievv_jsui_demoapp']


class SelectDemo(generic.StandaloneBaseTemplateView):
    template_name = 'ievv_jsui_demoapp/ievv-jsui-select-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['ievv_jsui_demoapp']
