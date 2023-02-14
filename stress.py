####################
#
#   By: Slim Jay
#
#
####################

import argparse
import random
import threading
import time

import requests
from tqdm import tqdm


def test_site(url, http_method, num_requests, proxy_list, headers):
    """Test the target site."""
    for i in range(num_requests):
        proxy = {"http": "socks5://" + random.choice(proxy_list)}
        try:
            response = requests.request(http_method, url, proxies=proxy, headers=headers, timeout=5)
            status_code = response.status_code
        except Exception as e:
            status_code = "Error: " + str(e)
        print(f"Request {i + 1}/{num_requests} (Proxy: {proxy['http']}, Status: {status_code})")
        time.sleep(0.5)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to test")
    parser.add_argument("http_method", help="HTTP method to use (GET or POST)", choices=["GET", "POST"])
    parser.add_argument("num_requests", help="Number of requests to send", type=int)
    parser.add_argument("--proxy_file", help="Path to a file containing a list of proxies (one per line)")
    parser.add_argument("--headers_file", help="Path to a file containing custom headers (one per line)")
    args = parser.parse_args()

    # Load proxies
    proxy_list = []
    if args.proxy_file:
        with open(args.proxy_file) as f:
            for line in f:
                proxy = line.strip()
                if ":" not in proxy:
                    print(f"Invalid proxy format: {proxy}. Skipping...")
                    continue
                proxy_list.append(proxy)
    else:
        print("No proxy file specified. Using local IP address...")
        proxy_list.append("127.0.0.1:9050")

    # Load headers
    headers = {}
    if args.headers_file:
        with open(args.headers_file) as f:
            for line in f:
                key, value = line.strip().split(":")
                headers[key] = value
    else:
        print("No headers file specified. Using default headers...")

    # Send multiple requests to the website
    print(f"Sending {args.num_requests} {args.http_method} requests to {args.url}...")
    with tqdm(total=args.num_requests) as pbar:
        for i in range(args.num_requests):
            thread = threading.Thread(target=test_site, args=(args.url, args.http_method, 1, proxy_list, headers))
            thread.start()
            thread.join()
            pbar.update(1)


if __name__ == "__main__":
    main()
