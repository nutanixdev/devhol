----------------------------
Nutanix Cloud-Init Quick Lab
----------------------------

Overview
++++++++

**Estimated time to complete: 30-60 MINUTES**

The Nutanix Cloud-Init Quick Lab will cover a few key points.

- Cloud-Init intro
- Preparing your cluster for Cloud-Init based VM deployments
- Deployment of a CentOS 7 based environment bootstrapped with Cloud-Init

This lab was written in May 2019 with the following Nutanix software versions:

- Acropolis 5.10.3.1 LTS
- Prism Central 5.10.3

Introduction
++++++++++++

When setting up development environments the requirements can often be highly repeatable across deployment iterations.

For example, let's say you are developing a Python application that will run on a CentOS 7 Linux VM.  Sure, you could create this VM, install the packages manually and then clone the VM later.  There are no "issues" with that approach, but what if you need to do the following on all VMs deployed in the future ...

- Update all packages to their latest versions?
- Quickly add a new package?
- Change the hostname?
- Add a/another specific SSH key pair?

This is where bootstrap tools like Cloud-Init come in.  For some time now, Cloud-Init has been fully supported by Nutanix Acropolis.  Nutanix and Cloud-Init together allows you to create a VM and, during the time of creation, automatically carry out a set of predefined tasks.  For example:

- Ensure a specific set of packages is installed
- Specific SSH key pairs are installed
- User accounts are created
- Custom scripts or commands are run
- ... etc

How do we do this with Nutanix?  Easy!  Read on ...

Sample code
+++++++++++

Before getting started, please note the following.

Throughout this lab there are a number of code samples provided for you use.  When moving the mouse over these samples, a copy button will appear in the top-corner of the code block.  It is strongly recommended to use this button when copying sample code, instead of manually copying the text from the browser window.

.. figure:: images/copy_button.png

Deploying Cloud-Init VM
+++++++++++++++++++++++

Our clusters already have images that can be used with Cloud-Init; we can now begin with the first VM deployment.

Base VM
.......

#. Login to Prism Central

#. Select :fa:`bars` **> Virtual Infrastructure > VMs**.

    .. figure:: images/pc_vms.png

#. Select **Create VM**

#. **Name** - *Initials*-Cloud-Init-VM

#. **Description** - VM created with Cloud-Init

#. **Timezone** - Leave unchanged

#. **Use this VM as an agent VM** - Unchecked

#. **VCPU(S)** - 1

#. **Number Of Cores Per Vcpu** - 1

#. **Memory** - 1

#. **Disks** - Select **Add New Disk**

     - **Type** - Disk
     - **Operation** - Clone from Image Service
     - **Bus Type** - SCSI
     - **Image** - *CentOS7.qcow2*
     - **Size** - Disabled field for this operation
     - **Index** - Next Available

     .. figure:: images/add_disk.png

#. Click **Add**

#. Click **Add New NIC**

     - **VLAN Name** - Primary
     - **Network Connection State** - Connected (this option may not be available if using Nutanix Community Edition)
     - **IP Address** - Leave blank to ensure the NIC receives a DHCP address

#. Click **Add**

#. *DO NOT* click the Save button yet

**Cloud-Init Configuration**

This section is where we move beyond the creation of a "basic" VM and into the Cloud-Init specific configuration.

#. **Custom Script** - Checked

#. **Type or Paste Script** - Selected (double-check that you have clicked the radio button!)

