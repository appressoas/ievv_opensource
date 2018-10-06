####################################################################
`utils.class_registry_singleton` --- Framework for swappable classes
####################################################################


*****************
What is this for?
*****************
If you are creating a library where you need to enable apps using the library
to replace or add some classes with injection. There are two main use-cases:

1. You have a choice field, and you want to bind the choices to values backed by classes
   (for validation, etc.), AND you want apps using the library to be able to add more choices
   and/or replace the default choices.
2. You have some classes, such as adapters working with varying user models, and you need
   to be able to allow apps to inject their own implementations.


See :class:`ievv_opensource.utils.class_registry_singleton.ClassRegistrySingleton` examples.


********
API docs
********

.. currentmodule:: ievv_opensource.utils.class_registry_singleton

.. automodule:: ievv_opensource.utils.class_registry_singleton
    :members:
