API Intro
#########

Nutanix API Intro
.................

Before we start creating our app, let's take a look at how Nutanix describes the APIs we'll use today.

**Those familiar with the Nutanix APIs may wish to skip this section.**

The Nutanix REST APIs allow you to create scripts that run system administration commands against the Nutanix cluster.
The API enables the use of HTTP requests to get information about the cluster as well as make changes to the configuration.
Output from the API calls are returned in JSON format.

The v2 API is an update of the v1 API. Users of the v1 API are encouraged to migrate to v2.

Authentication
..............

Authentication against the Nutanix REST APIs is done using HTTP Basic Authentication.
Requests on HTTP port 80 are automatically redirected to HTTPS port 443.
This requires that a valid cluster or configured directory service credential is passed as part of the API request.

For the purposes of this lab, we will assume you have access to at least a Nutanix cluster username with a minimum of READ access.
Note that a Cluster Admin account is not required to read information via Nutanix API request.

For those attendees or readers following this lab in a presenter-led environment, please use the cluster IP address and credentials given to you by your presenter.

Prism Element "vs" Prism Central
................................

Prism Element APIs are cluster-specific i.e. designed to manage and manipulate entities on the cluster Prism is running on.

Prism Central APIs include a larger set of APIs designed to manipulate entities that aren't necessarily specific to a single cluster.

API Versions
............

As at January 2019, there are four publicly available Nutanix APIs.  Note that while Nutanix API v0.8 is available via the REST API Explorer in Nutanix Prism, it is strongly recommended to use v2.0 APIs instead.  v0.8 is mentioned here for completeness reasons only.

The API versions available today are as follows.

- v1
- v2.0
- v3

**Note re security:** In the sample commands below you'll see use of the `--insecure` cURL parameter.  This is used to get around SSL/TLS verification issues when using self-signed certificates.  Please consider the potential pitfalls and security implications of bypassing certificate verification before using `--insecure` in a production environment.  The same precautions apply when providing a username and password on the command-line.  This should be avoided when possible, since this method shows both the username and password in clear text.

**Note re Windows systems:** When running the cURL sample commands on Windows 10, single-quote characters (`'`) may need to be replaced with double-quote characters (`"`).

API v0.8
~~~~~~~~

Status: Super-ceded by API v2.0

This set of APIs was available when API v1 didn’t yet have the capability to carry out some VM management operations, e.g. VM power state.

Using a combination of v0.8 and v1 APIs, nearly all information and functions available in Prism could be completed via API requests.

Here's an example of an API v0.8 request to list the VMs running on a cluster.

.. code-block:: html

  https://<cluster_virtual_ip>:9440/api/nutanix/v0.8/vms

Alternatively, this HTTPS API request can be carried out using the `curl` command:

.. code-block:: bash

  curl -X GET \
    'https://<cluster_virtual_ip>:9440/api/nutanix/v0.8/vms' \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    --insecure \
    --basic --user <cluster_username>:<cluster_password>

API v1
~~~~~~

Status: Available

This set of APIs, chronologically, was released before the v0.8 APIs. They were used, for example, to manipulate and view VMs, storage containers, storage pools etc. For some time, the v1 and v0.8 APIs were the only way we, as developers, had to interact with Nutanix clusters. Some of the API endpoints could only be used with the AHV hypervisor and some could be used across multiple hypervisors e.g. AHV and ESXi.

Here’s a simple example of a v1 API request to list all storage containers on a cluster:

.. code-block:: html

  https://<cluster_virtual_ip>:9440/api/nutanix/v1/containers

Alternatively, this HTTPS API request can be carried out using the `curl` command:

.. code-block:: bash

  curl -X GET \
    'https://<cluster_virtual_ip>:9440/api/nutanix/v1/containers?=' \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    --insecure \
    --basic --user <cluster_username>:<cluster_password>

One of the reasons to use API v1 today is to collect entity performance information.  For example, the application we are building in this lab contains API v1 requests to collect storage performance.  An upcoming Nutanix Developer blog article will discuss the API v1 performance metrics and how to use them.

API v2.0
~~~~~~~~

Status: Available

The v0.8 and v1 APIs worked really well. In fact, they were (and still are, in some respects) how the Prism UI gathers data from the cluster. Another over-simplification would be to say that the v2 APIs are where the v0.8 and v1 APIs came together. Many of the entities and endpoints available in v0.8 and v1 were made available in v2, along with a huge amount of backend cleanup, endpoint renaming and generally making the APIs better. The v2 APIs are also the first officially GA API made available by Nutanix.

