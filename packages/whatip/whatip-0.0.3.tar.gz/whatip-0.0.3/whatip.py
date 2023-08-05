try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
import re
from argparse import ArgumentParser
import sys
import logging
import socket
from threading import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

VERSION = '0.0.3'
SOURCES = ['ipapi', 'formyip']


def parse_cli():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--only-ip', action='store_true', default=False,
        help='display only IP',
    ) 
    parser.add_argument(
        '-s', '--source', choices=SOURCES,
        help='use specific source',
    )
    return parser.parse_args()


def parse_formyip():
    data = urlopen('http://formyip.com').read().decode('utf-8')
    ip = re.search(r'Your IP is ([^<]*)', data).group(1)
    cnt = re.search(r'Your Country is: ([^<]*)', data).group(1)
    return ip, cnt


def parse_ipapi():
    data = urlopen('http://ip-api.com/json').read().decode('utf-8')
    ip = re.search(r'query":"(.+?)"', data).group(1)
    cnt = re.search(r'country":"(.+?)"', data).group(1)
    return ip, cnt


def worker_parser(parser, resultq):
    try:
        ip, cnt = parser()
    except Exception as ex:
        logging.error('Failed to parse %s source: %s' % (source, ex))
    else:
        resultq.put((ip, cnt))


def main(**kwargs):
    logging.basicConfig(level=logging.DEBUG)
    socket.setdefaulttimeout(5)
    opts = parse_cli()
    if opts.source in SOURCES:
        sources = [opts.source]
    else:
        sources = SOURCES
    ip, cnt = None, None
    pool = []
    resultq = Queue()
    for source in sources:
        func = globals()['parse_%s' % source]
        th = Thread(target=worker_parser, args=[func, resultq])
        th.start()
        pool.append(th)

    ip = None
    while sum(1 for x in pool if x.is_alive()):
        try:
            ip, cnt = resultq.get(False, 0.1)
        except Empty:
            pass
        else:
            break
    if not ip and resultq.qsize():
        ip, cnt = resultq.get()

    if ip is None:
        logging.error('Fatal error: all sources failed')
        sys.exit(1)
    if opts.only_ip:
        print(ip)
    else:
        print('%s %s' % (ip, cnt))


if __name__ == '__main__':
    main()
