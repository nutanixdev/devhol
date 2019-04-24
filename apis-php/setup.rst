Lab Setup
#########

Project Location
................

You can put the project files anywhere you like.  If you are running this lab in a Nutanix Frame environment, the c:\developer folder has already been created for you to use.

For those following this lab outside of Nutanix frame, the following commands can be used to setup the project structure.

.. figure:: images/linux_logo_32x32.png
.. figure:: images/osx_logo_32x32.png

.. code-block:: bash

  mkdir -p ~/developer/api-app-lab-<your_initials>
  cd ~/developer/api-app-lab-<your_initials>

.. figure:: images/windows_logo_32x32.png

.. code-block:: bash

  cd %HOMEPATH%
  mkdir developer
  cd developer

Preprepared Scripts
...................

Many scripts and files throughout this lab have been prepared and stored in our Nutanix Developer Github repository.

Throughout this lab, raw source files will be shown as per the example below:

.. note::

  **Raw source file for this section, if required:** https://fakeurl.com/FakeFile404.php

In order for this lab to be successful, you will first need to install a base Laravel application.

To complete this step, ensure you have PHP Composer installed and that is functioning correctly.  A quick test is to run the following command.

.. code-block::

  composer --version

Now we can install the base application.  All dependencies are taken care of during this process.

- From a command prompt, run the following command.  Make sure you replace **<your_initials>** with your actual initials.  For example ...

.. code-block:: bash

  composer create-project laravel/laravel="5.1.*" api-app-lab-<your_initials>

.. note::

  Laravel version 5.1 is reasonably old but has been selected for compatibility with older systems that may not have PHP7 available.

- Change to the new application's folder:

.. figure:: images/linux_logo_32x32.png
.. figure:: images/osx_logo_32x32.png

.. code-block:: bash

  cd ~/developer/api-app-lab-<your initials>

.. figure:: images/windows_logo_32x32.png

.. code-block:: bash

  cd c:\developer\api-app-lab-<your initials>
 
- Run the following command.  This will make sure all required Laravel packages are installed.

.. code-block:: bash
    
    composer update

- Run the following command.  This will generate an application key, something that is required for Laravel session management.

.. code-block:: bash

    php artisan key:generate

- Run the following command.  The 'artisan' commands are provided with Laravel and simplify the creation of models/classes, views (etc) along with many application management features.  This command will start a local

.. code-block:: bash

    php artisan serve

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/artisan_serve.png

- Test the application by browsing to http://localhost:8000.  If your system already has a service or application listening on port 8000, you can change the port PHP listens on by modifying the command as follows:

.. code-block:: bash

    php artisan serve --port=<port>

If you see the Laravel default page, your base application has been installed successfully.  The default page, at the time of writing this lab, displays the Laravel logo.

You can now continue to the next part of this lab - the app itself.