If you have some exposure to the previous v0.8 and v1 APIs, moving to the v2 APIs will highlight a number of differences. For example “containers” got renamed to “storage_containers” and “storagePools” got renamed to “storage_pools”. The difference? A consistent naming convention in the form of snake-case across all entities.

Here’s a basic example of a v2 API request to list all **storage_containers** on a cluster:

.. code-block:: html

  https://<cluster_virtual_ip>:9440/api/nutanix/v2.0/storage_containers

Alternatively, this HTTPS API request can be carried out using the `curl` command:

.. code-block:: bash

  curl -X GET \
    https://<cluster_virtual_ip>:9440/api/nutanix/v2.0/storage_containers \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    --insecure \
    --basic --user <cluster_username>:<cluster_password>

Quick Summary
~~~~~~~~~~~~~

Before moving forward, note that all the APIs above return a JSON response that is easily consumable by many programming or scripting languages.

Also, all the requests above are basic HTTP GET requests and do not require a payload (POST body).

API v3
~~~~~~

Status: Available

The v3 APIs, which were released as GA on April 17th 2018, are the first departure from how things were done before.

We had standard GET requests to get data from a cluster and standard POST methods to make changes - the v3 APIs are a bit different. All the previous APIs still required the developer to tell the system what to do and how to do it. The v3 APIs, on the other hand, are the first APIs built around an Intentful paradigm, that is, `move the programming from the user to the machine`. Instead of writing a ton of code to get something done, we tell the system what the desired state is and the system will “figure out” the best way to get there. This will sound somewhat familiar to those using configuration management frameworks like Salt, Puppet, Chef, Ansible, PowerShell DSC etc.

How this all happens is somewhat beyond the scope of this particular lab but look at the request below. It’s still getting similar information to the previous requests but with a couple of key differences.

1. It is an HTTP POST request, not GET.
2. A JSON payload (POST body) is required so that the cluster knows what type of entity to return. In this example, we’re talking about VMs.
3. We’re telling the system what we want to do with the data. In this case, we want to list all VMs.
4. While this request can be run without issue against Prism Element, it can also be run against Prism Central. More on that later.

.. code-block:: html

  https://<prism_central_or_cluster_virtual_ip>:9440/api/nutanix/v3/vms/list

And the post body:

.. code-block:: JSON

  {"kind":"vm"}

Alternatively, this HTTPS API request can be carried out using the `curl` command:

.. code-block:: bash

  curl -X POST \
    https://<prism_central_virtual_ip>:9440/api/nutanix/v3/vms/list \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"kind":"vm"}' \
    --insecure \
    --basic --user <cluster_username>:<cluster_password>

cURL Command Analysis
.....................

As an extra step, let's take the v3 API request above and look at what each part of the command is doing.  If you are familiar with using cURL to make API requests, please feel free to skip this section.

- `curl -X POST \` - Run cURL and specify that we will be making an HTTP POST request (as opposed to HTTP GET).
- `https://<prism_central_virtual_ip>:9440/api/nutanix/v3/vms/list \` - Specify the complete URL to send the request to.
- `-H 'Accept: application/json' \` - Specify the content types the client is able to understand.
- `-H 'Content-Type: application/json' \` - Tell the server what type of data is actually sent.
- `-d '{"kind":"vm"}' \` - For our POST request, specify the request **body** i.e. the parameters to send along with the request.
- `--insecure \` - Tell the cURL command to ignore SSL certificate verification errors (please see the note above re what this means).
- `--basic` - Tell the cURL command that we will authenticate using **Basic Authentication**.
- `--user <cluster_username>:<cluster_password>` - Specify the username and password to use during basic authentication.

Version Use Cases
.................

With what we know about the various API versions now, let's take a look at why you might use each API.

- **v1**: Legacy application support and cluster-wide performance metrics.
- **v2.0**: Migration away from legacy APIs, combination of older v0.8 and v1 APIs into single GA API, <em>cluster-specific</em> tasks e.g. storage container information & management.
- **v3 on Prism Element**: Latest supported API aimed at managing <em>cluster-specific</em> entities such as VMs.
- **v3 on Prism Central**: Latest supported API aimed at managing <em>environment-wide</em> configuration and entities.  Unlike API v3 on Prism Element, this includes a vast array of entities such as Nutanix Calm Blueprints, RBAC, Applications, Nutanix Flow Network Security Rules.

Summary
.......

At this point, you know what the available APIs versions are and what some of the differences are between them.

Now let’s move on to the lab itself.