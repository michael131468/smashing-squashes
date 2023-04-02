# smashing-squashes

A Python friendly smashing dashboard setup

## About

The Smashing dashboard is a simple and elegant dashboard solution built
with Ruby. The default language used to write jobs for this dashboard
is with Ruby but the dashboard supports receiving data via a http
endpoint (formatted with json).

This framework (smashing-squashes) is a quick fast-food setup for
Smashing that enables the use of Python plugins to feed the dashboard
with data. The bundled Python framework (feeder.py) allows for
developing Python functions in a structured manner (jobs) that the
framework automatically runs on regular intervals and emits the data
collected to the dashboard http endpoint.

The project operates in a Container environment that spawns the
dashboard instance and the Python feeder.py script together. If the
feeder.py script crashes or exits due to error, the container will
exit.

## Install & Usage

Clone the project and build the container and launch it.

```
podman build -t squashes:latest .
podman run --rm -p 3030:3030 -it squashes:latest /bin/bash
```

You can customise the dashboard layout by editing the files under the
dashboard subdirectory. You need to re-build and re-launch the container
after changing these files for them to take effect.

You can add custom data fetchers in the feeder subdirectory. Simply
make a new subdirectory under feeder/jobs and create a &lt;name&gt;.py
and &lt;name&gt;.yapsy-plugin. Populate these files using the other job
definitions as a template. The definition of these jobs is explained
below.

## Jobs

TODO.

## License

See LICENSE file.
