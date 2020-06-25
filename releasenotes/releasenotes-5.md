IEVV Opensource 5 releasenotes
==============================

The first releasenote created for ievv_opensource (for minor-version 5.23).

5.23
====

## What is new

- Customsql registry and management command supports one or more apps to be excluded. Run `ievv customsql --help` for an overview of available commands.

## 5.23: Patch releases

### 5.23.1
- Remove unused htmls import from customsql code. Was just there by mistake.

### 5.23.2
- Add optional base-url instance and path arguments to `get_translation_to_activate_for_languagecode` for i18n URL-handler.