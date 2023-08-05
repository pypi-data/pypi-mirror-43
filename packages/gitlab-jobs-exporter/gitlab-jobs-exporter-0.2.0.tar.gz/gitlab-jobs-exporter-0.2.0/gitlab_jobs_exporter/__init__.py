import json
import os
import sys
import time

from dateutil.parser import parse
from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from urllib.request import Request, urlopen

COLLECTION_TIME = Summary("gitlab_jobs_collector_collect_seconds",
                          "Time spent to collect metrics from GitLab")

class GitLabJobsCollector:
    """gitlab jobs exporter"""
    scopes = ["failed", "success"]


    def __init__(self, url, project, token):
        """initalize target and project for collector"""
        self._url = url.rstrip("/")
        self._project = project
        self._token = token
        self._prometheus_metrics = {}


    def collect(self):
        """collect interface used by REGISTRY"""
        start = time.time()

        self._setup_prometheus_metrics()

        for scope in self.scopes:
            latest = self._request_data(scope)
            self._add_to_prometheus_metrics(scope, latest)

        for scope in self.scopes:
            for metric in self._prometheus_metrics[scope].values():
                yield metric

        duration = time.time() - start
        COLLECTION_TIME.observe(duration)


    def _setup_prometheus_metrics(self):
        """setup metrics we want to export"""
        for scope in self.scopes:
            self._prometheus_metrics[scope] = {
                "id":
                    GaugeMetricFamily("gitlab_job_latest_id",
                                      "latest GitLab job id",
                                      labels=["project", "scope"]),
                "duration":
                    GaugeMetricFamily("gitlab_job_latest_duration_seconds",
                                      "latest GitLab job duration in seconds",
                                      labels=["project", "scope"]),
                "created_timestamp":
                    GaugeMetricFamily("gitlab_job_latest_created_timestamp_seconds",
                                      "latest GitLab job created timestamp in unixtime",
                                      labels=["project", "scope"]),
                "finished_timestamp":
                    GaugeMetricFamily("gitlab_job_latest_finished_timestamp_seconds",
                                      "latest GitLab job finished timestamp in unixtime",
                                      labels=["project", "scope"]),
                "started_timestamp":
                    GaugeMetricFamily("gitlab_job_latest_started_timestamp_seconds",
                                      "latest GitLab job started timestamp in unixtime",
                                      labels=["project", "scope"]),
            }


    def _request_data(self, scope):
        """request jobs from gitlab for a scope"""
        request = Request(
            "{0}/api/v4/projects/{1}/jobs?scope[]={2}".format(
                self._url, self._project, scope))
        request.add_header("PRIVATE-TOKEN", self._token)

        # latest job is always the first item
        return json.loads(urlopen(request).read().decode("utf-8"))[0]


    def _add_to_prometheus_metrics(self, scope, data):
        """add compute data and scope for prometheus_metrics"""

        try: created = parse(data.get("created_at")).timestamp()
        except TypeError: created = 0
        try: finished = parse(data.get("finished_at")).timestamp()
        except TypeError: finished = 0
        try: started = parse(data.get("started_at")).timestamp()
        except TypeError: started = 0

        self._prometheus_metrics[scope]["id"].add_metric([self._project, scope], data.get("id", 0))
        self._prometheus_metrics[scope]["duration"].add_metric([self._project, scope], data.get("duration", 0))
        self._prometheus_metrics[scope]["created_timestamp"].add_metric([self._project, scope], created)
        self._prometheus_metrics[scope]["finished_timestamp"].add_metric([self._project, scope], finished)
        self._prometheus_metrics[scope]["started_timestamp"].add_metric([self._project, scope], started)
