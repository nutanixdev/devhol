.. _era:

---
Era
---

*The estimated time to complete this lab is 60 minutes.*

.. raw:: html

  <iframe width="640" height="360" src="https://www.youtube.com/embed/AbPMhTQ40Mw?rel=0&amp;showinfo=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Overview
++++++++

Nutanix Era is a software suite that automates and simplifies database administration – bringing One Click simplicity and invisible operations to database provisioning and lifecycle management (LCM).

With One Click database provisioning and Copy Data Management (CDM) as its first services, Nutanix Era enables DBAs to provision, clone, refresh, and backup their databases to any point in time. Line of business applications in every vertical depend on databases, providing use cases in both production and non-production environments.

**In this lab you will explore how Era can be used to standardize database deployment, allow for rapid cloning from a production database to a clone used for application development, updating that clone based on production data, and finally leveraging the REST API to understand how Era can integrate with a customer's existing automation tools.**

Lab Setup
+++++++++

This lab requires applications provisioned as part of the :ref:`windows_tools_vm`.

If you have not yet deployed this VM, see the linked steps before proceeding with the lab.

Deploying Era
+++++++++++++

Era is distributed as a virtual appliance that can be installed on either AHV or ESXi. In this lab you will deploy Era to your AHV cluster.

#. In **Prism Central**, select :fa:`bars` **> Virtual Infrastructure > VMs**.

   .. figure:: images/2a.png

#. Click **Create VM**.

#. Fill out the following fields:

   - **Name** - *Initials*-Era
   - **Description** - (Optional) Description for your VM.
   - **vCPU(s)** - 4
   - **Number of Cores per vCPU** - 1
   - **Memory** - 16 GiB

   - Select **+ Add New Disk**
       - **Type** - DISK
       - **Operation** - Clone from Image Service
       - **Image** - Era\*.qcow2
       - Select **Add**

   - Select **Add New NIC**
       - **VLAN Name** - Primary
       - Select **Add**

#. Click **Save** to create the VM.

#. Select your Era VM and click **Power On**.

Registering a Cluster
+++++++++++++++++++++

#. In **Prism Central > VMs > List**, identify the IP address assigned to your Era VM using the **IP Addresses** column.

#. Open \https://*ERA-VM-IP:8443*/ in a new browser tab.

   .. note::

     It may take up to 2 minutes for the Era interface to initialize after booting the VM.

#. Select **I have read and agree to terms and conditions** and click **Continue**.

#. Enter **techX2019!** as the **admin** password and click **Set Password**.

#. Login using the following credentials:

   - **Username** - admin
   - **Password** - techX2019!

#. On the **Welcome to Era** page, fill in the following information:

   - **Name** - *Your Cluster Name*
   - **Description** - (Optional) Description
   - **Address** - *Your Prism Element Cluster IP*
   - **Prism Element Administrator** - admin
   - **Password** - techX2019!

   .. figure:: images/3b2.png

   .. note::

     Era requires a Prism Element account with full administrator access. For ESXi clusters, vCenter must also be registered with Prism Element.

#. Click **Next**.

#. Select the **Default** storage container and click **Next**.

   .. figure:: images/3c.png

#. Select the **Primary** VLAN. This is the default network profile that Era will use when provisioning new databases. Do **not** select **Manage IP Address Pool**, as your AHV cluster already has IPAM (DHCP) configured for that network.

   .. figure:: images/3d.png

#. Click **Next**.

#. Once Era setup has completed, click **Get Started**.

   .. figure:: images/3e2.png

Provisioning a Database
+++++++++++++++++++++++

The initial release of Era supports the following Operating Systems and Database Servers:

- CentOS 6.9, 7.2, and 7.3
- Oracle Linux 7.3
- RHEL 6.9, 7.2, and 7.3
- Windows Server 2012, Windows Server 2012 R2, and Windows Server 2016
- Oracle 11.2.0.4.x, 12.1.0.2.x, and 12.2.0.1.x
- PostgreSQL 9.x and 10.x
- SQL Server 2008 R2, SQL Server 2012, SQL Server 2014, and SQL Server 2016

Era can be used to provision database servers and databases on the registered Nutanix cluster, or you can register an existing source database running on the cluster. In this lab, you will provision a new PostgreSQL database server and database.

