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

#### &lt;name&gt;.py

TODO: more info on how this file is structured, the format of the data
returned, how it correlates to the widget data-id, and notes on the
class object instance persistency.

#### &lt;name&gt;.yapsy-plugin

TODO: more info on how this file is structured and how it correlates to
the &lt;name&gt;.py file.

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
