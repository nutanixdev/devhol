********************************
API App Lab - Partially Complete
********************************

For those that only wish to go through the API "wiring up" sections, a partially-complete version of the application has been prepared for you.

**If you prefer to setup the entire application (a better learning experience) or have arrived here from the setup step, please skip this section and continue by clicking the button at the bottom of this page.**

To install and use this version, follow the steps below.

1. Clone the repository by running the following command:

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/windows_logo_32x32.png

.. code-block:: bash

  git clone https://github.com/digitalformula/dev-rel-demo-test.git

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/linux_logo_32x32.png
.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/osx_logo_32x32.png

.. code-block:: bash

  git clone git@github.com:digitalformula/dev-rel-demo-test.git

2. Checkout the partially-complete version by running the following command:

.. code-block:: bash

    git checkout 9092eed007007c48d6a1f77a52239ecc75e768c3

3. Create a new branch of the source so that you can commit your changes later.  Change **<your_initials>** to match your own initials.

.. code-block:: bash

    git checkout -b api-app-lab-<your_initials>

4. Make sure the packages are up-to-date:

.. code-block:: bash

    composer update

5. Copy the default environment configuration for use with the app (using Windows Explorer, if required)

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/windows_logo_32x32.png

.. code-block:: bash

  copy .env.example .env

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/linux_logo_32x32.png
.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/osx_logo_32x32.png

.. code-block:: bash

  cp .env.example .env

6. Generate an application key:

.. code-block:: bash

    php artisan key:generate

7. Publish the error message package's files:

.. code-block:: bash

    php artisan vendor:publish

8. Set global read/write permissions on the temporary storage folders (Everyone:Read/Write in Windows):

.. codce-block:: bash

    chmod -R 777 ./storage

With this parially-complete version of the application available, we can continue with the most important part - connecting the app to the Nutanix REST APIs.