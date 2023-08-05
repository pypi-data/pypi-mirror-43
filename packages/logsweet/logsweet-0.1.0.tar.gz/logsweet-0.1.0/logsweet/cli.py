# _*_ coding: utf-8 _*_
"""
This module provides the CLI for the tool.
"""

import click
import socket
from .core import write_logfiles, watch_and_send, listen_and_print, \
    proxy as proxy_messages


@click.group(help='A suite with a variety of tools for handling log messages.')
def main():
    pass


@main.command(help='Generate random log file entries.')
@click.option('-i', '--interval', type=float, default=0.5,
              help='The interval for entry generation in seconds.')
@click.option('-n', '--max-lines', type=int, default=None,
              help='The number of log messages to generate.')
@click.argument('logfiles', nargs=-1)
def mock(logfiles, interval, max_lines):
    write_logfiles(logfiles, interval=interval, max_n=max_lines)


@main.command(help='Follow logfiles '
                   'and send new lines via ZeroMQ PUB and/or PUSH socket.')
@click.option('-b', '--bind-address', type=str, default=None,
              help='IP and port to bind the ZeroMQ PUB socket.')
@click.option('-c', '--connect-address', type=str, multiple=True,
              help='Hostname(s) or IP(s) with port to connect the '
                   'ZeroMQ PUSH socket.')
@click.option('-cfg', '--config-file',
              type=click.Path(exists=True, resolve_path=True,
                              file_okay=True, dir_okay=False,
                              readable=True),
              help='A configuration file (YAML).')
@click.option('-x', '--exec-actions', is_flag=True,
              help='Activates the execution of action rules '
                   'from the configuration.')
@click.option('-a', '--all-lines', is_flag=True,
              help='Broadcast all existing content before following.')
@click.option('-t', '--tail-lines', type=int, default=0,
              help='Number of tail lines to broadcast before following.')
@click.option('-e', '--encoding', type=str, default=None,
              help='Encoding for reading the text files.')
@click.option('-n', '--name', type=str, default=None,
              help='The source name for the watched logs.')
@click.option('--echo', is_flag=True,
              help='Print events to the console.')
@click.argument('file-glob')
def watch(file_glob, bind_address, connect_address,
          config_file, exec_actions,
          all_lines, tail_lines, encoding,
          name, echo):
    if bind_address is None and not connect_address:
        bind_address = '127.0.0.1:9000'
    watch_and_send(file_glob,
                   bind_address=bind_address,
                   connect_addresses=connect_address,
                   config_file=config_file,
                   exec_actions=exec_actions,
                   all_lines=all_lines,
                   tail_lines=tail_lines,
                   encoding=encoding,
                   name=name or socket.gethostname(),
                   echo=echo)


@main.command(help='Listen to text lines with ZeroMQ SUB and/or PULL socket.')
@click.option('-b', '--bind-address', type=str, default=None,
              help='IP and port to bind the ZeroMQ PULL socket.')
@click.option('-c', '--connect-address', type=str, multiple=True,
              help='Hostname(s) or IP(s) with port to connect '
                   'the ZeroMQ SUB socket.')
@click.option('-cfg', '--config-file',
              type=click.Path(exists=True, resolve_path=True,
                              file_okay=True, dir_okay=False,
                              readable=True),
              help='A configuration file (YAML).')
@click.option('-x', '--exec-actions', is_flag=True,
              help='Activates the execution of action rules '
                   'from the configuration.')
def listen(bind_address, connect_address, config_file, exec_actions):
    listen_and_print(bind_address=bind_address,
                     connect_addresses=connect_address,
                     config_file=config_file,
                     exec_actions=exec_actions)


@main.command(help='Run a log proxy between watchers and listeners. '
                   'Allowing listeners and watchers to come and go. '
                   'Supporting a high availability architecture '
                   'with multiple proxies.')
@click.option('-bb', '--backend-bind-address', type=str, default=None,
              help='The IP and port to bind a ZeroMQ PULL socket for '
                   'collecting log messages from watchers or other proxies.')
@click.option('-bc', '--backend-connect-address', type=str, multiple=True,
              help='Hostname(s) or IP(s) with port to connect a '
                   'ZeroMQ SUB socket '
                   'for receiving log messages from watchers '
                   'or other proxies.')
@click.option('-fb', '--frontend-bind-address', type=str, default=None,
              help='The IP and port to bind the PUB socket for '
                   'broadcasting log messages to listeners or other proxies.')
@click.option('-fc', '--frontend-connect-address', type=str, multiple=True,
              help='Hostname(s) or IP(s) with port to connect a '
                   'ZeroMQ PUSH socket '
                   'for transmitting log messages to a listener '
                   'or other proxies.')
def proxy(backend_bind_address,
          backend_connect_address,
          frontend_bind_address,
          frontend_connect_address):

    if backend_bind_address is None and not backend_connect_address:
        backend_bind_address = '127.0.0.1:9001'
    if frontend_bind_address is None and not frontend_connect_address:
        frontend_bind_address = '127.0.0.1:9002'

    proxy_messages(backend_bind_address=backend_bind_address,
                   backend_connect_addresses=backend_connect_address,
                   frontend_bind_address=frontend_bind_address,
                   frontend_connect_addresses=frontend_connect_address)


if __name__ == '__main__':
    main()