Era makes it even simpler to provision a simple PostgreSQL database by providing sample profiles for **Software**, **Compute**, and **Database Parameters**. You will explore each of these profiles to understand how they are configured.

#. Select the **Era > Getting Started** drop down menu and click **Profiles**.

   .. figure:: images/3g.png

#. Select **Software** and note there are included profiles for **PostgreSQL 10.4** and **MariaDB 10.3** shipped with Era.

   Additional PostgreSQL, MariaDB, SQL Server, and Oracle profiles can be created by registering database server VMs with Era.

#. Select **Compute > DEFAULT_OOB_COMPUTE** and note the default Compute Profile creates a 4 core, 32GiB RAM VM to host the database. To reduce memory consumption in the shared lab environment, you will create a custom Compute Profile.

#. Click **+ Create** and fill out the following fields:

   - **Name** - Lab
   - **Description** - Lab Compute Profile
   - **vCPUs** - 1
   - **Cores per CPU** - 2
   - **Memory (GiB)** - 16

   .. figure:: images/3f2.png

#. Click **Create**.

#. Select **Database Parameters > DEFAULT_POSTGRES_PARAMS** and note the default parameters for a PostgreSQL database provisioned by Era.

#. Select the **Era > Profiles** drop down menu and click **Getting Started**.

#. On the **Getting Started** page, click the **PostgreSQL** button under **Provision a Database**.

   .. figure:: images/4b2.png

#. Click **Provision a Database**.

   .. figure:: images/4c.png

#. Select the **PostgreSQL** engine and click **Next**.

#. Fill out the following **Database Server** fields:

   - **Database Server** - Select **Create New Server**
   - **Database Server Name** - *Initials*-DBServer
   - **Compute Profile** - Lab
   - **Network Profile** - DEFAULT_OOB_NETWORK
   - **Software Profile** - POSTGRES_10.4_OOB
   - **Description** - (Optional) Description
   - **SSH Public Key for Node Access** -

   .. code-block:: text

     ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoQRdEfm8ZJNGlYLQ2iw08eVk/Wyj0zl3M5KyqKmBTpUaS1uxj0K05HMHaUNP+AeJ63Qa2hI1RJHBJOnV7Dx28/yN7ymQpvO1jWejv/AT/yasC9ayiIT1rCrpHvEDXH9ee0NZ3Dtv91R+8kDEQaUfJLYa5X97+jPMVFC7fWK5PqZRzx+N0bh1izSf8PW0snk3t13DYovHFtlTpzVaYRec/XfgHF9j0032vQDK3svfQqCVzT02NXeEyksLbRfGJwl3UsA1ujQdPgalil0RyyWzCMIabVofz+Czq4zFDFjX+ZPQKZr94/h/6RMBRyWFY5CsUVvw8f+Rq6kW+VTYMvvkv

   .. note::

     The above SSH public key is provided as an example and is configured as an authorized key for the operating system provisioned by Era. In a non-lab setting you would create your own SSH private/public keypair and provide the public key during this step.

   .. figure:: images/4d2.png

#. Click **Next**.

#. Fill out the following **Database** fields:

   - **Database Name** - *Initials*\_LabDB
   - **Description** - (Optional) Description
   - **POSTGRES Password** - techX2019!
   - **Database Parameter Profile** - DEFAULT_POSTGRES_PARAMS
   - **Listener Port** - 5432
   - **Size (GiB)** - 200

   .. note::

     Era also offers to ability to run scripts or commands both before and after database creation . These can be used to further customize an environment based on specific enterprise needs.

   .. figure:: images/4e2.png

#. Click **Next**.

#. Fill out the following **Time Machine** fields:

   - **Name** - *Initials*\_LabDB_TM
   - **Description** - (Optional) Description
   - **SLA** - Gold
   - **Schedule** - Default

   .. figure:: images/4f2.png

#. Click **Provision**.

#. Click **Operations** in the upper right-hand corner to view the provisioning progress. Provisioning should take approximately 5 minutes.

   .. note::

     All operations within Era have unique IDs are fully visible for logging/auditing.

   .. figure:: images/4g2.png

#. Upon completion, select **Dashboard** from the drop down menu and note your new **Source Database**.

   .. figure:: images/4i2.png

   You should also be able to see the *Initials*-**DBServer** VM running within Prism.

