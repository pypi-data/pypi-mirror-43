import subprocess
import os
import signal


class PubSubRunner:

    def __init__(self):
        self.process = None
        return self

    def start(self, port='8538'):
        port_args = '--host-port=127.0.0.1:{port}'
        self.process = subprocess.Popen(
            " ".join(['gcloud', 'beta', 'emulators', 'pubsub', 'start', port_args]),
            shell=True,
            preexec_fn=os.setsid,
        )
        os.environ['PUBSUB_EMULATOR_HOST'] = f'localhost:{port}'

    def kill(self):
        del os.environ['PUBSUB_EMULATOR_HOST']
        os.killpg(self.process.pid, signal.SIGTERM)
