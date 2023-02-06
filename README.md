# Docker Desktop Installation Script for Mac

This script is designed to check if Docker Desktop is installed on your Mac, and if not, install it from a Docker disk image. The disk image location is configurable using an environment variable.

## Requirements

- Mac with a supported version of macOS (check the Docker Desktop system requirements for the latest information).

## Usage

1. Clone this repository or download the `install_docker.py` script.
2. Set the location of the Docker disk image using the `--path` flag. The default location is `/Users/<username>/Downloads/Docker.dmg`, where `<username>` is the current user's username.
3. Run the script using the command `python install_docker.py`.

The script will check if Docker Desktop is installed and if not, install it using the disk image at the specified location. If Docker Desktop is already installed, the script will print a message indicating that it's already installed.

## Tips

- Run the script regularly using a cron job or similar tool to ensure Docker Desktop is always installed and ready to use.
```
* * * * * /usr/local/bin/python /path/to/install_docker.py
```
To set up this cron job, open a terminal and run the following command, add the cron job above, and save the crontab file:
```
crontab -e
```

## Troubleshooting

- If the script fails to install Docker Desktop, check the error message for any issues.
- If the script reports that Docker Desktop is already installed but you're still having trouble using it, try restarting your Mac or check the Docker Desktop settings for any issues.
