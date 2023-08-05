import subprocess

from onepanel.utilities.s3.authentication import Provider


class CLIWrapper:
    def __init__(self, credentials_provider=None, retry=3):
        """
        :param credentials_provider: Provides credentials for requests.
        :type credentials_provider: onepanel.lib.s3.authentication.Provider
        """
        if credentials_provider is None:
            credentials_provider = Provider()

        self.credentials_provider = credentials_provider
        self.retry = retry
        self.retries = 0

    def run(self, *args, **kwargs):
        print('inside cli wrapper. env is', kwargs['env'])
        # TODO on failure retry with creds...
        p = subprocess.Popen(kwargs)

        output = ""
        err = ""

        for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
            output += line.decode()
        for line in iter(p.stderr.readline, '' or b''):  # replace '' with b'' for Python 3
            err += line.decode()

        return 0, output, err
