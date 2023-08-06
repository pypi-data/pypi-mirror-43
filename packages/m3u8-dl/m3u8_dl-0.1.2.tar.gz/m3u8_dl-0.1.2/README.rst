M3u8-dl
~~~~~~~

|alt text| |alt text| |alt text|

M3u8-dl is a simple command-line util which downloads m3u8 file.

Install
~~~~~~~

.. code:: bash

    pip install m3u8-dl

Usage
~~~~~

Get the HLS Request infomation from web browser with
``Developer Tools``. Such As ``Request URL`` and ``Referer``

.. code:: bash

    # HLS_URL -> Request URL
    # OUTPUT -> such as example.ts
    m3u8-dl HLS_URL OUTPUT

If you are failed to download the stream, try it again with the options
below: - Specify the Referer with ``-r`` when you're blocked by the
website (403 forbidden) - Specify the base uri with ``-u`` when
``#EXTINF hls-720p0.ts`` has no base uri in ``output.m3u8``

You can even make it run faster by using ``-t``, which means how many
threads you want to start

For more details, check ``--help``

TODO
~~~~

Maybe I will add a ``--restore`` option in the future to recover from
the last session where the user left off so that you don't have to
redownload when the task is interrupted.

.. |alt text| image:: https://img.shields.io/pypi/v/m3u8_dl.svg
.. |alt text| image:: https://img.shields.io/travis/kedpter/m3u8_dl.svg
.. |alt text| image:: https://readthedocs.org/projects/m3u8_dl/badge/?version=latest

