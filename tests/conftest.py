import pytest
import shutil
import socket

def pytest_runtest_setup():
    shutil.rmtree('tmp', ignore_errors=True)

    def block_socket(*args, **kwargs):
        raise Exception('socket not allowed in test mode')
    socket.socket = block_socket
