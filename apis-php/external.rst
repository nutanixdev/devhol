External Scripts
################

We're going to use quite a few external/third-party packages in this lab.  These packages manage, amongst other things, how our application **looks**.

Because there's no need for us to write these packages ourselves, we can grab them from their original sources and simply copy them into our app.

Checking directory structure
............................

Create the following directories and files:

- **public/css**
- **public/css/ntnx.css**
- **public/css/fonts**
- **public/css/vendor**
- **public/js**
- **public/js/ntnx.js**
- **public/js/vendor**

.. code-block:: bash

  mkdir public/css
  mkdir public/css/fonts
  mkdir public/css/vendor
  mkdir public/js
  mkdir public/js/vendor

Adding packages
...............

From the URLs below, grab the relevant file, make sure the name is correct and save it into the appropriate directory.

- CSS_ - extract to **public/css/vendor**
- Javascript_ - extract to **public/js/vendor**
- Fonts_ - extract to **public/css/fonts**

**Note**: When extracting the ZIP files, ensure they are extracted **directly** to the directories above and not into subdirectories.

.. _CSS: https://github.com/nutanixdev/lab-assets/blob/master/php-lab-v1.1/resources/css-vendor.zip?raw=true
.. _Javascript: https://github.com/nutanixdev/lab-assets/blob/master/php-lab-v1.1/resources/js-vendor.zip?raw=true
.. _Fonts: https://github.com/nutanixdev/lab-assets/blob/master/php-lab-v1.1/resources/fonts.zip?raw=true

Further testing
...............

With these files in place, our application is starting to not only come together, but also starting to look a lot better.

The navigation bar and form elements at the top of the screen are now styled properly with both colours and fonts.

It's now time to dig deeper into wiring our app into the Nutanix REST APIs ...