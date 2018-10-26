import os
import pytest
import shutil
import socket

TMP_DIR = os.path.join(os.getcwd(), 'tmp/tests')

def pytest_runtest_setup():
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    os.makedirs(TMP_DIR)
    def block_socket(*args, **kwargs):
        raise Exception('socket not allowed in test mode')
    socket.socket = block_socket
