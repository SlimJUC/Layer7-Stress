<h1 align="center">Website Stress Test Script</h1>

<p align="center">
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

This script is a Python program that can be used to stress test a website by sending a large number of requests using either the GET or POST method. The script can optionally use one or more SOCKS5 proxies to route the requests, and can write the output to a log file.

## Prerequisites

This script requires Python 3 and the `requests` and `pyproxy` libraries. You can install these libraries using `pip`:

```
pip install requests pyproxy tqdm
```

## Usage
Create a file called proxy_list.txt and add the list of SOCKS5 proxies that you want to use, one per line. For example:

```
127.0.0.1:1080
192.168.0.1:1080

```
Run the script using the following command:

```
python stress.py
```

Follow the prompts to enter the target URL, the HTTP method to use (GET or POST), the number of requests to make, and whether to use a SOCKS5 proxy or write the output to a log file.

If you choose to use a SOCKS5 proxy, enter the proxy host and port when prompted.

If you choose to write the output to a log file, enter the log file name when prompted.

The script will send the requests and print the response status code to the console. If you chose to write the output to a log file, the script will also write the output to the specified file.

## License
This script is licensed under the MIT License. See LICENSE for more information.


You can copy and paste this code into your `README.md` file on Github and then push it to your repository. The resulting file will be formatted with a title, table of contents, and sections, with the code blocks formatted in a way that is easy to read.
