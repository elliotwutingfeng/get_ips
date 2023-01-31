# get_ips

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

[![Codecov Coverage](https://img.shields.io/codecov/c/github/elliotwutingfeng/get_ips?color=bright-green&logo=codecov&style=for-the-badge&token=63a1xj1fbI)](https://codecov.io/gh/elliotwutingfeng/get_ips)

[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)

Get IPv4 and IPv6 addresses of hostnames using [socket.getaddrinfo()](https://docs.python.org/3/library/socket.html#socket.getaddrinfo).

## Requirements

Python 3

## Setup

```shell
pip install -r requirements.txt
```

## Testing

```shell
pytest --cov --cov-report html
```

## Usage

```shell
python main.py --input-file sample_urls.txt --output-file output.txt
```
