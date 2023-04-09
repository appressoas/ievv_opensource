IEVV Opensource 8 releasenotes
==============================


8.0.0
=====

## What is new

Updated to Django 3.2.x.

Django 3.2 is an LTS version and is expected to receive security updates for at least the next three years from it's initial 
launch (6. April 2024).


## Migrating to ievv-opensource 8.0

- Update your own application for Django 3.2. If you're coming from Django 1.11.x, there are plenty of changes through Django 2 and 3 
  that needs to be addressed (you can migrate directly to Django 3 without going through Django 2 first).
- Check out the documentation for ievv-opensource 7.x (this is the initial Django 3 release) if you're updating from Django 1 or 2.
- Update to ievv-opensource 8.x.


# 8.1

## What's new?
- ievv_sms: New debug backend for pswin and set max length and part count to 134 for pswin backend.

## 8.1 Patch releases

### 8.1.1
- register new pswin debug sms backend in apps.py

### 8.1.2
- use re_path instead of url in developemail admin model


# 8.2

## What's new?
- ievv_developemail: Set admin site name correctly in URLs, allowing the ModelAdmin for developemail to be used in multiple admin sites.

## 8.2 Patch releases

### 8.2.1
- ievvbuildstatic...cssbuild*: Update for changes to postcss/stylelint.
  - postcss: Set custom syntax for scss.
  - stylelint: Replace deprecated and removed options with the correct options.

### 8.2.2
- ievvbuildstatic: handle exit codes more correctly

### 8.2.3
- fix(ievvdevrun): port _bg argument to subprocess

### 8.2.4
- fix(npm installer): handle auth errors

### 8.2.5
- fix(ievvtasks): make ievv task exit correctly. With correct exit code and nice status message. Also handle KeyboardInterrupt.

### 8.2.6
fix(lessbuild): encode cli arguments for less correctly
