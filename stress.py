####################
#
#   By: Slim Jay
#
#
####################

import requests
import cloudscraper
from tqdm import tqdm
import itertools

# Prompt the user to enter the target URL
url = input("Enter the target URL: ")

# Prompt the user to enter the HTTP method to use
http_method = input("Enter the HTTP method (GET or POST): ")

# Prompt the user to enter the number of requests to make
num_requests = int(input("Enter the number of requests to make: "))

# Prompt the user to enter a file path that contains the list of proxies (optional)
proxy_file = input("Enter the file path that contains the list of proxies to use (leave blank for no proxies): ")
if proxy_file:
    with open(proxy_file, "r") as f:
        proxy_list = [line.strip() for line in f if line.strip()]
else:
    proxy_list = []

# Use the proxies in a round-robin fashion
proxy_cycle = itertools.cycle(proxy_list)

# Prompt the user to enter whether the website is behind Cloudflare (optional)
use_cloudflare = input("Is the website behind Cloudflare? (Y/N): ")
if use_cloudflare.upper() == "Y":
    scraper = cloudscraper.create_scraper()
    use_cloudscraper = True
else:
    session = requests.Session()
    use_cloudscraper = False

# Prompt the user to enter the log file name (optional)
use_log = input("Do you want to write the output to a log file? (Y/N): ")
if use_log.upper() == "Y":
    log_filename = input("Enter the log file name: ")
    log_file = open(log_filename, "w")
else:
    log_file = None

# Send a request `num_requests` times using the specified HTTP method and proxy (if any)
for i in tqdm(range(num_requests), desc="Sending requests", unit="req"):
    if use_cloudscraper:
        if proxy_list:
            proxy = next(proxy_cycle)
            proxies = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}",
            }
            response = scraper.request(http_method, url, proxies=proxies)
        else:
            response = scraper.request(http_method, url)
    else:
        if proxy_list:
            proxy = next(proxy_cycle)
            proxies = {
                "http": f"socks5://{proxy}",
                "https": f"socks5://{proxy}",
            }
            session.proxies = proxies
            with session:
                if http_method.upper() == "GET":
                    response = session.get(url)
                elif http_method.upper() == "POST":
                    response = session.post(url)
                else:
                    print("Invalid HTTP method. Please enter GET or POST.")
                    break
        else:
            if http_method.upper() == "GET":
                response = requests.get(url)
            elif http_method.upper() == "POST":
                response = requests.post(url)
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
