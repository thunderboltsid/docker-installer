import argparse
import platform
import subprocess
import sys

def check_docker():
    try:
        output = subprocess.check_output(["docker", "info"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_docker(volume_path, dry_run=False):
    if check_docker():
        print('Docker is already installed')
        return

    architecture = platform.architecture()[0]
    if architecture == '64bit':
        uri = 'https://desktop.docker.com/mac/main/amd64/Docker.dmg'
    else:
        uri = 'https://desktop.docker.com/mac/main/arm64/Docker.dmg'

    if not dry_run:
        subprocess.run(["curl", "-o", volume_path, uri])
    else:
        print(f'curl -o {volume_path} {uri}')

    # check if Docker volume is already attached
    attached_volumes = subprocess.check_output(["hdiutil", "info"]).decode()
    if f'/Volumes/Docker' in attached_volumes:
        print(f'Docker volume is already attached at /Volumes/Docker')
        return

    if not dry_run:
        subprocess.run(["hdiutil", "attach", volume_path])
    else:
        print(f'hdiutil attach {volume_path}')

    # check if Docker.app is already installed
    app_path = '/Applications/Docker.app'
    if check_docker():
        print(f'Docker is already installed at {app_path}')
        return

    if not dry_run:
        subprocess.run(["cp", "-r", "/Volumes/Docker/Docker.app", app_path])
    else:
        print(f'cp -r /Volumes/Docker/Docker.app {app_path}')

    print(f'Docker has been installed at {app_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check and install Docker Desktop for Mac')
    parser.add_argument('-p', '--path', help='Path to save Docker.dmg', default='~/Downloads/Docker.dmg')
    parser.add_argument('-d', '--dry-run', help='Print actions that would be taken', action='store_true')
    args = parser.parse_args()

    volume_path = args.path
    dry_run = args.dry_run
    install_docker(volume_path, dry_run)