Connecting to the Database
++++++++++++++++++++++++++

Now that Era has successfully provisioned a database instance, you will connect to the instance and verify the database was created.

#. Select **Era > Databases** from the drop down menu.

#. Under **Sources**, click the name of your database.

   .. figure:: images/5a2.png

#. Note the IP Address of your **Database Server**.

   .. figure:: images/5b.png

#. Using *Initials*\ **-Windows-ToolsVM**, open **pgAdmin**.

   .. note::

     If installed, you can also use a local instance of pgAdmin. The Tools VM is provided to ensure a consistent experience.

#. Under **Browser**, right-click **Servers** and select **Create > Server...**.

   .. figure:: images/5c.png

#. On the **General** tab, provide your database server name (e.g. *Initials*-**DBServer**).

#. On the **Connection** tab, fill out the following fields:

   - **Hostname/IP Address** - *Initials*-DBServer IP Address
   - **Port** - 5432
   - **Maintenance Database** - postgres
   - **Username** - postgres
   - **Password** - techX2019!

   .. figure:: images/5d2.png

#. Expand *Initials*\ **-DBServer > Databases** and note an empty database has been created by Era.

   .. figure:: images/5h2.png

..  Now you will create a table to store data regarding Names and Ages.

  Expand *Initials*\_**labdb** **> Schemas > public**. Right-click on **Tables** and select **Create > Table**.

  .. figure:: images/5e.png

  On the **General** tab, enter **table1** as the **Name**.

  On the **Columns** tab, click **+** and fill out the following fields:

  - **Name** - Id
  - **Data type** - integer
  - **Primary key?** - Yes

  Click **+** and fill out the following fields:

  - **Name** - Name
  - **Data type** - text
  - **Primary key?** - No

  Click **+** and fill out the following fields:

  - **Name** - Age
  - **Data type** - integer
  - **Primary key?** - No

  .. figure:: images/5f.png

  Click **Save**.

  Using your **Tools VM**, open the following link to download a .CSV file containing data for your database table: http://ntnx.tips/EraTableData

  Using **pgAdmin**, right-click **table1** and select **Import/Export**.

  Toggle the **Import/Export** button to **Import** and fill out the following fields:

  - **Filename** - C:\\Users\\Nutanix\\Downloads\\table1data.csv
  - **Format** - csv

  .. figure:: images/5g.png

  Click **OK**.

  You can view the imported data by right-clicking **table1** and selecting **View/Edit Data > All Rows**.

Cloning Your PostgreSQL Source
++++++++++++++++++++++++++++++

Now that you have created a source database, you can easily clone it using Era Time Machine. Database clones are helpful for development and testing purposes, allowing non-production environments to utilize product data without impacting production operations. Era clones utilize Nutanix-native copy-on-write cloning technology, allowing for zero-byte database clones. This space efficiency can significantly lower storage costs for environments supporting large numbers of database clones.

#. In **Era > Time Machines**, select the Time Machine instance for your source database.

   .. figure:: images/16a2.png

#. Click **Snapshot** and enter **First** as the **Snapshot Name**.

   .. figure:: images/17a.png

#. Click **Create**.

   You can monitor the **Create Snapshot** job in **Era > Operations**.

   .. figure:: images/18a2.png

#. After the snapshot job completes, select the Time Machine instance for your source database in **Era > Time Machines** and click **Clone Database**.

#. On the **Time** tab, select **Snapshot > First**.

   .. note::

     Without creating manual snapshots, Era also offers the ability to clone a database based on **Point in Time** increments including Continuous (Every Second), Daily, Weekly, Monthly, or Quarterly. Availability is controlled by the SLA of the source.

   .. figure:: images/19a2.png

#. Click **Next**.

