# Ievv Logging 

An easy to use interface for logging events to the database models in this app. By using this you can easily log and have a useful overview about what
is going on in e.g. scheduled scripts.

## Install

To use it, add `ievv_opensource.ievv_logging` to `INSTALLED_APPS` and run 

    python manage.py migrate

## Usage

If for example you are running a management nightly and want to log the running, do:

    from ievv_opensource.ievv_logging.utils import IevvLogging

    ievvlogging = IevvLogging(__name__) # or any custom preferred name like 'the_foo_script'
    ievvlogging.begin()

    # the script does its work

    ievvlogging.finish(
        number_of_users_updated=12,
        number_of_users_anonymized=4
    )

To avoid filling the database with to many log rows, set up *cron* or *scheduled* running of this:

    python manage.py ievv_opensource_logging_items_delete_older_than_last_100
    
The logs can be (with normal django and ievv setup) found at

    PROJECTDOMAIN/djangoadmin/ievv_logging/
    
which will contain a `logging event base` that contains information about the last run for each script, 
and a `logging event item` that contains information about multiple runs of 
a given script.  
