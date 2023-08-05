Remotsy python library |Build Status| |Codacy Badge|
====================================================

`Remotsy <https://www.remotsy.com>`_ is an infrared blaster device, is cloud controlled,
this a Python library to control the Remotsy device via Rest API.

Installation
============

  $ pip install remotsylib3

Example
========

.. code-block:: python

  from remotsylib3.api_async import (API, run_remotsy_api_call)

    if __name__ == "__main__":

        client = API()

        #Do the login and get the token
        token = run_remotsy_api_call(client.login(args.username, args.password))

        #Get the list of the controls
        lst_ctl = run_remotsy_api_call(client.list_controls())
        for ctl in lst_ctl:
            print("id %s Name %s" % (ctl["_id"], ctl['name']))


Authentication
==============

You can use your remotsy username and password, but for security is recomended to generate
a application password, logon in https://home.remotsy.com and use the option App Passwords.


Documentation API
-----------------

The API documentation and links to additional resources are available at
https://www.remotsy.com/help

.. |Build Status| image:: https://travis-ci.org/jorgecis/RemotsyLib3.svg?branch=master
   :target: https://travis-ci.org/jorgecis/RemotsyLib3
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/79fb3255b464442983bb5b6b6fdecd98
   :target: https://app.codacy.com/app/jorgecis/RemotsyLib3?utm_source=github.com&utm_medium=referral&utm_content=jorgecis/RemotsyLib3&utm_campaign=Badge_Grade_Settings

