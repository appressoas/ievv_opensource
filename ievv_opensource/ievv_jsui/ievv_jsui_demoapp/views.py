from django_cradmin.viewhelpers import generic


class Overview(generic.StandaloneBaseTemplateView):
    template_name = 'ievv_jsui_demoapp/overview.django.html'


class IevvJsUiDateTimePickerDemo(generic.StandaloneBaseTemplateView):
    template_name = 'ievv_jsui_demoapp/ievv-jsui-datetimepicker-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['ievv_jsui_demoapp']

