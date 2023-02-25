import os
import subprocess


class Mkdk:

    _DEFAULT_PS_FORMAT = 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}'
    _PS_FORMAT = os.environ.get('MKIE_PS_FORMAT', _DEFAULT_PS_FORMAT)

    @classmethod
    def ps(cls, format, pattern):
        format = format or cls._PS_FORMAT
        cmd = ['docker', 'ps', '--format', format]

        if pattern:
            cmd.extend(['--filter', f'name={pattern}'])

        subprocess.run(cmd)

    @classmethod
    def build(cls):
        subprocess.run('docker-compose build', shell=True)

    @classmethod
    def up(cls):
        subprocess.run('docker-compose up -d', shell=True)

    @classmethod
    def down(cls):
        subprocess.run('docker-compose down', shell=True)
