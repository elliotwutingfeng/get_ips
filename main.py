import logging
import socket
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
    RawTextHelpFormatter,
)
from collections import namedtuple
from ipaddress import IPv4Address, IPv6Address, ip_address
from queue import Queue
from threading import Thread

import tldextract


class CustomFormatter(
    RawTextHelpFormatter,
    RawDescriptionHelpFormatter,
    ArgumentDefaultsHelpFormatter,
):
    """Custom Help text formatter for argparse."""


def get_ip_type(address):
    try:
        ip = ip_address(address)
        if isinstance(ip, IPv4Address):
            return IPv4Address
        if isinstance(ip, IPv6Address):
            return IPv6Address
    except ValueError:
        return None


def extract_fqdns(filename):
    with open(filename, "r") as f:
        urls = f.read().splitlines()
        fqdns = sorted(
            list(
                set(
                    fqdn for url in urls if (fqdn := tldextract.extract(url).fqdn) != ""
                )
            )
        )
    return fqdns


def get_addr_info(fqdns):
    results = [None] * len(fqdns)

    fqdn_addr_info = namedtuple(
        "fqdn_addr_info", ["fqdn", "ipv4_addresses", "ipv6_addresses"]
    )

    def getips(queue):
        for index, fqdn in iter(queue.get, None):
            try:  # resolve fqdn
                addrinfo = socket.getaddrinfo(fqdn, None)
            except IOError as e:
                logging.warning("error %s reason: %s", fqdn, e)
            else:
                ipv4_ips = set()
                ipv6_ips = set()
                for entry in addrinfo:
                    maybe_ip = entry[4][0]
                    ip_type = get_ip_type(maybe_ip)
                    if ip_type is IPv4Address:
                        ipv4_ips.add(maybe_ip)
                    if ip_type is IPv6Address:
                        ipv6_ips.add(maybe_ip)
                results[index] = fqdn_addr_info(
                    fqdn,
                    sorted(list(ipv4_ips), key=IPv4Address),
                    sorted(list(ipv6_ips), key=IPv6Address),
                )

    queue = Queue()
    threads = [Thread(target=getips, args=(queue,)) for _ in range(8)]
    for t in threads:
        t.daemon = True
        t.start()

    for index, site in enumerate(fqdns):
        queue.put((index, site))

    # sentinel values
    for _ in threads:
        queue.put(None)

    for t in threads:
        t.join()
    return results


def write_ip_list(filename, results):
    with open(filename, "a") as f:
        for result in results:
            if result is None:
                continue
            f.write("# " + result.fqdn + "\n")
            for ipv4_address in result.ipv4_addresses:
                f.write(ipv4_address + "\n")
            for ipv6_address in result.ipv6_addresses:
                f.write(ipv6_address + "\n")


def parse_args(args):
    parser = ArgumentParser(
        description="""
    Get IPv4 and IPv6 addresses of hostnames using socket.getaddrinfo().

    For example, `python main.py --input-file sample_urls.txt --output-file output.txt`
    calls socket.getaddrinfo() for every hostname in `sample_urls.txt`
    and writes its associated IPv4 and IPv6 addresses to `output.txt`.
    """,
        formatter_class=CustomFormatter,
        # Disallows long options to be abbreviated
        # if the abbreviation is unambiguous
        allow_abbrev=False,
    )

    parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        help="""
        Path to text file containing URLs.
        """,
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        help="""
        Path to output text file where IPv4 and IPv6 addresses are to be stored.
        """,
        type=str,
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    parser = parse_args(sys.argv[1:])

    fqdns = extract_fqdns(parser.input_file)
    results = get_addr_info(fqdns)
    write_ip_list(parser.output_file, results)