#. On the **Database Server** tab, fill out the following fields:

   - **Database Server** - Create New Server
   - **VM Name** - *Initials*-DBServer-Clone
   - **Compute Profile** - Lab
   - **Network Profile** - DEFAULT_OOB_NETWORK
   - **SSH Public Key** -

   .. code-block:: text

     ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoQRdEfm8ZJNGlYLQ2iw08eVk/Wyj0zl3M5KyqKmBTpUaS1uxj0K05HMHaUNP+AeJ63Qa2hI1RJHBJOnV7Dx28/yN7ymQpvO1jWejv/AT/yasC9ayiIT1rCrpHvEDXH9ee0NZ3Dtv91R+8kDEQaUfJLYa5X97+jPMVFC7fWK5PqZRzx+N0bh1izSf8PW0snk3t13DYovHFtlTpzVaYRec/XfgHF9j0032vQDK3svfQqCVzT02NXeEyksLbRfGJwl3UsA1ujQdPgalil0RyyWzCMIabVofz+Czq4zFDFjX+ZPQKZr94/h/6RMBRyWFY5CsUVvw8f+Rq6kW+VTYMvvkv

   .. figure:: images/20a2.png

#. Click **Next**.

#. On the **Database Server** tab, fill out the following fields:

   - **Name** - *Initials*\_LabDB_Clone
   - **Description** - (Optional) Description
   - **Password** - techX2019!
   - **Database Parameter Profile** - DEFAULT_POSTGRES_PARAMS

   .. figure:: images/21a2.png

#. Click **Clone**.

   The cloning process will take approximately the same amount of time as provisioning the original database and can be monitored in **Era > Operations**.

   While waiting for the clone to complete, explore **Era > SLAs** to understand the differences between standard SLAs offered by Era, or create your own custom SLA.

   .. figure:: images/21b.png

#. Following the completion of the clone operation, you can connect to the clone instance as described in the previous section, `Connecting to the Database`_.

   .. figure:: images/23a2.png

   The newly provisioned clone is now ready to be used.

Refreshing A Cloned Database
++++++++++++++++++++++++++++

The ability to easily refresh a cloned database using new data from the source database improves development, test, and other use cases by ensuring they have access to new and relevant data. In this section you will add a new table for storing data to your source database, and refresh the existing clone.

#. In **pgAdmin**, select your source database (**NOT** the cloned database), and from the menu bar click **Tools > Query Tool**.

   .. figure:: images/25a2.png

#. From the **Query Tool**, type the following SQL command into the editor:

   .. code-block:: postgresql
     :name: products-table-sql

     CREATE TABLE products (
     product_no integer,
     name text,
     price numeric
     );

#. Click :fa:`bolt` **Execute/Refresh**.

   .. figure:: images/26a.png

#. Verify the creation of the table under **Schemas > Public > Tables > products**.

   .. note::

     You may need to refresh **Tables** for the newly created table to appear.

   .. figure:: images/27a2.png

   Previously you created a manual snapshot on which to base your cloned database, for the refresh you will leverage the **Point in Time** capability of Era.

   The default schedule for **Log Catch Up**, configured when provisioning the source database, is every 30 minutes. Based on this schedule, you should expect to be able to refresh the database based on updates older than 30 minutes with no further action required.

   In this case, you just created the **products** table in your source database, so a manual execution of **Log Catch Up** would be required to copy transactional logs to Era from your source database.

#. In **Era > Time Machines**, select the Time Machine instance for your source database and click **Log Catch Up > Yes**.

   .. figure:: images/27c.png

#. Once the **Log Catchup** job completes, in **Era > Databases > Clones**, select the clone of your source database and click **Refresh**.

   .. figure:: images/27b2.png

#. Refreshing to the latest available **Point in Time** is selected by default. Click **Refresh**.

   .. figure:: images/27d.png

#. Observe the steps taken by Era to refresh the cloned database in **Operations**.

   .. figure:: images/27e.png

#. Once the **Refresh Clone** job is complete, refresh the **Tables** view of your clone database in **pgAdmin** and confirm the **products** table is now present.

   .. figure:: images/28a2.png

   In just a couple of clicks and minutes you were able to update your cloned database using the latest available production data. This same approach could be leveraged to recover absent data from a database by provisioning a clone based on a previous snapshot or point in time.

#. Return to the **Dashboard** and review the critical information Era provides to administrators, including storage savings, clone aging, tasks, and alerts.

   .. figure:: images/28b2.png

Using the Era REST API Explorer
+++++++++++++++++++++++++++++++

Era features an "API first" architecture and provides a fully documented REST API to allow for automation and orchestration of its functions through external tools. Similar to Prism, Era also provides a Rest API Explorer to easily discover and test API functions.

