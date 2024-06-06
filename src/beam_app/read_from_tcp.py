import logging
import socket
import time
import apache_beam as beam


class ReadFromTCP(beam.DoFn):
    def __init__(self, host, port, retries=5, delay=2):
        self.host = host
        self.port = port
        self.retries = retries
        self.delay = delay
        self.client_socket = None
        self.logger = logging.getLogger(__name__)

    def start_bundle(self):
        attempt = 0
        while attempt < self.retries:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                self.logger.info(f"Connected to {self.host}:{self.port}")
                break
            except ConnectionRefusedError as e:
                attempt += 1
                if attempt < self.retries:
                    self.logger.warning(f"Connection attempt {attempt} failed: {e}")
                    time.sleep(self.delay)
                else:
                    self.logger.error(f"Connection attempt {attempt} failed: {e}")
                    raise e

    def process(self, element):
        while True:
            try:
                data = self.client_socket.recv(2048)  # Adjust buffer size as needed
                if data:
                    yield data.decode('utf-8')
            except (ConnectionResetError, BrokenPipeError) as e:
                self.logger.warning(f"Connection lost: {e}")
                self.start_bundle()  # Attempt to reconnect

    def finish_bundle(self):
        if self.client_socket:
            self.client_socket.close()
