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

    def start_bundle(self):
        attempt = 0
        while attempt < self.retries:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                print(f"Connected to {self.host}:{self.port}")
                break
            except ConnectionRefusedError as e:
                attempt += 1
                print(f"Connection attempt {attempt} failed: {e}")
                if attempt < self.retries:
                    time.sleep(self.delay)
                else:
                    raise e

    def process(self, element):
        while True:
            try:
                data = self.client_socket.recv(2048)  # Adjust buffer size as needed
                if data:
                    yield data.decode('utf-8')
            except (ConnectionResetError, BrokenPipeError) as e:
                print(f"Connection lost: {e}")
                self.start_bundle()  # Attempt to reconnect

    def finish_bundle(self):
        if self.client_socket:
            self.client_socket.close()
