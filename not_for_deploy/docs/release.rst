###############################################
How to release a new version of ievv_opensource
###############################################

.. note:: This assumes you have permission to release ievv_opensource to pypi.


1. Update ``ievv_opensource/version.json``.
2. Add releasenote to releasenotes folder on root with name `releasenotes-<major-version>.md`.
3. Commit.
4. Tag the commit with ``<version>``.
5. Push (``git push && git push --tags``).
6. Release to pypi (``python setup.py sdist && twine upload dist/ievv_opensource-<version>.tar.gz``).
