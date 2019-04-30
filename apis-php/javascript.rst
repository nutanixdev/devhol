Creating the JavaScript
#######################

The final and probably most important file is **ntnx.js**.  For our app, it could be looked at as the interface between the user's browser and the **AjaxController.php** class created in the previous section.

While it's true that JavaScript can be used for a server-side functions via Node.js/NPM plus many others, we aren't using that in our app.

To ensure everything is modular and easy to modify later, the **ntnx.js** JavaScript has been written in a way that allows it to be easy to read.

- Make sure a file named **ntnx.js** exists in the **public/js** directory.  This file should exist as we created this class earlier.
- The contents of the **ntnx.js** file should be as follows:

.. note::

  **Raw source file for this section, if required:** https://raw.githubusercontent.com/nutanixdev/lab-assets/master/php-lab-v1.1/ntnx.js

.. raw:: html

  <strong><font color="red">Important note: The ntnx.js file is reasonably long.  Please create it first, then we'll look at what it does.</font></strong><br>

.. code-block:: JavaScript

    var NtnxDashboard;
    NtnxDashboard = {

        init: function ( config )
        {
            this.config = config;
            this.setupGridster();
            this.setUI();
            this.bindEvents();

            /* load the saved/default dashboard when the DOM is ready */
            $( document).ready( function() {

                NtnxDashboard.loadLayout();

            });

        },
        /* init */

        resetCell: function( cell )
        {
            $( '#' + cell ).html( '<span class="gs-resize-handle gs-resize-handle-both"></span>' );
        },

        physicalInfo: function( token, cvmAddress, username, password )
        {
            physicalData = $.ajax({
                url: '/ajax/physical-info',
                type: 'POST',
                dataType: 'json',
                data: { _token: token, _cvmAddress: cvmAddress, _username: username, _password: password },
            });

            physicalData.success( function(data) {
                NtnxDashboard.resetCell( 'hosts' );
                $( '#hosts' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">' + data.hostCount + ' Hosts</div>' );
                $( '#hosts' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">' + data.hostSerials + '</div>' );
            });

            physicalData.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });
        },

        vmInfo: function( token, cvmAddress, username, password )
        {

            vmData = $.ajax({
                url: '/ajax/vm-info',
                type: 'POST',
                dataType: 'json',
                data: { _token: token, _cvmAddress: cvmAddress, _username: username, _password: password },
            });

            vmData.success( function(data) {
                NtnxDashboard.resetCell( 'vmInfo' );
                $( '#vmInfo' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">VM(s)</div><div>' + data.vmCount + '</div><div></div>');
            });

            vmData.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });
        },

        clusterInfo: function( token, cvmAddress, username, password )
        {

            clusterInfo = $.ajax({
                url: '/ajax/cluster-info',
                type: 'POST',
                dataType: 'json',
                data: { _token: token, _cvmAddress: cvmAddress, _username: username, _password: password },
            });

            clusterInfo.success( function(data) {
                NtnxDashboard.resetCell( 'nosVersion' );
                $( '#nosVersion' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">NOS</div><div>' + data.results.version + '</div><div></div>');

                NtnxDashboard.resetCell( 'clusterSummary' );
                $( '#clusterSummary' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Cluster</div><div>' + data.results.name + '</div><div></div>');

                NtnxDashboard.resetCell( 'blocks' );
                $( '#blocks' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Hypervisors</div>' );
                $( '#blocks' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">' );

                $( data.results.hypervisorTypes ).each( function( index, item ) {
                    switch( item )
                    {
                        case 'kKvm':
                            $( '#blocks' ).append( 'AHV' );
                            break;
                        case 'kVMware':
                            $( '#blocks' ).append( 'ESXi' );
                            break;
                        case 'kHyperv':
                            $( '#blocks' ).append( 'Hyper-V' );
                            break;
                    }
                });

                $( '#blocks' ).append( '</div' );

            });

            clusterInfo.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });

        },

        containerInfo: function( token, cvmAddress, username, password ) {

            /* AJAX call to get some container stats */
            request = $.ajax({
                url: '/ajax/container-info',
                type: 'POST',
                dataType: 'json',
                data: { _token: token, _cvmAddress: cvmAddress, _username: username, _password: password },
            });

            request.success( function(data) {
                var plot1 = $.jqplot ('controllerIOPS', data.stats, {
                    title: 'Controller Average I/O Latency',
                    animate: true,
                    axesDefaults: {
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        tickOptions: {
                            showMark: false,
                            show: true,
                        },
                        showTickMarks: false,
                        showTicks: false
                    },
                    seriesDefaults: {
                        rendererOptions: {
                            smooth: false
                        },
                        showMarker: false,
                        fill: true,
                        fillAndStroke: true,
                        color: '#b4d194',
                        fillColor: '#b4d194',
                        fillAlpha: '0.3',
                        // fillColor: '#bfde9e',
                        shadow: false,
                        shadowAlpha: 0.1,
                    },
                    axes: {
                        xaxis: {
                            min: 5,
                            max: 120,
                            tickOptions: {
                                showGridline: true,
                            }
                        },
                        yaxis: {
                            tickOptions: {
                                showGridline: false,
                            }
                        }
                    }
                });

                NtnxDashboard.resetCell( 'containers' );
                $( '#containers' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Container(s)</div><div>' + data.containerCount + '</div><div></div>');

            });

            request.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });

        },

        removeGraph: function( token ) {
            var gridster = $( '.gridster ul' ).gridster().data( 'gridster' );
            var element = $( '#bigGraph' );
            gridster.remove_widget( element );
        },

        restoreDefaultLayout: function( token ) {
            var gridster = $( '.gridster ul' ).gridster().data( 'gridster' );
            gridster.remove_all_widgets();

            /* AJAX call to get the default layout from the system's default dashboard */
            request = $.ajax({
                url: '/ajax/load-default',
                type: 'POST',
                dataType: 'json',
                data: { _token: token },
            });

            request.success( function(data) {
                serialization = Gridster.sort_by_row_and_col_asc( JSON.parse( data.layout ) );
                $.each( serialization, function() {
                    gridster.add_widget('<li id="' + this.id + '" />', this.size_x, this.size_y, this.col, this.row);
                });

                NtnxDashboard.resetCell( 'footerWidget' );
                $( 'li#footerWidget' ).addClass( 'panel' ).append( '<div class="panel-body"><div id="controllerIOPS" style="height: 150px; width: 1000px; text-align: center;"></div></div>' );
                $( '#status_new' ).html( 'Default layout restored. Don\'t forget to save!' ).removeClass().addClass( 'alert' ).addClass( 'alert-warning' ).slideDown( 300 );
            });

            request.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });

        },

        serializeLayout: function( token ) {
            var gridster = $( '.gridster ul' ).gridster().data( 'gridster' );
            var json = gridster.serialize();
            $( '#serialized' ).html( JSON.stringify( json ) );
        },

        saveLayout: function( token ) {
            /* get the gridster object */
            var gridster = $( '.gridster ul' ).gridster().data( 'gridster' );
            /* serialize the current layout */
            var json = gridster.serialize();

            /* convert the layout to json */
            var serialized = JSON.stringify( json );

            /* AJAX call to save the layout the app's configuration file */
            request = $.ajax({
                url: '/ajax/save-to-json',
                type: 'POST',
                dataType: 'json',
                data: { _token: token, _serialized: serialized },
            });

            request.success( function(data) {
                $( '#status_new' ).removeClass().html( 'Dashboard saved!' ).addClass( 'alert' ).addClass( 'alert-success' ).slideDown( 300 ).delay( 2000 ).slideUp( 300 );
            });

            request.fail(function ( jqXHR, textStatus, errorThrown )
            {
                $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
            });

        },

        s4: function()
        {
            return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
        },

        loadLayout: function()
        {
            request = $.ajax({
                url: '/ajax/load-layout',
                type: 'POST',
                dataType: 'json',
                data: {},
            });

            var cvmAddress = $( '#cvmAddress' ).val();
            var username = $( '#username' ).val();
            var password = $( '#password' ).val();

            request.success( function( data ) {
                var gridster = $( '.gridster ul' ).gridster().data( 'gridster' );
                var serialization = JSON.parse( data.layout );

                // $( '#serialized' ).html( data.layout );

                serialization = Gridster.sort_by_row_and_col_asc(serialization);
                $.each( serialization, function() {
                    // gridster.add_widget('<li id="' + this.id + '"><div class="panel"><div class="panel-body"></div></div></li>', this.size_x, this.size_y, this.col, this.row);
                    gridster.add_widget('<li id="' + this.id + '" />', this.size_x, this.size_y, this.col, this.row);
                });

                /* add the chart markup to the largest containers */
                // $( 'li#bigGraph' ).addClass( 'panel' ).append( '<div class="panel-body"><div id="chartdiv" style="height: 330px; width: 330px; text-align: center;"></div></div>' );
                $( 'li#footerWidget' ).addClass( 'panel' ).append( '<div class="panel-body"><div id="controllerIOPS" style="height: 150px; width: 1000px; text-align: center;"></div></div>' );

                NtnxDashboard.resetCell( 'bigGraph' );
                $( '#bigGraph' ).addClass( 'info_hilite' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Hey ...</div><div>Enter your cluster details above, then click the Go button ...</div>');
                $( '#hints' ).addClass( 'info_hilite' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Also ...</div><div>Drag &amp; Drop<br>The Boxes</div>');

            });

            request.fail(function ( jqXHR, textStatus, errorThrown )
            {
                /* Display an error message */
                alert( 'Unfortunately an error occurred while processing the request.  Status: ' + textStatus + ', Error Thrown: ' + errorThrown );
            });
        },

        setupGridster: function ()
        {
            $( function ()
            {

                var gridster = $( '.gridster ul' ).gridster( {
                    widget_margins: [ 10, 10 ],
                    widget_base_dimensions: [ 170, 170 ],
                    max_cols: 10,
                    autogrow_cols: true,
                    resize: {
                        enabled: true
                    },
                    draggable: {
                        stop: function( e, ui, $widget ) {
                            $( '#status_new' ).html( 'Your dashboard layout has changed. Don\'t forget to save!' ).removeClass().addClass( 'alert' ).addClass( 'alert-warning' ).slideDown( 300 );
                        }
                    },
                    serialize_params: function ($w, wgd) {

                        return {
                            /* add element ID to data*/
                            id: $w.attr('id'),
                            /* defaults */
                            col: wgd.col,
                            row: wgd.row,
                            size_x: wgd.size_x,
                            size_y: wgd.size_y
                        }

                    }
                } ).data( 'gridster' );

            } );
        },

        setUI: function ()
        {

            // $( 'input#date' ).datepicker();

            $( 'div.alert-success' ).delay( 3000 ).slideUp( 1000 );
            $( 'div.alert-info' ).delay( 3000 ).slideUp( 1000 );

            $(function () {
                $('[data-toggle="tooltip"]').tooltip()
            })

        },
        /* setUI */

        bindEvents: function()
        {

            var self = NtnxDashboard;

            $( '#goButton' ).on( 'click', function ( e ) {

                var cvmAddress = $( '#cvmAddress' ).val();
                var username = $( '#username' ).val();
                var password = $( '#password' ).val();

                if( ( cvmAddress == '' ) || ( username == '' ) || ( password == '' ) )
                {
                    NtnxDashboard.resetCell( 'bigGraph' );
                    $( '#bigGraph' ).addClass( 'info_error' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Awww ...</div><div>Did you forget to enter something?</div>');
                }
                else
                {
                    NtnxDashboard.resetCell( 'bigGraph' );
                    $( '#bigGraph' ).html( '<span class="gs-resize-handle gs-resize-handle-both"></span>' ).removeClass( 'info_hilite' ).removeClass( 'info_error' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Ok ...</div><div>Let\'s test your cluster details ...</div>');
                    NtnxDashboard.resetCell( 'hints' );
                    $( '#hints' ).html( '<span class="gs-resize-handle gs-resize-handle-both"></span>' ).addClass( 'info_hilite' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">Also ...</div><div>Drag &amp; Drop<br>The Boxes</div>');

                    NtnxDashboard.clusterInfo( $( '#csrf_token' ).val(), cvmAddress, username, password );
                    NtnxDashboard.physicalInfo( $( '#csrf_token' ).val(), cvmAddress, username, password );
                    NtnxDashboard.vmInfo( $( '#csrf_token' ).val(), cvmAddress, username, password );
                    NtnxDashboard.containerInfo( $( '#csrf_token' ).val(), cvmAddress, username, password );
                }

                e.preventDefault();
            });

            $( '.serializeLayout' ).on( 'click', function( e ) {
                NtnxDashboard.serializeLayout( $( '#csrf_token' ).val() );
                e.preventDefault();
            });

            $( '.saveLayout' ).on( 'click', function( e ) {
                NtnxDashboard.saveLayout( $( '#csrf_token' ).val() );
                e.preventDefault();
            });

            $( '.defaultLayout' ).on( 'click', function( e ) {
                NtnxDashboard.restoreDefaultLayout( $( '#csrf_token' ).val() );
                e.preventDefault();
            });

            $( '.removeGraph' ).on( 'click', function( e ) {
                NtnxDashboard.removeGraph( $( '#csrf_token' ).val() );
                e.preventDefault();
            });

            $( '.containerStats' ).on( 'click', function( e ) {
                NtnxDashboard.containerInfo( $( '#csrf_token' ).val(), $( '#cvmAddress' ).val(), $( '#username' ).val(), $( '#password' ).val() );
                e.preventDefault();
            });

            $( '.testButton' ).on( 'click', function( e ) {
                $( '#clusterSummary' ).html( 'Hello' );
                e.preventDefault();
            });

        },
        /* bindEvents */

    };

    NtnxDashboard.init({

    });

What does the **ntnx.js** script do?  The functions of **ntnx.ns**, in load-time order, are as follows.

1. Initialises the user interface via the **init** function.
2. Create an instance of the jQuery **gridster** plugin class and configures the properties of that instance.  For our app, we are setting things like the element margins, the number of columns and telling the elements they are "draggable".
3. Altering small number of UI elements so they appear correctly.
4. Binding the user interface events to other functions within **ntnx.js**.  This is a critical step as it instructs the browser and the JavaScript what to do when "something" happens.  For example, which part of the script should execute when a user enters cluster info and clicks the "Go!" button?

Loading the UI
..............

This final load-time action has been split into its own small section as it essentially controls what the user sees upon loading the app.

1. An AJAX POST request is made to the **/ajax/load-layout** PHP method.
2. The **/ajax/load-layout** request loads the default layout from the **/config/dashboard.json** file we created earlier.
3. The contents of **/config/dashboard.json** are parsed and the individual UI elements ("boxes") are created.
4. Finally, CSS classes are added to the new UI elements, e.g. setting background colour and font-size.

JavaScript functions
....................

The other functions within **ntnx.js** are only executed when specific events are fired.  Let's look at the **physicalInfo** function in more detail now.

The **physicalInfo** function is as follows (you've already added it to your **ntnx.js** script):

.. code-block:: JavaScript

    physicalInfo: function( token, cvmAddress, username, password )
    {
        physicalData = $.ajax({
            url: '/ajax/physical-info',
            type: 'POST',
            dataType: 'json',
            data: { _token: token, _cvmAddress: cvmAddress, _username: username, _password: password },
        });

        physicalData.success( function(data) {
            NtnxDashboard.resetCell( 'hosts' );
            $( '#hosts' ).addClass( 'info_big' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">' + data.hostCount + ' Hosts</div>' );
            $( '#hosts' ).append( '<div style="color: #6F787E; font-size: 25%; padding: 10px 0 0 0;">' + data.hostSerials + '</div>' );
        });

        physicalData.fail(function ( jqXHR, textStatus, errorThrown )
        {
            $( '#status_new' ).removeClass().html( textStatus + ' - ' + errorThrown ).addClass( 'alert' ).addClass( 'alert-error' );
        });
    },

Going through this function, we can see it does the following things.

1. An AJAX POST request is made to the **/ajax/physical-info** PHP method (we'll also look at that shortly).
2. If the request was successful, the results of the AJAX request are parsed.
3. The parsed data is dynamically shown in the app UI via the jQuery **.append** method.

The **/ajax/physical-info** method is as follows.

.. code-block:: php

    public function postPhysicalInfo()
    {
        $parameters = [ 'username' => $_POST[ '_username' ], 'password' => $_POST[ '_password' ], 'cvmAddress' => $_POST[ '_cvmAddress' ], 'objectPath' => 'hosts' ];

        $physical = ( new ApiRequest( new ApiRequestParameters( $parameters ) ) )->doApiRequest();

        $hostCount = $physical[ 'metadata' ][ 'grand_total_entities' ];

        $hostSerials = '';

        foreach( $physical[ 'entities' ] as $host )
        {
            $hostSerials = $hostSerials . 'S/N&nbsp;' . $host[ 'serial' ] . '<br>';
        }

        return response()->json( [ 'hostCount' => $hostCount, 'hostSerials' => $hostSerials ] );
    }

The first thing to note is the name of the method within **/app/Http/Controllers/AjaxController.php**.  The **postPhysicalInfo** name is how Laravel identifies that the only way the method can be called is via an HTTP POST request, with the following camel-case "words" instructing PHP how to refer to that method.

In this example, **postPhysicalInfo** is called via POST request to **physical-info**.

Going through this method, we can see it does the following things.

1. Creates an array containing a number of variables e.g. cluster username & password, the IP address of the cluster or CVM and the API endpoint we want to query.
2. An instance of our **ApiRequest** class is created, with an instance of our **ApiRequestParameters** class passed to the **ApiRequest** constructor.
3. Using method-chaining (**->** in PHP), we are then calling **doApiRequest** to execute the actual request.
4. Parses the results of the request found in the request's **metadata/grand_total_entities** property to find out how many hosts are in our cluster.
5. Loops through the list of hosts and prepares to dynamically shows the serial number in the app UI via the jQuery **.append** method.
6. Returns all the above info in JSON format, ready for our JavaScript to process.

Most of the other functions in **ntnx.js** work the exact same way.  They prepare the request parameters, create and execute the request, then pass the results back to **ntnx.js** for showing in the UI.

Final Testing
.............

With all our classes, JavaScript, views and styling files in place, the app should now be ready to test!

1. Ensure your local web server is running by running the following command, if it isn't already running.

.. code-block:: bash

    php artisan serve

2. If using the default port, browse to **http://localhost:8000**.
3. If everything has been setup correctly, you'll see a collection of UI elements ("boxes") displayed on the screen, with fields at the top for cluster/CVM IP address, username and password.

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/ui_loaded.png

4. Enter your cluster/CVM IP address, username and password, then click the "Go!" button.
5. If everything has been setup correctly, you should see the app load as shown below.

.. figure:: https://s3-ap-southeast-2.amazonaws.com/lab.digitalformula.net/images/dev-rel-demo/request_completed.png