#. Paste the YAML file below into the field provided

     .. figure:: images/pe_pc_create_vm.png

    A Cloud-Init YAML spec has been prepared for you ahead of time.  To use this file, you will need to create or use an existing SSH key pair.  A sample public/private key pair has been provided below.  Please note we will add a real SSH Public Key in upcoming steps.

     .. code-block:: bash

        #cloud-config
        users:
          - name: nutanix
            sudo: ['ALL=(ALL) NOPASSWD:ALL']
            ssh-authorized-keys:
              - <your public SSH RSA key will go here>
            lock-passwd: false
            passwd: $6$4guEcDvX$HBHMFKXp4x/Eutj0OW5JGC6f1toudbYs.q.WkvXGbUxUTzNcHawKRRwrPehIxSXHVc70jFOp3yb8yZgjGUuET.

        # note: the encoded password hash above is "nutanix/4u" (without the quotes)

        yum_repos:
          epel-release:
            baseurl: http://download.fedoraproject.org/pub/epel/7/$basearch
            enabled: true
            failovermethod: priority
            gpgcheck: true
            gpgkey: http://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-7
            name: Extra Packages for Enterprise Linux 7 - Release

        package_update: true
        package_upgrade: true

        hostname: centos7-tools-vm

        packages:
          - gcc-c++
          - make
          - unzip
          - bash-completion
          - python-pip
          - s3cmd
          - stress
          - awscli
          - ntp
          - ntpdate
          - nodejs
          - python36
          - python36-setuptools
          - jq

        runcmd:
          - npm install -g request express
          - systemctl stop firewalld
          - systemctl disable firewalld
          - /sbin/setenforce 0
          - sed -i -e 's/enforcing/disabled/g' /etc/selinux/config
          - /bin/python3.6 -m ensurepip
          - pip install -U pip
          - pip install boto3 python-magic
          - ntpdate -u -s 0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org
          - systemctl restart ntpd

        final_message: CentOS 7 Tools Machine setup successfully!

     .. _GitHub: https://github.com/nutanixdev/cloud-init/blob/master/20190513_centos7toolsvm.yaml

     If you would like to refer to the YAML file later, it has also been made available on GitHub_.

     So what does this Cloud-Init YAML spec actually do?

     - Creates a user named 'nutanix'.  In the **Nutanix** image, this user already exists, although there's some other user configuration we'll do, too
     - Adds the specified SSH key to the nutanix user's **~/.ssh/authorized_keys** file i.e. sets that key as authorised for login via SSH
     - Adds the RHEL 7 'Epel' repo (release version)
     - Updates and upgrades all CentOS 7 packages
     - Installs a selection of packages e.g. Python utilities, AWS tools, NTP, jq (see the full list above)
     - Runs some post-installation commands to configure NTP and disable SELinux (this is one of the reasons the file would need to be modified before use in production)

     **Note**

    Please refer to the Nutanix Cloud-Init Limitations_ and Guidelines documentation for important information on using Cloud-Init in production.

    .. _Limitations: https://portal.nutanix.com/#/page/docs/details?targetId=Web-Console-Guide-Prism-v510:wc-vm-image-guidelines-wc-r.html

