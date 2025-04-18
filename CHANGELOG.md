## 12.0.0 (2025-04-09)

### BREAKING CHANGE

- Requires Django 5.2x or higher.

### Feat

- **django**: update Django version to >=5.2.0,<6.0.0

## 11.2.0 (2025-02-03)

### Feat

- **utils**: glob copy plugin for ievv buildstatic

## 11.1.1 (2024-11-26)

### Fix

- **virtualenv**: install/upgrade pip, setuptools and wheel

## 11.1.0 (2024-11-26)

### Feat

- **python_version**: 3.12

## 11.0.0 (2024-11-15)

### BREAKING CHANGE

- rq_console handler should now use the class `rq.logutils.ColorizingStreamHandler` instead of `rq.utils.ColorizingStreamHandler`

### Feat

- **settings**: change in rq_console class
- **deps**: rq>=2.0.0, django-rq>=3.0.0

### Fix

- **buildstatic**: Update for yarn > 1.

## 9.3.6 (2024-07-01)

### Fix

- **buildstatic**: Bring back and update yarn installer for latest yarn version.
- **buildstatic**: Use get_installer() to run scripts in npmrun_jsbuild.

## 9.3.5 (2024-06-30)

### Fix

- **buildstatic**: Add support for extra npm installer args.

## 9.3.4 (2024-06-30)

### Fix

- **buildstatic**: Correctly call npm link with multiple packages - bugfixes.
- **buildstatic**: Correctly call npm link with multiple packages.
- **buildstatic**: Remove yarn installer - not maintained

## 9.3.3 (2024-04-11)

### Fix

- **buildstatic**: Ignore watchdog opened/closed events.

## 9.3.2 (2023-12-13)

### Fix

- **ievvbuildstatic**: Add support for using "npm ci" in production build.

## 9.3.1 (2023-12-13)

### Fix

- **ievvbuildstatic**: Add support for setting postcss-scss version.

## 9.3.0 (2023-12-12)

### Feat

- Import psycopg types from django instead of psycopg2. Makes us compatible with psycopg3.

## 9.2.3 (2023-06-05)

### Refactor

- **recreate-virtualenv.sh**: move into root tools folder

## 9.2.2 (2023-04-19)

### Fix

- **apps_config**: use default is true

    - batchframeworkdemo
    - customsqldemo
    - ievv_model_mommy_extras
    - ievv_sms

## 9.2.1 (2023-04-09)

### Fix

- **lessbuild**: encode cli arguments for less correctly

## 9.2.0 (2023-04-08)

### Feat

- **pyproject**: use .sh for creating venv

## 9.1.6 (2023-04-06)

### Fix

- **ievvtasks**: make ievv task exit correctly

## 9.1.5 (2023-04-06)

### Fix

- **npm installer**: handle auth errors

## 9.1.4 (2023-04-06)

### Fix

- **ievvdevrun**: port _bg argument to subprocess

## 9.1.3 (2023-04-05)

### Fix

- **ievvbuildstatic**: handle exit codes more correctly

## 9.1.2 (2023-04-03)

### Fix

- **ievv_model_mommy_extras**: :bug: use now from django utils timezone

## 9.1.1 (2023-03-31)

### Fix

- fix rq task that use python2 style print statement

## 9.1.0 (2023-03-30)
Older changelogs from this version backwards are in ``releasenotes/`` and ``not_for_deploy/docs/releasenotes/``.

## 9.0.1 (2023-03-28)

## 9.0.0 (2023-03-21)

## 8.2.1 (2023-03-18)

## 8.2.0 (2022-06-15)

## 8.1.2 (2022-04-05)

## 8.1.1 (2021-11-09)

## 8.1.0 (2021-11-09)

## 8.0.0 (2021-08-25)

## 8.0.0b1 (2021-08-24)

## 7.0.4 (2021-08-13)

## 7.0.3 (2020-11-18)

## 7.0.2 (2020-11-12)

## 7.0.1 (2020-11-12)

## 7.0.0 (2020-11-11)

## 5.25.0 (2020-10-15)

## 5.24.0 (2020-10-07)

## 5.23.2 (2020-06-25)

## 5.23.1 (2020-06-21)

## 5.23.0 (2020-05-26)

## 5.22.1 (2020-05-05)

## 5.22.0 (2020-05-05)

## 5.21.0 (2020-04-21)

## 5.20.2 (2020-04-07)

## 5.20.1 (2020-04-07)

## 5.20.0 (2020-04-07)

## 5.19.13 (2020-04-02)

## 5.19.12 (2020-01-20)

## 5.19.11 (2019-11-24)

## 5.19.10 (2019-11-23)

## 5.19.9 (2019-11-23)

