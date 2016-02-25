from ievv_opensource import ievv_elasticsearch2


# MAIN_INDEX_FLOW = {
#     'ievv_opensource.demo.elasticsearch2.doctypes.CompanyDocType': {
#         'ievv_opensource.demo.elasticsearch2.models.on_change_company_name': [
#             {
#                 'action': 'reindex',
#                 'mode': 'blocking',
#             },
#         ],
#         'ievv_opensource.demo.elasticsearch2.models.employee_created': [
#             {
#                 'action': 'reindex_employee_count',
#                 'mode': 'blocking',
#             },
#         ],
#         'ievv_opensource.demo.elasticsearch2.models.employee_deleted': [
#             {
#                 'action': 'reindex_employee_count',
#                 'mode': 'blocking',
#             },
#         ],
#     },
#     'ievv_opensource.demo.elasticsearch2.doctypes.EmployeeDocType': {
#         'ievv_opensource.demo.elasticsearch2.models.on_change_company_name': [
#             {
#                 'action': 'reindex_company_name',
#                 'mode': 'background',
#                 'worker': 'highpriority',
#                 # Returns 0, or a positive number of milliseconds until retry.
#                 # can_start_worker_checker(batchoperation, **kwargs)
#                 'can_start_worker_checker': 'path.to.mycallable'
#                 # 'worker': 'devilry.devilry_elasticsearch.tasks.superimportant',
#             },
#         ]
#     }
# }
#
#
#
#
# IEVV_ELASTICSEARCH2_REINDEX_ALL_DOCTYPES = [
#     'ievv_opensource.demo.elasticsearch2.doctypes.CompanyDocType',
#     'ievv_opensource.demo.elasticsearch2.doctypes.EmployeeDocType',
# ]


ievv_elasticsearch2.indexingmanager.Registry.get_instance().add(
    ievv_elasticsearch2.indexingmanager.SignalSet(
        doctype_class_path='ievv_opensource.demo.elasticsearch2.doctypes.CompanyDocType',
        actionsets=[
            ievv_elasticsearch2.indexingmanager.ActionSet(
                signalpath='ievv_opensource.demo.elasticsearch2.models.on_change_company_name',
                actions=[
                    ievv_elasticsearch2.indexingmanager.Action(action='reindex'),
                    ievv_elasticsearch2.indexingmanager.Action(action='reindex_employee_count',
                                                               mode='background',
                                                               worker='highpriority'),
                ]
            )
        ]
    )
)

"""
Trigger a change (devilry_update_assignment_name)
    - Triggers one or more actions (some may be realtime, and some background, with different priorities)
    - For each action
        - Wait if we have overlapping actions
        - Execute action
"""
