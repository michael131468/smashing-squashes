# smashing-squashes

A Python friendly [Smashing][0] dashboard setup.

## About

The [Smashing][0] dashboard is a simple and elegant dashboard solution
built with Ruby. The default language used to write jobs for this
dashboard is with Ruby but the dashboard supports receiving data via a
http endpoint (formatted with json).

This framework (smashing-squashes) is a quick fast-food setup for
Smashing that enables the use of Python plugins to feed the dashboard
with data. The bundled Python framework (feeder.py) allows for
developing Python functions in a structured manner (as jobs) that the
framework automatically runs on configurable intervals and emits the
data collected to the dashboard http endpoint.

The project operates in a Container environment that spawns the
dashboard instance and the Python feeder.py script together. If the
feeder.py script crashes or exits due to error, the container will
exit.

This project may be useful if you want a containerised Smashing
dashboard solution to spawn in your k8s cluster and if you would prefer
to use Python instead of Ruby to feed it data (in a centralised
fashion).

## Install & Usage (Local Setup)

Clone the project and build the container and launch it.

```
podman build -t squashes:latest .
podman run --rm -p 3030:3030 -it squashes:latest /bin/bash
```

Access the dashboard in your browser with the following url:

[http://127.0.0.1:3030/](http://127.0.0.1:3030)

## Customising the Dashboard Layout

You can customise the dashboard layout by editing the files under the
`dashboard/dashboards` subdirectory. The default layout comes from the
defaults of the Smashing dashboard.

You need to re-build and re-launch the container after changing these
files for them to take effect.

## Customising the Data Jobs

You can add custom data jobs to feed the dashboard in the feeder
subdirectory. A default set are provided that feed the sample layout
with random values. The dashboard widgets and data jobs are linked
together so modifying the dashboard may require removing/updating the
jobs to be in sync otherwise the Container may crash with errors.

To make a new data job, simply make a new subdirectory under
`feeder/jobs` and create a &lt;name&gt;.py file and
&lt;name&gt;.yapsy-plugin file. You can populate these files using the
other job definitions as a template. More info on these files is below.
The jobs framework is using the [Yapsy plugin system][1] as a base so
you can also find more information from that project space.

You need to re-build and re-launch the container after changing these
files for them to take effect.

- &lt;name&gt;.py

  This file defines the Python snippet to run as a data job. It must
  import the IPlugin module from the [Yapsy plugin system][1] and
  define a Class that inherits IPlugin and contains at least the
  following two public methods:

    - get_interval(self) -> int
    - get_data(self) -> dict

  The get_interval method should return an integer representing the job
  execution period in seconds (aka the number of seconds to wait before
  re-running the data job).

  The get_data method should return a dictionary where the keys
  correspond to widget data-id's and the values are the data (as
  dictionaries) to send to the widget endpoint. This allows a job to
  feed multiple widgets (which may save data bandwidth if operating
  on a repetitive data source).

  Example of a custom data job:

  ```Python
  # feeder/jobs/customdata/customdata.py
  from yapsy.IPlugin import IPlugin

  class CustomData(IPlugin):
    def get_interval(self) -> int:
      return 10

    def get_data(self) -> dict:
      data = {"customdata": {"text": "I am customised"}}
      return data
  ```

  If the widget data-id does not exist on the dashboard, this may cause
  the feeder framework to exit with error.

  Note that the class instantiation is once per program, so repeated
  runs of the get_data job can save and restore data in the object
  variables. See the example `valuation` data job for a practical
  example of this.

  This file must correspond to a .yapsy-plugin file (described next).

- &lt;name&gt;.yapsy-plugin

  This file is a basic ini config file that corresponds to the
  &lt;name&gt;.py file. Its definition comes from the [Yapsy plugin
  system][1]. The core configuration should set a human readable name to
  reference the job as, and reference to the linked python script file.
  In the case of the example so far:

  ```INI
  [Core]
  Name = CustomData
  Module = customdata
  ```

  The configuration file should also include some documentation
  attributes. i.e. Author, Version, Website, Description.

  ```INI
  [Documentation]
  Author = Michael Ho
  Version = 0.1
  Website = https://github.com/michael131468/smashing-squashes
  Description = Custom widget data job
  ```

## Custom Dashboard Widgets

You can install custom widgets into the dashboard/widgets subdirectory.

The standard Smashing cli tool can be used or directories and files can
be manually created/downloaded.

Example:

```
cd dashboard
smashing install 150faddf6c637279fe117dd3cb041553
```

This would create a subdirectory named hot_list_status in the widgets
directory containing a coffee file, a html file and an scss file. These
would be copied on Container build into the Smashing dashboard setup
and made available to the dashboard.

## License

The Python framework under the feeder directory is licensed under the
MIT license. See the LICENSE file.

The default files in the dashboard/dashboards subdirectory come from
the [Smashing][0] dashboard project and is the default file layouts.
These are distributed under the MIT license.

[0]: https://github.com/Smashing/smashing/
[1]: https://yapsy.sourceforge.net/
