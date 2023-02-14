####################
#
#   By: Slim Jay
#
#
####################

import requests
import pyproxy
from tqdm import tqdm
import itertools

# Prompt the user to enter the target URL
url = input("Enter the target URL: ")

# Prompt the user to enter the HTTP method to use
http_method = input("Enter the HTTP method (GET or POST): ")

# Prompt the user to enter the number of requests to make
num_requests = int(input("Enter the number of requests to make: "))

# Read the list of SOCKS5 proxies from a file
with open("proxy_list.txt", "r") as f:
    proxy_list = [line.strip() for line in f if line.strip()]

# Use the proxies in a round-robin fashion
proxy_cycle = itertools.cycle(proxy_list)

# Prompt the user to enter the log file name (optional)
use_log = input("Do you want to write the output to a log file? (Y/N): ")
if use_log.upper() == "Y":
    log_filename = input("Enter the log file name: ")
    log_file = open(log_filename, "w")
else:
    log_file = None

# Send a request `num_requests` times using the specified HTTP method and proxy (if any)
session = requests.Session()
for i in tqdm(range(num_requests), desc="Sending requests", unit="req"):
    proxy_host, proxy_port = next(proxy_cycle).split(":")
    proxy = pyproxy.Socks5Proxy(host=proxy_host, port=int(proxy_port))
    proxies = {
        "http": f"socks5://{proxy_host}:{proxy_port}",
        "https": f"socks5://{proxy_host}:{proxy_port}",
    }
    session.proxies = proxies
    with pyproxy.route(session, proxy):
        if http_method.upper() == "GET":
            response = session.get(url)
        elif http_method.upper() == "POST":
            response = session.post(url)
        else:
            print("Invalid HTTP method. Please enter GET or POST.")
            break
        log_message = f"Request {i+1}: {response.status_code}\n"
        if log_file:
            log_file.write(log_message)
        tqdm.write(log_message)

# Close the log file (if any)
if log_file:
    log_file.close()
    print(f"Log file written to {log_filename}")
