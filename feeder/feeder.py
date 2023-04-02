#!/usr/bin/env python3

import argparse
import datetime
import requests
import os
import sys

from datetime import datetime
from typing import Callable

from apscheduler.schedulers.blocking import BlockingScheduler
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin


def report_data(base_endpoint_url: str, widget: str, data: dict) -> None:
    """Helper function to send job data to dashboard widgets"""
    endpoint_url = f"{base_endpoint_url.rstrip('/')}/{widget}"
    print(data)
    try:
        resp = requests.post(endpoint_url, json=data)
        if resp.status_code < 200 or resp.status_code > 299:
            print(f"Error: {widget}: {resp.text}")
    except:
        pass


def run_job(base_endpoint_url: str, auth_token: str, job: IPlugin) -> None:
    """Wrapper function to run jobs"""
    print(f"Running: {job.name}")
    data = job.plugin_object.get_data()

    # Validate returned data
    # Expect a dict where each key is a widget name and the value is the data
    # to send to the widget
    if type(data) is not dict:
        print("Error: job did not return dictionary")
        sys.exit(1)

    for widget, widget_data in data.items():
        if type(widget_data) is not dict:
            print(f"Error: data for widget {widget} is not a dictionary")
            sys.exit(1)

    # Send data to dashboard
    for widget, widget_data in data.items():
        widget_data["auth_token"] = auth_token
        report_data(base_endpoint_url, widget, widget_data)


def tick() -> None:
    """Show alive message"""
    print("Tick: %s" % datetime.now())


def valid_job(job: IPlugin) -> bool:
    """Check if job definition has required methods and attributes"""
    result = True
    job_interval_func = getattr(job.plugin_object, "get_interval", None)
    if not job_interval_func or not callable(job_interval_func):
        print("Error: job missing get_interval()")
        result = False

    job_data_func = getattr(job.plugin_object, "get_data", None)
    if not job_data_func or not callable(job_data_func):
        print("Error: job missing get_data()")
        result = False

    return result


def main() -> None:
    """Main function"""
    auth_token = os.environ.get("AUTH_TOKEN", "MY_AUTH_TOKEN")

    argparser = argparse.ArgumentParser(
        description="Feeder script for Smashing dashboard"
    )

    argparser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        default="http://127.0.0.1:3030/widgets",
        help="Dashboard api endpoint url (default: http://127.0.0.1:3030/widgets)",
    )
    argparser.add_argument(
        "-d", "--debug", action="store_true", help="Toggle job debug logging"
    )
    argparser.add_argument(
        "-t",
        "--token",
        type=str,
        default=auth_token,
        help="Set dashboard endpoint authentication token",
    )

    args = argparser.parse_args()

    # Load jobs
    print("Loading plugins...")
    jobs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs")

    manager = PluginManager()
    manager.setPluginPlaces([jobs_dir])
    manager.collectPlugins()

    for job in manager.getAllPlugins():
        if not valid_job(job):
            print(f"Cannot load job: {job.name}")
            sys.exit(1)

        print(f"Loaded: {job.name} ({job.path})")

    print("Plugins loaded.")

    # create event loop via the BlockingScheduler
    print("Configuring scheduler")
    scheduler = BlockingScheduler()

    # add regular "i'm-alive" job to show daemon is alive
    scheduler.add_job(tick)
    scheduler.add_job(tick, "interval", seconds=60)

    # add jobs
    for job in manager.getAllPlugins():
        job_interval = job.plugin_object.get_interval()

        # Force immediate run of jobs on start
        scheduler.add_job(run_job, args=[args.endpoint, args.token, job])

        # Schedule jobs to run on regular intervals
        scheduler.add_job(
            run_job,
            "interval",
            args=[args.endpoint, args.token, job],
            seconds=job_interval,
        )

    print("Scheduler configured.")

    # Begin scheduler processing
    print("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
