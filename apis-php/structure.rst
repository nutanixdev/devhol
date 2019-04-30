Creating the app structure
##########################

With our system now correctly configured to run Laravel PHP applications, we can start creating the application itself.

The key components of our app are as follows.

- Our Laravel base application, created in the previous step
- A Nutanix cluster, running Acropolis 5.5 or later
- The Nutanix REST APIs. Note that this application reads local-cluster information and cluster statistics.  This dictates that we will be using API v1 and v2.0.
- A collection of third-party Javascripts and CSS that simplify front-end operations.  For those already familiar, this is primarily done using jQuery_.
- An application-specific "master" Javascript that handles the communications between the front-end and the Nutanix REST APIs.

.. _jQuery: https://jquery.com

Adding required packages
........................

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/composer.json

- From the command line, run the following commands.  This will add 3 required packages to our application's **composer.json** file.

.. code-block:: bash

    composer require laravelcollective/html:^5.0
    composer require laracasts/flash:^1.3
    composer require guzzlehttp/guzzle:~5.3

Configuring new packages
........................

With the new packages added, we need to tell Laravel how to use them.

- Open the **config/app.php** file and navigate to the **providers** section.
- Add the following lines just before the end of the **providers** section.

**You may need to add a comma after the end of current last line.**

.. code-block:: php

    Laracasts\Flash\FlashServiceProvider::class,
    Collective\Html\HtmlServiceProvider::class,

- Navigate to the **aliases** section.
- Add the following lines just before the end of the **aliases** section.

**You may need to add a comma after the end of the current last line.**

.. code-block:: php

    'Form' => Collective\Html\FormFacade::class,
    'Html' => Collective\Html\HtmlFacade::class,
    'Flash' => Laracasts\Flash\Flash::class,

Publish the 'Flash' package files
.................................

This is a Laravel function that takes installed packages and moves files into place, if it is required.

The 'Flash' package, used to show pretty messages, requires that its files are moved to specific locations within the app.

.. code-block:: bash

    php artisan vendor:publish

Creating the app controllers
............................

- Our app contains two main controllers; **HomeController** and **AjaxController**.  For now, we can create shell controllers that don't do anything (yet).  To do this, run the following commands from the app's directory.

.. code-block:: bash

    php artisan make:controller HomeController --plain
    php artisan make:controller AjaxController --plain

If you want to make sure this worked, check for the existence of files named **AjaxController** and **HomeController** in the **app/Http/Controllers** directory.

Disabling CSRF Protection
.........................

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/VerifyCsrfToken.php

**Don't do this in production!**

For our app, we don't need CSRF protection for one specific route.  CSRF protection is Laravel's built-in way of making sure a POST request is what it says it is by sending a CSRF token with that request.  If the token doesn't match, the POST request is rejected.

- Open the **app/Http/Middleware/VerifyCsrfToken.php** file
- The default configuration looks like this:

.. code-block:: php

    protected $except = [
        //
    ];

- Change the configuration to this so that CSRF protection is disabled specifically for POST requests to **/ajax/load-layout**

.. code-block:: php

    protected $except = [
        'ajax/load-layout',
    ];

The first controller method
...........................

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/HomeController.php

- Open the **app/Http/Controllers/HomeController.php** file.  It's empty right now, with a single-line comment block (**//**).  Replace the single-line comment block with the following method.

.. code-block:: php

    /**
    * Load the main view
    *
    * @return mixed
    */
    public function getIndex()
    {

      $layout = '[{"col":1,"row":1,"size_x":1,"size_y":1},{"col":1,"row":2,"size_x":1,"size_y":1},{"col":1,"row":3,"size_x":1,"size_y":1},{"col":2,"row":1,"size_x":2,"size_y":1},{"col":2,"row":2,"size_x":2,"size_y":2},{"col":4,"row":1,"size_x":1,"size_y":1},{"col":4,"row":2,"size_x":2,"size_y":1},{"col":4,"row":3,"size_x":1,"size_y":1},{"col":5,"row":1,"size_x":1,"size_y":1},{"col":5,"row":3,"size_x":1,"size_y":1},{"col":6,"row":1,"size_x":1,"size_y":1},{"col":6,"row":2,"size_x":1,"size_y":2}]';

      $source_json = json_decode( file_get_contents( base_path() . '/config/dashboard.json', true ) );

      if( $source_json->version )
      {
        $layout = base64_decode( $source_json->layout );
      }
      else
      {
        $layout = null;
      }

      return view( 'home.index' )->with( 'data', [ 'layout' => $layout ] );

    }
    /* getIndex */

This **getIndex** method is the function that will be called when someone browses to the app's root URL (**/**).  At a high level, it does the following things:

