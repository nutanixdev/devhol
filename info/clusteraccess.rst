.. _clusteraccess:

----------------------
Accessing Your Cluster
----------------------

Clusters used for the **Hands on Labs** run within the Nuanix Hosted POC environment, hosted in the Nutanix PHX and RTP datacenters.

In order to access these resources you must be connected to one of the (2) VPN options listed below. Connection to a virtual desktop environment **is not necessary**.

.. note::

  Certain labs leverage a Windows VM with pre-installed tools to provide a controlled environment. It is **highly recommended** that you connect to these Windows VMs using the Microsoft Remote Desktop client rather than the VM console launched via Prism. An RDP connection will allow you to copy and paste between your device and the VMs.


Attendee VPN
............

Log in to https://xlv-uswest1.nutanix.com using the following credentials:

- **Username** - Refer to :ref:`clusterassignments` for your **Lab VPN Username**
- **Password** - techX2019!

Under **Client Application Sessions**, click **Start** to the right of **Pulse Secure** to download the client.

Install and open **Pulse Secure**.

Add a connection:

- **Type** - Policy Secure (UAC) or Connection Server
- **Name** - HPOC VPN
- **Server URL** - https://xlv-uswest1.nutanix.com

Connect using the provided credentials.
