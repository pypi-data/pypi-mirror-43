==============
python-foscam
==============

Python Library for Foscam IP Cameras

Getting Started
===============

Install
-------

.. code:: bash

  $ pip install python-foscam

Simple example
--------------
Here is a simple example to move camera lens up and stop after 1s.

.. code:: python

    from libpyfoscam import FoscamCamera
    from time import sleep

    mycam = FoscamCamera('192.168.0.113', 88, 'admin', 'superuser')
    mycam.ptz_move_up()
    sleep(1)
    mycam.ptz_stop_run()

Asynchronous feature
--------------------
This example uses the asynchronous feature provided by ``FoscamCamera``.

Normally, a command is sent synchronously, waiting for results and blocking the main thread.

By initializing ``FoscamCamera`` with `daemon=True` (defaults to False), commands are sent asynchronously.

.. code:: python

    mycam = FoscamCamera('192.168.0.113', 88, 'admin', 'superuser', daemon=True)
    mycam.get_ip_info()
    mycam.get_port_info()
    mycam.refresh_wifi_list()


Send command with callback
--------------------------
This example illustrates the use of a callback function when the command completes.

.. code:: python

    from libpyfoscam import FoscamCamera, FOSCAM_SUCCESS
    def print_ipinfo(returncode, params):
        if returncode != FOSCAM_SUCCESS:
            print 'Failed to get IPInfo!'
            return
        print 'IP: %s, Mask: %s' % (params['ip'], params['mask'])

    mycam = FoscamCamera('192.168.0.113', 88, 'admin', 'superuser', daemon=False)
    mycam.get_ip_info(print_ipinfo)
