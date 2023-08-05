import subprocess
import os
import signal


class PubSubRunner:

    def __init__(self):
        self.process = None

    def start(self, port='8538'):
        self.process = subprocess.Popen(
            ['gcloud', 'beta', 'emulators', 'pubsub', 'start'],
            stdout=subprocess.DEVNULL,
        )
        os.environ['PUBSUB_EMULATOR_HOST'] = f'localhost:{port}'

    def kill(self):
        del os.environ['PUBSUB_EMULATOR_HOST']
        os.killpg(self.process.pid, signal.SIGTERM)