#. In the Cloud-Init spec that was just copied and pasted, near the top, replace **<your public SSH RSA key will go here>** with either your own SSH public key, or the key provided below, if you don't have one available:

    **Public key**

    ::

      ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAii7qFDhVadLx5lULAG/ooCUTA/ATSmXbArs+GdHxbUWd/bNGZCXnaQ2L1mSVVGDxfTbSaTJ3En3tVlMtD2RjZPdhqWESCaoj2kXLYSiNDS9qz3SK6h822je/f9O9CzCTrw2XGhnDVwmNraUvO5wmQObCDthTXc72PcBOd6oa4ENsnuY9HtiETg29TZXgCYPFXipLBHSZYkBmGgccAeY9dq5ywiywBJLuoSovXkkRJk3cd7GyhCRIwYzqfdgSmiAMYgJLrz/UuLxatPqXts2D8v1xqR9EPNZNzgd4QHK4of1lqsNRuz2SxkwqLcXSw0mGcAL8mIwVpzhPzwmENC5Orw== rsa-key-20190108

    The private key below is for use later, if you would like to login to the new VM using SSH.  This is optional.

    **Private key**

    ::

      -----BEGIN RSA PRIVATE KEY-----
      MIIEowIBAAKCAQEAii7qFDhVadLx5lULAG/ooCUTA/ATSmXbArs+GdHxbUWd/bNG
      ZCXnaQ2L1mSVVGDxfTbSaTJ3En3tVlMtD2RjZPdhqWESCaoj2kXLYSiNDS9qz3SK
      6h822je/f9O9CzCTrw2XGhnDVwmNraUvO5wmQObCDthTXc72PcBOd6oa4ENsnuY9
      HtiETg29TZXgCYPFXipLBHSZYkBmGgccAeY9dq5ywiywBJLuoSovXkkRJk3cd7Gy
      hCRIwYzqfdgSmiAMYgJLrz/UuLxatPqXts2D8v1xqR9EPNZNzgd4QHK4of1lqsNR
      uz2SxkwqLcXSw0mGcAL8mIwVpzhPzwmENC5OrwIBJQKCAQB++q2WCkCmbtByyrAp
      6ktiukjTL6MGGGhjX/PgYA5IvINX1SvtU0NZnb7FAntiSz7GFrODQyFPQ0jL3bq0
      MrwzRDA6x+cPzMb/7RvBEIGdadfFjbAVaMqfAsul5SpBokKFLxU6lDb2CMdhS67c
      1K2Hv0qKLpHL0vAdEZQ2nFAMWETvVMzl0o1dQmyGzA0GTY8VYdCRsUbwNgvFMvBj
      8T/svzjpASDifa7IXlGaLrXfCH584zt7y+qjJ05O1G0NFslQ9n2wi7F93N8rHxgl
      JDE4OhfyaDyLL1UdBlBpjYPSUbX7D5NExLggWEVFEwx4JRaK6+aDdFDKbSBIidHf
      h45NAoGBANjANRKLBtcxmW4foK5ILTuFkOaowqj+2AIgT1ezCVpErHDFg0bkuvDk
      QVdsAJRX5//luSO30dI0OWWGjgmIUXD7iej0sjAPJjRAv8ai+MYyaLfkdqv1Oj5c
      oDC3KjmSdXTuWSYNvarsW+Uf2v7zlZlWesTnpV6gkZH3tX86iuiZAoGBAKM0mKX0
      EjFkJH65Ym7gIED2CUyuFqq4WsCUD2RakpYZyIBKZGr8MRni3I4z6Hqm+rxVW6Dj
      uFGQe5GhgPvO23UG1Y6nm0VkYgZq81TraZc/oMzignSC95w7OsLaLn6qp32Fje1M
      Ez2Yn0T3dDcu1twY8OoDuvWx5LFMJ3NoRJaHAoGBAJ4rZP+xj17DVElxBo0EPK7k
      7TKygDYhwDjnJSRSN0HfFg0agmQqXucjGuzEbyAkeN1Um9vLU+xrTHqEyIN/Jqxk
      hztKxzfTtBhK7M84p7M5iq+0jfMau8ykdOVHZAB/odHeXLrnbrr/gVQsAKw1NdDC
      kPCNXP/c9JrzB+c4juEVAoGBAJGPxmp/vTL4c5OebIxnCAKWP6VBUnyWliFhdYME
      rECvNkjoZ2ZWjKhijVw8Il+OAjlFNgwJXzP9Z0qJIAMuHa2QeUfhmFKlo4ku9LOF
      2rdUbNJpKD5m+IRsLX1az4W6zLwPVRHp56WjzFJEfGiRjzMBfOxkMSBSjbLjDm3Z
      iUf7AoGBALjvtjapDwlEa5/CFvzOVGFq4L/OJTBEBGx/SA4HUc3TFTtlY2hvTDPZ
      dQr/JBzLBUjCOBVuUuH3uW7hGhW+DnlzrfbfJATaRR8Ht6VU651T+Gbrr8EqNpCP
      gmznERCNf9Kaxl/hlyV5dZBe/2LIK+/jLGNu9EJLoraaCBFshJKF
      -----END RSA PRIVATE KEY-----

