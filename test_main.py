from ipaddress import IPv4Address, IPv6Address, ip_address
from tempfile import NamedTemporaryFile

from main import extract_fqdns, get_addr_info, get_ip_type, parse_args, write_ip_list

input_filename = "sample_urls.txt"


def test_get_ip_type():
    assert get_ip_type("0.0.0.1") is IPv4Address
    assert get_ip_type("2f5c:44df:a1f9:4635:4d65:74df:2848:d659") is IPv6Address
    assert get_ip_type("42") is None


def test_extract_fqdns():
    assert extract_fqdns(input_filename) == [
        "example.com",
        "example.org",
        "icann.org",
        "www.w3.org",
    ]


def test_get_addr_info():
    fqdns = extract_fqdns(input_filename) + ["example.noexist"]
    results = get_addr_info(fqdns)
    for result in results:
        if result is not None:
            assert result.fqdn != ""
            if result.ipv4_addresses:
                assert isinstance(ip_address(result.ipv4_addresses[0]), IPv4Address)
            if result.ipv6_addresses:
                assert isinstance(ip_address(result.ipv6_addresses[0]), IPv6Address)


def test_write_ip_list():
    with NamedTemporaryFile() as tf:
        fqdns = extract_fqdns(input_filename) + ["example.noexist"]
        results = get_addr_info(fqdns)
        output_filename = tf.name
        write_ip_list(output_filename, results)
        tf.seek(0)
        content = tf.read().decode().splitlines()
        assert content[0] == "# example.com"
        assert isinstance(ip_address(content[1]), IPv4Address)


def test_parser():
    parser = parse_args(["-i", "sample_urls.txt", "-o", "output.txt"])
    assert parser.input_file
    assert parser.output_file
