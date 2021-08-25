######################
ievv_opensource 5.22.1
######################

*****
Fixes
*****
- Support django RQ up to version 2.1.x. It was wrongly frozen on ``django-rq<2``
  because of django 1.x support, but we can use versions up to 2.1.x with django 1.x.