import argparse
import platform
import subprocess
import requests
import os


def check_docker():
    docker_app_path = "/Applications/Docker.app"
    if os.path.exists(docker_app_path):
        return True
    else:
        return False


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
        try:
            output = subprocess.check_output("hdiutil info", shell=True).decode("utf-8")
        except Exception as e:
            print("failed to get run hdiutil info")
            print(e)
            return
        lines = output.split("\n")
        for line in lines:
            if volume_name in line:
                volume_path = line.split("\t")[-1]
                break
    # Attach the Docker volume if it's not already attached
    if volume_path is None:
        print(f"Docker image not attached at /Volumes/{volume_name}")
        if not dry_run:
            try:
                subprocess.check_output(f"hdiutil mount {path}", shell=True)
            except Exception as e:
                print(f"failed to mount docker installer image at /Volumes/{volume_name}")
                print(e)
                return
            print(f"hdiutil attach {path}")
    else:
        print("Docker volume already attached at:", path)

    if not dry_run:
        print("Installing docker from the mounted volume")
        os.chdir("/Volumes/Docker")
        try:
            subprocess.check_output("./Docker.app/Contents/MacOS/install", shell=True)
        except Exception as e:
            print("failed to install docker")
            print(e)
            return

    print("cd /Volumes/Docker")
    print("./Docker.app/Contents/MacOS/Docker/install")
    print("Docker has been installed")


if __name__ == '__main__':
    print("-----start docker installer-----")
    parser = argparse.ArgumentParser(description='Check and install Docker Desktop for Mac')
    parser.add_argument('-p', '--path', help='Path to save Docker.dmg', default='/Users/' + os.getlogin() + '/Downloads/Docker.dmg')
    parser.add_argument('-d', '--dry-run', help='Print actions that would be taken', action='store_true')
    args = parser.parse_args()

    path = args.path
    print(f"using image path: {path}")

    dry_run = args.dry_run
    if dry_run:
        print("running the command with the --dry-run flag")
    if check_docker():
        print('Docker is already installed')
    else:
        print("Docker is not installed")
        download_docker_dmg(path, dry_run)
        install_docker(path, dry_run)
    print("-----end docker installer-----")
