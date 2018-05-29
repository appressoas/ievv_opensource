###############################################
How to release a new version of ievv_opensource
###############################################

.. note:: This assumes you have permission to release ievv_opensource to pypi.


1. Update ``ievv_opensource/version.json``.
2. Commit.
3. Tag the commit with ``<version>``.
4. Push (``git push && git push --tags``).
5. Release to pypi (``python setup.py sdist && twine upload dist/ievv-opensource-<version>.tar.gz``).
