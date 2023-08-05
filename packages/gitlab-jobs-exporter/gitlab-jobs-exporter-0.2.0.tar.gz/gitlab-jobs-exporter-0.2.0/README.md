# GitLab CI Jobs Exporter
This tool allows for exporting build job metrics from GitLab CI.
It is used to monitor the experience as a user of the CI infrastructure.
More information at https://xinau.ch/notes/prometheus-gitlab-job-exporter/

## Installation
```
pip install gitlab_jobs_exporter
```
In the examples folder exists a sample systemd unit file template.

## Usage
Required environment variables are:
- `ACCESS_TOKEN` api token https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html

Required arguments are:
- `--url` url of your gitlab instance (`https://gitlab.example.com`)
- `--project` project id of your jobs

Optional arguments are:
- `--interval` the scrape interval in seconds (default 10s)
- `--port` the port on which the server runs (default 9118)


