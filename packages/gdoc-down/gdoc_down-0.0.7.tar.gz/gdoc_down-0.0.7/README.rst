|PyPI package| |Documentation| |Test results| |Test coverage| |Code
analysis| |License| |Analytics|

``gdoc_down``
=============

API and command line program to save Google documents, presentations,
and worksheets in a local Google Drive / Backup & Sync directory to to
local files.

``gdoc_down`` supports several formats:

-  CSV (.csv)
-  EPUB (.epub)
-  Excel workbook (.xlsx)
-  HTML (.html)
-  Image (.png, .jpg, .svg)
-  LaTeX (.tex)
-  Open Office document (.odt)
-  Open Office presentation (.odp)
-  Open Office workbook (.ods)
-  Plain text file (.txt)
-  Portable document format (.pdf)
-  Powerpoint presentation (.pptx)
-  Rich text document (.rtf)
-  TSV (.tsv)
-  Word document (.docx)

``gdoc_down`` also has special features for handling .gdoc files that
contain LaTeX:

-  ``gdoc_down`` ignores all images. This allows the user to place
   images inside the Google document for convenience and to use
   :raw-latex:`\includegraphics `to embed images in compile PDF files.
-  ``gdoc_down`` will convert all Google document comments to PDF
   comments.
-  ``gdoc_down`` ignores all page breaks.

The first time ``gdoc_down`` is called, ``gdoc_down`` will request
access to the user's Google account. This will create a client.json file
in the users home directory (~/.gdoc\_down/client.json).

Installation
------------

-  Latest release from PyPI ``pip install gdoc_down``

-  Latest revision from GitHub
   ``pip install git+https://github.com/KarrLab/gdoc_down.git#egg=gdoc_down``

Command line usage
------------------

::

    usage: gdoc_down (sub-commands ...) [options ...] {arguments ...}

    Download a Google document, presentation, or workbook to a local file

    positional arguments:
      google_file           path to Google document, presentation, or workbook

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --format FORMAT, -f FORMAT
                            output format (csv, docx, epub, html, jpg, odft, odp,
                            ods, pdf, pptx, png, rtf, svg, tsv, tex, txt, xlsx)
      --out_path OUT_PATH, -o OUT_PATH
                            path where Google document, presentation, or workbook
                            should be downloaded
      --extension EXTENSION, -e EXTENSION
                            output extension

Examples
--------

::

    gdoc_down -f docx /path/to/Google \Drive/file.gdoc
    gdoc_down -f pptx /path/to/Google \Drive/file.gslides
    gdoc_down -f xlsx /path/to/Google \Drive/file.gsheet

Documentation
-------------

Please see the documentation at `Read the
Docs <http://docs.karrlab.org/gdoc_down>`__.

Tests
-----

``pytest`` can be used to run the tests:

::

    pytest tests

Please note that several additional packages are required for testing
(see `tests/requirements.txt <tests/requirements.txt>`__).

License
-------

The example model is released under the `MIT license <LICENSE>`__.

Development team
----------------

``gdoc_down`` was developed by `Jonathan
Karr <http://www.karrlab.org>`__ at the Icahn School of Medicine at
Mount Sinai in New York, USA.

Questions and comments
----------------------

Please contact the `Jonathan Karr <http://www.karrlab.org>`__ with any
questions or comments.

.. |PyPI package| image:: https://img.shields.io/pypi/v/gdoc_down.svg
   :target: https://pypi.python.org/pypi/gdoc_down
.. |Documentation| image:: https://readthedocs.org/projects/gdoc-down/badge/?version=latest
   :target: http://docs.karrlab.org/gdoc_down
.. |Test results| image:: https://circleci.com/gh/KarrLab/gdoc_down.svg?style=shield
   :target: https://circleci.com/gh/KarrLab/gdoc_down
.. |Test coverage| image:: https://coveralls.io/repos/github/KarrLab/gdoc_down/badge.svg
   :target: https://coveralls.io/github/KarrLab/gdoc_down
.. |Code analysis| image:: https://api.codeclimate.com/v1/badges/3c7f002e731de98c31d0/maintainability
   :target: https://codeclimate.com/github/KarrLab/gdoc_down
.. |License| image:: https://img.shields.io/github/license/KarrLab/gdoc_down.svg
   :target: LICENSE
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-86759801-1/gdoc_down/README.md?pixel