#. From the menu bar, select **Admin > REST API Explorer** from the top right.

   .. figure:: images/29.png

#. Expand the different categories to view the available operations, including registering Nutanix clusters, registering and provisioning databases, cloning and refreshing databases, updating profiles and SLAs, and getting operation and alert information.

#. As a simple test, expand **Databases > GET /databases**.

   This function returns JSON containing details regarding all registered and provisioned databases and requires no additional parameters.

#. Click **Try it out > Execute**.

   .. figure:: images/30.png

   You should receive a JSON response body similar to the image below.

   .. figure:: images/32.png

   This API can be used to create powerful workflows using tools like Nutanix Calm, ServiceNow, Ansible, or others. As an example you could provision a Calm blueprint containing the web tier of an application and use a Calm eScript to invoke Era to clone an existing database and return the IP of the newly provisioned database to Calm.

Takeaways
+++++++++

What are the key things you should know about **Nutanix Era**?

- Era supports Oracle, SQL Server, PostgreSQL, and MariaDB.

- Era supports One Click operations for registering, provisioning, cloning and refreshing supported databases.

- Era enables the same type of simplicity and operating efficiency that you would expect from a public cloud while allowing DBAs to maintain control.

- Era automates complex database operations – slashing both DBA time and the cost of managing databases with traditional technologies and saving immensely on enterprise OpEx.

- Era enables database admins to standardize their database deployments across database engines and automatically incorporate database best practices.

- Era enable DBAs to clone their environments to the latest application-consistent transaction.

- Era provides a REST API to allow for integration with other orchestration and automation tools.

- Era can easily be demoed using the http://demo.nutanix.com environment.

Cleanup
+++++++

.. raw:: html

  <strong><font color="red">Once your lab completion has been validated, PLEASE do your part to remove any unneeded VMs to ensure resources are available for all users on your shared cluster.</font></strong>

**IF** you **DO NOT** intend on completing either the :ref:`cloud_native_lab` or :ref:`calm_win` labs, **THEN** you should delete the *Initials*-**Era**, *Initials*-**DBServer**, and *Initials*-**DBServer-Clone** VMs deployed as part of this exercise.

**IF** you **DO** intend on completing either the :ref:`cloud_native_lab` or :ref:`calm_win` labs, **THEN** you should only delete the *Initials*-**DBServer** and *Initials*-**DBServer-Clone** VMs deployed as part of this exercise. Both VMs should be removed via the Era web interface but will still need to be powered off and deleted through Prism.


Getting Connected
+++++++++++++++++

Have a question about **Nutanix Era**? Please reach out to the resources below:

+---------------------------------------------------------------------------------------------------+
|  Era Product Contacts                                                                             |
+============================================+======================================================+
|  Slack Channel                             |  #era                                                |
+--------------------------------------------+------------------------------------------------------+
|  Product Manager                           |  Jeremy Launier, jeremy.launier@nutanix.com          |
+--------------------------------------------+------------------------------------------------------+
|  Product Marketing Manager                 |  Maryam Sanglaji, maryam.sanglaji@nutanix.com        |
+--------------------------------------------+------------------------------------------------------+
|  Technical Marketing Engineer              |  Mike McGhee, michael.mcghee@nutanix.com             |
+--------------------------------------------+------------------------------------------------------+
|  Engineering                               |                                                      |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect Americas - Era        |  Murali Sriram, murali.sriram@nutanix.com            |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect Americas - Oracle/Era |  Mandar Surkund, mandar.surkund@nutanix.com          |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect Americas - SQL/Era    |  Mike Matthews, mike.matthews@nutanix.com            |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect APAC - Oracle/Era     |  Kim Hock Cheok, kimhock.cheok@nutanix.com           |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect APAC - Oracle/Era     |  Predee Kajonpai, predee.kajonpa@nutanix.com         |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect EMEA - Oracle/Era     |  Olivier Parcollet, olivier.parcollet@nutanix.com    |
+--------------------------------------------+------------------------------------------------------+
|  Solutions Architect EMEA - Oracle/Era     |  Karsten Zimmermann, karsten.zimmermann@nutanix.com  |
+--------------------------------------------+------------------------------------------------------+
