<h1 align="center">Website Stress Test Script</h1>

<p align="center">
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

This script is a Python program that can be used to stress test a website by sending a large number of requests using either the GET or POST method. The script can optionally use one or more SOCKS5 proxies to route the requests, and can write the output to a log file.

## Prerequisites

This script requires Python 3 and the `requests` and `pyproxy` libraries. You can install these libraries using `pip`:

```bash
pip install requests pyproxy

