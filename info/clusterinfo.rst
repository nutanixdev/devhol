.. role:: html(raw)
   :format: html

.. _clusterinfo:

--------------------
Your Cluster Details
--------------------

.. _clusterassignments:

Cluster Assignments
+++++++++++++++++++

Refer to **YOUR NAME** in the table below for all critical environmental information, including IP addresses that you will use to complete the self-paced labs.

**Please ensure you are using ONLY the cluster details you have been assigned in order to not create issues for other participants. When prompted during a lab, you will create resources using YOUR OWN initials (or name) to avoid duplicate, confusing resource names. For example, if your name is Dheeraj Danger Pandey, and you were creating a VM called VM1, you would name the VM DDP-VM1 (not XYZ-VM1).**

:html:`<iframe width="99%" height="450" frameborder="0" scrolling="no" src="https://nutanixinc-my.sharepoint.com/:x:/g/personal/christo_rasmuss_nutanix_com/EcHzx1Qo_uZIj-ZxBz0YQK8BYPC6i-abQSvtBSlrcRXuAw?e=AswoFp&action=embedview&ActiveCell='Anaheim'!A1&Item='Anaheim'!A1%3AO319&wdDownloadButton=True&wdInConfigurator=True"></iframe>`

.. note::

  The table above can be filtered in place to display only your assignment or can be downloaded and viewed locally.

  If the embedded spreadsheet does not load, try loading the page in Incognito or Private browsing mode.

.. _stagingdetails:

Cluster Staging Details
+++++++++++++++++++++++

Each attendee will have access to a **SHARED** AOS 5.10.2 (AHV 20170830.185) cluster, staged as follows:

.. note::

  Refer to :ref:`clusterassignments` for the *XX* and *YY* octets for your cluster and replace where appropriate.

  For example, if your **Cluster/Prism Element Virtual IP** is 10.42.10.37, substitute *42* for *XX* and *10* for *YY* below.

Virtual Machines
................

The following VMs have already been provisioned to each cluster:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - VM Name
     - IP Address
     - Description
   * - **Prism Central**
     - 10.XX.YY.39
     - Nutanix Prism Central 5.10.1, Calm 2.6.0.3
   * - **AutoDC2**
     - 10.XX.YY.40
     - ntnxlab.local Domain Controller

Images
......

All disk images required to complete the labs have been uploaded to the Image Service for each cluster:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Image Name
     - Description
   * - **Windows2012R2.qcow2**
     - Pre-built Windows Server 2012 R2 Standard Disk Image (Sysprep)
   * - **Windows10-1709.qcow2**
     - Pre-built Windows 10 Disk Image (Sysprep)
   * - **CentOS7.qcow2**
     - Pre-built CentOS 7 Disk Image
   * - **ToolsVM.qcow2**
     - Pre-built Windows Server 2012 R2 + Tools (pgAdmin, CyberDuck, text editors, etc.) Disk Image
   * - **acs-centos7.qcow2**
     - CentOS Kubernetes Host for Karbon Disk Image
   * - **ERA-Server-build-1.0.1.qcow2**
     - Era 1.0.1 Disk Image


Credentials
...........

The lab guides will explicitly share any unique credentials, the table below contains common credentials used throughout the labs:

.. list-table::
  :widths: 33 33 33
  :header-rows: 1

  * - Name
    - Username
    - Password
  * - **Prism Element**
    - admin
    - nx2Tech2019!
  * - **Prism Central**
    - admin
    - nx2Tech2019!
  * - **Controller VMs**
    - nutanix
    - nx2Tech2019!
  * - **Prism Central VM**
    - admin
    - nx2Tech2019!
  * - **NTNXLAB Domain**
    - NTNXLAB\\Administrator
    - nutanix/4u

Networks
........

The following virtual networks have been pre-configured for each cluster:

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * -
     - **Primary** Network
     - **Secondary** Network
   * - **IPAM**
     - Enabled
     - Enabled
   * - **DHCP Pool**
     - 10.XX.YY.50 - 124
     - 10.XX.YY.132 - 229
   * - **Default Gateway**
     - 10.XX.YY.1
     - 10.XX.YY.129
   * - **Netmask**
     - 255.255.255.128
     - 255.255.255.128
   * - **DNS**
     - 10.XX.YY.40 (DC VM)
     - 10.XX.YY.40 (DC VM)
