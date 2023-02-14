import requests
import pyproxy

# Prompt the user to enter the target URL
url = input("Enter the target URL: ")

# Prompt the user to enter the HTTP method to use
http_method = input("Enter the HTTP method (GET or POST): ")

# Prompt the user to enter the number of requests to make
num_requests = int(input("Enter the number of requests to make: "))

# Read the list of SOCKS5 proxies from a file
with open("proxy_list.txt", "r") as f:
    proxy_list = [line.strip() for line in f if line.strip()]

# Send a request `num_requests` times using the specified HTTP method and proxy (if any)
session = requests.Session()
for i in range(num_requests):
    proxy_host = proxy_list[i % len(proxy_list)]
    proxy = pyproxy.Socks5Proxy(host=proxy_host, port=1080)
    proxies = {
        "http": f"socks5://{proxy_host}:1080",
        "https": f"socks5://{proxy_host}:1080",
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
        print(log_message, end="")

# Prompt the user to enter the log file name (optional)
use_log = input("Do you want to write the output to a log file? (Y/N): ")
if use_log.upper() == "Y":
    log_filename = input("Enter the log file name: ")
    with open(log_filename, "w") as f:
        for i in range(num_requests):
            proxy_host = proxy_list[i % len(proxy_list)]
            proxy = pyproxy.Socks5Proxy(host=proxy_host, port=1080)
            proxies = {
                "http": f"socks5://{proxy_host}:1080",
                "https": f"socks5://{proxy_host}:1080",
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
                f.write(log_message)

# Print a message indicating where the log file is located (if any)
if use_log.upper() == "Y":
    print(f"Log file written to {log_filename}")
