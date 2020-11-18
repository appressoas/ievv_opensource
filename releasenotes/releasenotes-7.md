IEVV Opensource 7 releasenotes
==============================


7.0.0
=====

## What is new

- Django 3.x is the minimum required version.


## Migrating to ievv-opensource 7.0

### Migrating from 5.x
If you are migrating from ievv-opensource 5.x, you should just need to:

- Update your own application for Django 3.
- Update ievv-opensource to 7.0.x
- If you use ``ievv_model_mommy_extras``, you need to update model_mommy -> model_bakery.
  This is a good idea in any case since model_mommy is dead, and model_bakery update
  just requires renaming the imports and renaming ``mommy`` -> ``bakery``.


### Migrating from 6.x
Version 6.x of ievv-opensource was an experimental Django2 release. There is many changes
in 5.x and 7.x that is not in 6.x. You SHOULD be able to just update to ievv-opensource 7.0.x,
but you may have some issues. If you do, check out the releasenotes for 5.x.


## 7.0 patch releases

### 7.0.1
- More django3 fixes.
- Include more dependencies in setup.py.
- Fix and migrate deprecated JSONField.
- Change NullBooleanField to BooleanField(null=True).

### 7.0.2
- Remove dependency on the future library.
- Use model_bakery instead of model_mommy for the tests.
- Update ievv_model_mommy_extras to use model_bakery instead of model_mommy.

### 7.0.3
- Remove pyproject.toml. It causes an issue with strict PEP 517 checking in pip.