1. Sets up a default grid layout.  This layout is based on the jQuery **Gridster** plugin.
2. Loads a default layout from a file provided with the app - we will create that file shortly.
3. Using the layout information that has been created, it returns an HTML view to the user.

Default layouts
...............

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/dashboard.json

As mentioned above, a default layout is loaded when the user browses to **/**.  Let's now create that default layout.

- Inside the **config** directory, create a file named **dashboard.json**.  This file describes the application layout that will be loaded at first run.  The contents of the file should be as follows:

.. code-block:: json

    {"version":"1.0","layout":"W3siaWQiOiJjbHVzdGVyU3VtbWFyeSIsImNvbCI6MSwicm93IjoxLCJzaXplX3giOjIsInNpemVfeSI6MX0seyJpZCI6Im5vc1ZlcnNpb24iLCJjb2wiOjMsInJvdyI6MSwic2l6ZV94IjoyLCJzaXplX3kiOjF9LHsiaWQiOiJtaXNjMSIsImNvbCI6NSwicm93IjoxLCJzaXplX3giOjEsInNpemVfeSI6MX0seyJpZCI6Im1pc2MyIiwiY29sIjo2LCJyb3ciOjEsInNpemVfeCI6MSwic2l6ZV95IjoxfSx7ImlkIjoiaG9zdHMiLCJjb2wiOjEsInJvdyI6Miwic2l6ZV94IjoxLCJzaXplX3kiOjF9LHsiaWQiOiJiaWdHcmFwaCIsImNvbCI6Miwicm93IjoyLCJzaXplX3giOjIsInNpemVfeSI6Mn0seyJpZCI6InZtSW5mbyIsImNvbCI6NCwicm93IjoyLCJzaXplX3giOjIsInNpemVfeSI6MX0seyJpZCI6ImNvbnRhaW5lcnMiLCJjb2wiOjYsInJvdyI6Miwic2l6ZV94IjoxLCJzaXplX3kiOjJ9LHsiaWQiOiJibG9ja3MiLCJjb2wiOjEsInJvdyI6Mywic2l6ZV94IjoxLCJzaXplX3kiOjF9LHsiaWQiOiJoaW50cyIsImNvbCI6NCwicm93IjozLCJzaXplX3giOjIsInNpemVfeSI6MX0seyJpZCI6ImZvb3RlcldpZGdldCIsImNvbCI6MSwicm93Ijo0LCJzaXplX3giOjYsInNpemVfeSI6MX1d"}

- Inside the **resources** directory, create a subdirectory named **install**.
- Inside the new **install** directory, create a file named **dashboard-default.json**.  This file describes the application layout when it is **reverted to default**.  The contents of the file should be as follows.

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/dashboard-default.json

.. code-block:: json

    [{"id":"clusterSummary","col":1,"row":1,"size_x":2,"size_y":1},{"id":"hosts","col":1,"row":2,"size_x":1,"size_y":1},{"id":"blocks","col":1,"row":3,"size_x":1,"size_y":1},{"id":"nosVersion","col":3,"row":1,"size_x":2,"size_y":1},{"id":"bigGraph","col":2,"row":2,"size_x":2,"size_y":2},{"id":"misc1","col":5,"row":1,"size_x":1,"size_y":1},{"id":"vmInfo","col":4,"row":2,"size_x":2,"size_y":1},{"id":"hints","col":4,"row":3,"size_x":2,"size_y":1},{"id":"misc2","col":6,"row":1,"size_x":1,"size_y":1},{"id":"containers","col":6,"row":2,"size_x":1,"size_y":2},{"id":"footerWidget","col":1,"row":4,"size_x":6,"size_y":1}]

The JSON in these files will be used and explained in more detail in a later step.

The main view
.............

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/index.blade.php

Because Laravel apps are based on the MVC (Model, View, Controller) design pattern, the next thing to do is create the main view for our app.  A simple 'Welcome' view is provided with Laravel (we saw it when making sure the app works), but we are going to create one more.

**Note**: Unless mentioned otherwise, all directory paths in this lab will be based on the root of your app.

- Inside the **resources/views** directory, create a subdirectory named **home**
- Inside the new **home** directory, create a file named **index.blade.php**.  For now, the contents of **index.blade.php** should be as follows.  These contents setup the base HTML5 page, a navigation bar and include directives for our scripts and stylesheets.

.. code-block:: html

    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Nutanix Dashboard</title>
        <link rel="stylesheet" type="text/css" href="/css/vendor/reset.css" />
        <link rel="stylesheet" type="text/css" href="/css/vendor/built-in.css" />
        <link rel="stylesheet" type="text/css" href="/css/vendor/jquery-ui-custom.css" />
        <link rel="stylesheet" type="text/css" href="/css/vendor/jq.dropdown.min.css" />
        <link rel="stylesheet" type="text/css" href="/css/vendor/jq.gridster.css" />
        <link rel="stylesheet" type="text/css" href="/css/vendor/jq.jqplot.css" />
        <link rel="stylesheet" type="text/css" href="/css/ntnx.css" />
    </head>
    <body>

    <nav class="navbar navbar-default navbar-fixed-top main-nav">
        <div class="container-fluid">
            <div class="collapse navbar-collapse">

                <ul class="nav navbar-nav">

                    {!! Form::hidden( 'csrf_token', csrf_token(), [ 'id' => 'csrf_token' ] ) !!}
                    <li><a href="#">Home</a></li>
                    <li><a href="#" class="saveLayout">Save Layout</a></li>
                    <li><a href="#" class="defaultLayout">Revert to Default Layout</a></li>

                </ul>

                {!! Form::open( [ 'class' => 'navbar-form navbar-left' ] ) !!}
                    <div class="form-group">
                        {!! Form::text( 'cvmAddress', null, [ 'id' => 'cvmAddress', 'class' => 'form-control', 'placeholder' => 'Cluster/CVM IP' ] ) !!}
                        {!! Form::text( 'username', null, [ 'id' => 'username', 'class' => 'form-control', 'placeholder' => 'Cluster Username' ] ) !!}
                        {!! Form::password( 'password', [ 'id' => 'password', 'class' => 'form-control', 'placeholder' => 'Cluster Password' ] ) !!}
                        {!! Form::submit( 'Go!', [ 'id' => 'goButton', 'class' => 'btn btn-primary' ] ) !!}
                    </div>
                {!! Form::close() !!}

            </div>
        </div>
    </nav>

    <div class="container" style="margin-top: 20px;">
        <div class="row">
            <div class="col-md-15">
                <div id="status_new" class="alert alert-warning">
                    <span class="glyphicon glyphicon-time"></span>&nbsp;
                    Your session has expired.&nbsp;&nbsp;Please <a href="{{ URL::to( '/signin' ) }}" title="Sign In">sign in</a> again to continue.
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-15">
                @include( 'vendor.flash.message' )
                <div class="container">                
                    <div class="row">
                        <div class="col-md-15">

                            <div class="gridster">
                                <ul>
                                    {{-- The grid layout will end up here, once it is generated --}}
                                </ul>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div style="height: 70px; clear: both;">&nbsp;</div>

    <script src="/js/vendor/jquery-2.1.3.min.js"></script>
    <script src="/js/vendor/jq.dropdown.min.js"></script>
    <script src="/js/vendor/classie.min.js"></script>
    <script src="/js/vendor/ntnx-bootstrap.min.js"></script>
    <script src="/js/vendor/modernizr.custom.min.js"></script>
    <script src="/js/vendor/jquery.jqplot.min.js"></script>
    <script src="/js/vendor/jqplot.logAxisRenderer.js"></script>
    <script src="/js/vendor/jqplot.categoryAxisRenderer.js"></script>
    <script src="/js/vendor/jqplot.canvasAxisLabelRenderer.js"></script>
    <script src="/js/vendor/jqplot.canvasTextRenderer.js"></script>
    <script src="/js/vendor/jqplot.barRenderer.js"></script>
    <script src="/js/vendor/jquery.gridster.min.js"></script>
    <script src="/js/ntnx.js"></script>

    </body>

    </html>

Connecting the main view
........................

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/routes.php

Right now, we can't access the new home page - we need to tell Laravel how to display that page, based on the URL provided by the user.

- Open the **app/Http/routes.php** file and replace everything below the comment block, as follows:

.. code-block:: php

    Route::get( '/', 'HomeController@getIndex' );
    Route::controller( 'ajax', 'AjaxController' );

The first line instructs Laravel serve all requests **/** (the app's root directory) by running the **getIndex** method from the **HomeController** controller.
The second line instructs Laravel to serve all requests prefixed with **/ajax/** by running the matching method from the **AjaxController** controller.  We will create this controller later.

Initial app testing
...................

At this point, your application doesn't do anything useful.  However, the basic structure has been completed and we're ready to start wiring the important parts together.

For now, browse to the root of your application and make sure you can see a form prompting for the following items:

1. Cluster/CVM IP
2. Cluster username
3. Cluster password

There should also be three links at the top of the screen - **Home**, **Save Layout** and **Revert to Default Layout**.

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/unstyled.png

If you are wondering why it looks incredibly ugly right now, it's because we haven't added any styling or formatting, yet ...