import argparse
import platform
import subprocess
import requests
import os
import shutil


def check_docker():
    if shutil.which("docker") is None:
        return False
    else:
        return True


def download_docker_dmg(path, dry_run=False):
    """Downloads Docker Desktop for Mac

    path - path to store image
    dry_run - if True, only print actions without actually downloading
    """
    # Define the URL to download Docker Desktop
    if os.path.exists(path):
        print(f"Image already exists for Docker desktop at {path}")
        return

    architecture = platform.machine()
    if architecture == 'x86_64':
        uri = 'https://desktop.docker.com/mac/main/amd64/Docker.dmg'
    elif architecture == 'arm64':
        uri = 'https://desktop.docker.com/mac/main/arm64/Docker.dmg'
    else:
        raise Exception(f"Unknown architecture {architecture}")

    # Download the Docker Desktop disk image
    if not dry_run:
        response = requests.get(uri)
        with open(path, "wb") as f:
            f.write(response.content)
    print(f'Downloaded Docker Desktop for {architecture} from {uri}.')


def install_docker(path, dry_run=False):
    volume_name = "Docker"
    volume_path = None
    # Check if the Docker volume is already attached
    if not dry_run:
        output = subprocess.check_output(["hdiutil", "info"]).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if volume_name in line:
                volume_path = line.split("\t")[-1]
                break
    else:
        print("hdiutil info")

    # Attach the Docker volume if it's not already attached
    if volume_path is None:
        if not dry_run:
            output = subprocess.check_output(["hdiutil", "attach", path, "-mountpoint", "/Volumes/Docker"]).decode("utf-8")
            lines = output.split("\n")
            for line in lines:
                if "Apple_HFS" in line:
                    volume_path = line.split("\t")[0]
                    break
        else:
            print(" ".join(["hdiutil", "attach", path, "-mountpoint", "/Volumes/Docker"]))
    else:
        print("Docker volume already attached at:", path)
    print("Docker has been installed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check and install Docker Desktop for Mac')
    parser.add_argument('-p', '--path', help='Path to save Docker.dmg', default='/Users/' + os.getlogin() + '/Downloads/Docker.dmg')
    parser.add_argument('-d', '--dry-run', help='Print actions that would be taken', action='store_true')
    args = parser.parse_args()

    path = args.path
    dry_run = args.dry_run

    if check_docker():
        print('Docker is already installed')
    else:
        print("Docker is not installed")
        download_docker_dmg(path, dry_run)
        install_docker(path, dry_run)