#. Click **Save**

     At this point, Nutanix Acropolis will create a VM with the specifications you have provided.  During this process you will see a task named **Batch Prism fanout**.  Clicking the **Details** link will show a sub-task named **VM create with customize**.  This is Nutanix Acropolis preparing the VM to run our Cloud-Init spec the first time it is powered on.  Wait until this step is completed before you try to power the VM on.

     .. figure:: images/create_vm_with_customize_pc.png

#. To check the status of the **Create VM with customize** task, follow the steps below.

   - Click the **Tasks** button (highlighted in blue) and then click **View All Tasks >** (highlighted in red)

     .. figure:: images/tasks_pc.png

#. When the **Create VM with customize** task has completed, select your new VM and power it on

     - In Prism Central it is recommended to use the **Search** field, finding your VM then clicking the **Power On** button

       .. figure:: images/power_on_pc.png

Verifying Cloud-Init status
...........................

At this point there isn't much to see if you open the VM console (although this is somewhat dependant on how the VM image is configured).

What we can do, though, is wait a few minutes for the Cloud-Init processes to complete, then login to the VM and take a look.

.. note::

  When opening the console below, please be aware that you'll be shown all console output that occurs during your session.  If you are trying to enter a username or password and the console shows verbose system output, press **Enter** and you should be taken back to the standard login prompt.

#. Login to the VM:

    Prism Central:

      - Select :fa:`bars` **> Virtual Infrastructure > VMs**.

        .. figure:: images/pc_vms.png

      - Option 1: Check the box next to your VM's name, click the **Actions** dropdown button and click **Launch Console**

        .. figure:: images/launch_console_pc.png

      - Option 2: Search for your VM using the **Search** field, select your VM and click **Power On**

        .. figure:: images/power_on_pc.png

    The remaining steps apply to the console on Prism Central.

#. Login to the VM either with username **nutanix** and password **nutanix/4u** (console only!) or with the SSH key provided earlier (for advanced users familiar with using key pair authentication).

#. Run the following (long, but clean) command.  Please note that you'll need to enter this command manually vs copy and paste used in previous steps.

     .. code-block:: bash

       clear; echo; sudo tail -5 /var/log/cloud-init.log; echo; sudo cat /run/cloud-init/status.json; echo;

     That will show the output of two files:

     - /var/log/cloud-init.log
     - /run/cloud-init/status.json

     Looking at the contents of those files you'll be able to see if any errors were generated during the Cloud-Init process.  An example is shown below.

     .. figure:: images/cloud_init_running.png

#. Lastly, we can also check if the process worked by doing a simple **yum** check on one of the packages we asked to install.

     .. code-block:: bash

       sudo yum install python-pip

     Since we specified **python-pip** should be installed by Cloud-Init, you should receive something similar to the following (the version number may be different):

     .. code-block:: bash

       Package python2-pip-8.1.2-8.el7.noarch already installed and latest version

Finishing up and takeaways
++++++++++++++++++++++++++

So now let's summarise what we've done in this quick lab.

- Obtained a Cloud-Init YAML spec that can be used with the Nutanix "Custom Scripts" option
- Made sure our SSH public/private key pair is ready for use with the Cloud-Init YAML spec
- Deployed a VM using VM customization
- Checked to make sure our Cloud-Init run was successful

Wrapping Up
+++++++++++

Lastly, what are the key concepts from this lab?

In short, there's one main concept that you should hopefully take away from today - that Nutanix makes it very easy to deploy repeatable, customizable VMs using Cloud-Init.

If you've gotten this far, you've successfully created a VM using Prism Central and customised it using Cloud-Init.  Nice!

Thanks for taking the time to complete this lab - we hope it was fun and educational.

Lab Resources
+++++++++++++

We also have a growing collection of labs that demonstrate other helpful developer-centric concepts.  Please see the Nutanix Developer Portal Labs_ page for more info.

.. _Labs: https://nutanix.dev/labs

Final Thoughts
++++++++++++++

For further information on this and other technologies interesting to developers, please see Nutanix Developer Portal_.  There will you find code samples, documentation and a regularly updated blog covering differnt Nutanix technologies.

- Nutanix Developer Portal_

.. _Portal: https://nutanix.dev