## 5.19.8 (2019-11-18)

## 5.19.7 (2019-11-14)

## 5.19.6 (2019-11-08)

## 5.19.5 (2019-11-08)

## 5.19.3 (2019-11-06)

## 5.19.2 (2019-11-06)

## 5.19.1 (2019-11-01)

## 5.19.0 (2019-10-31)

## 5.18.0 (2019-10-23)

## 5.16.0 (2019-09-24)

## 5.15.0 (2019-09-19)

## v5.14.5 (2019-06-26)

## 5.14.4 (2019-06-25)

## 5.14.3 (2019-05-20)

## 5.14.2 (2019-03-04)

## 5.14.1 (2019-01-17)

## 5.14.0 (2019-01-17)

## 5.13.0 (2018-10-17)

## 5.12.0 (2018-10-08)

## 5.11.0 (2018-09-18)

## 5.10.0 (2018-08-30)

## 5.9.1 (2018-07-18)

## 5.9.0 (2018-07-18)

## 5.8.0 (2018-07-10)

## 5.7.0 (2018-07-06)

## 5.6.0 (2018-07-02)

## 5.5.1 (2018-06-30)

## 5.5.0 (2018-06-28)

## 5.4.0 (2018-06-07)

## 5.3.0 (2018-05-31)

## 5.2.2 (2018-05-29)

## 5.2.1 (2018-05-29)

## 5.2.0 (2018-05-28)

## 5.1.1 (2018-05-22)

## 5.1.0 (2018-05-21)

## 5.0.1 (2018-05-03)

## 5.0.0 (2018-04-30)

## 4.5.1 (2018-04-10)

## 4.5.0 (2018-02-13)

## 4.4.0 (2018-01-18)

## 4.3.3 (2018-01-16)

## 4.3.2 (2018-01-16)

## 4.3.1 (2017-11-13)

## 4.3.0 (2017-11-13)

## 4.2.1 (2017-10-24)

## 4.2.0 (2017-10-24)

## 4.1.0 (2017-06-05)

## 4.0.0 (2017-05-21)

## 4.0.0rc4 (2017-04-28)

## 4.0.0rc3 (2017-03-29)

## 4.0.0rc2 (2017-03-14)

## 4.0.0rc1 (2017-02-11)

## 4.0.0b18 (2017-01-29)

## 4.0.0b17 (2017-01-18)

## 4.0.0b16 (2017-01-18)

## 4.0.0b15 (2017-01-07)

## 4.0.0b14 (2016-12-12)

## 4.0.0b12 (2016-12-12)

## 4.0.0b11 (2016-12-04)

## 4.0.0b10 (2016-11-25)

## 4.0.0b9 (2016-11-21)

## 4.0.0b8 (2016-11-21)

## 4.0.0b7 (2016-11-21)

## 4.0.0b6 (2016-11-09)

## 4.0.0b4 (2016-11-01)

## 4.0.0b3 (2016-10-30)

## 4.0.0b2 (2016-10-30)

## 4.0.0b1 (2016-10-30)

## 3.4.0 (2016-10-20)

## 3.3.0 (2016-10-18)

## 3.2.0 (2016-10-05)

## 3.1.0 (2016-10-05)

## 3.0.0 (2016-09-27)

## 2.0.0 (2016-09-23)

## 1.1.9 (2016-09-06)

## 1.1.8 (2016-09-06)

## 1.1.7 (2016-08-22)

## 1.1.6 (2016-08-22)

## 1.1.5 (2016-08-18)

## 1.1.4 (2016-08-15)

## 1.1.3 (2016-08-10)

## 1.1.2 (2016-07-28)

## 1.1.1 (2016-07-28)

## 1.1.0 (2016-07-08)

## 1.0.0 (2016-06-17)

## 0.2.26 (2016-06-14)

## 0.2.25 (2016-02-16)

## 0.2.24 (2016-02-15)

## 0.2.23 (2016-02-15)

## 0.2.22 (2016-02-15)

## 0.2.21 (2016-02-05)

## 0.2.20 (2016-01-27)

## 0.2.19 (2016-01-27)

## 0.2.18 (2016-01-27)

## 0.2.17 (2016-01-25)

## 0.2.15 (2016-01-13)

## 0.2.14 (2016-01-10)

## 0.2.13 (2016-01-09)

## 0.2.12 (2015-12-17)

## 0.2.11 (2015-12-17)

## 0.2.10 (2015-12-17)

## 0.2.8 (2015-12-10)

## 0.2.7 (2015-12-09)

## 0.2.5 (2015-12-09)

## 0.2.4 (2015-12-09)

## 0.2.3 (2015-11-22)

## 0.2.2 (2015-11-19)

## 0.2.1 (2015-10-31)
