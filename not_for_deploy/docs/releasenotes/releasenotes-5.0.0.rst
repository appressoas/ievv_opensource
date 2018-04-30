##################################
ievv_opensource 5.0.0 releasenotes
##################################


************
What is new?
************
- Make ``ievv docs`` not run ``ievv buildstatic`` by default. Have to use
  ``--buildstatic-docs`` to get the old default behavior.
- ``ievv_developemail``: New module that provides a develop email backend
  that makes all sent emails browsable through Django admin. See :doc:`../ievv_developemail` for
  form details.


****************
Breaking changes
****************
Removed all traces of celery. Should not break anything since the
only code using celery was ``ievv_batchframework``, and that has
been updated to using django-rq a few releases ago.
