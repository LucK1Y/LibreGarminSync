# LibreGarminSync
LibreGarminSync is an open-source Python tool that effortlessly syncs Garmin FIT files to GPX format. Prioritizing user privacy and freedom, it offers a transparent, hassle-free alternative to proprietary apps, enabling you to manage your fitness data securely and maintain full control over your activity files

## Features

- Copies Fit files from watch to local directory.
- Convert Garmin FIT files to GPX while preserving timestamps and location-data
- Adds elevation data if needed
- Prints a short aggregation of all workouts over the weeks to show trends

<br>
    
- Local, offline processing to protect user privacy
- Small, dependency-light Python implementation with a command-line interface and importable API
- Batch conversion and optional filename / directory organization

## Requirements

- Python
- Typical dependencies managed in requirements.txt (e.g., fitparse, gpxpy).

## Installation

From source:
1. Clone the repository
2. Create a virtual environment and activate it
3. Install requirements:
    - use **make init** or **pip install -r requirements.txt**
    - or pip install .
4. Configure **config.ini** file (default name). Otherwise hand over config filename to cli args
5. If you want to run all tests you will need to specify some example fit files in the test files.

## Command-line usage
```shell
usage: main.py [-h] [-t] [-s] [-o] [-c CONFIG]

LibreGarminSync CLI

options:
  -h, --help            show this help message and exit
  -t, --transform       Transform local fit to gpx
  -s, --sync            Sync remote fit to local
  -o, --overview_training
                        Run overview training task
  -c CONFIG, --config CONFIG
                        Path to the config file. Default: /<Repo>/LibreGarminSync/config.ini
```


## Repository layout (adjust to actual repo)

Typical files and purpose:
- pyproject.toml / setup.py — packaging and dependencies
- requirements.txt — pinned dependencies for development
- src/libregarminsync/ — library source
  - __init__.py — package entry
  - cli.py / __main__.py — command-line interface
  - converters.py — FIT → GPX conversion logic
  - utils.py — helpers (parsing, logging, file handling)
- tests/ — unit and integration tests
- examples/ — example usage and sample commands
- docs/ — extended documentation if present
- Dockerfile — optional container image
- LICENSE — project license

## Development & testing

- Run tests: pytest
- Add tests for new conversion cases (edge-case FIT messages, missing GPS, multi-session files)

## Contributing

- Fork the repo, create a feature branch, add tests, open a pull request
- Follow the existing code style and include changelog notes for user-visible changes
- Be mindful of user privacy — do not add telemetry or external uploads

## Troubleshooting

- If timestamps look wrong, check whether the FIT file contains timezone or timestamp offsets.
- If GPX files are empty, verify the FIT file actually contains GPS trackpoints (some devices record only summary data).

## License

- See LICENSE in repository for terms.
