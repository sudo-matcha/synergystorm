# SynergyStorm

![SynergyStorm Logo](./synergystorm_logo_banner.png)

SynergyStorm is a command-line client designed to de-jank the SynergyVue user experience (and for being a bit evil).

## Installation

### Installation using a Release

SynergyStorm is available as either a standalone Python Script or a binary for unix-like systems.
Just download either from the latest release and enjoy!
(just make sure to install dependencies)

### Installing from Cloned Repo

1. **Clone the Repository:**

```bash
git clone https://github.com/sudo-matcha/synergystorm.git
```

2. **Navigate to the Directory:**

```bash
cd synergystorm
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```
4. **Install the Binary**

```bash
sudo cp ./dist/synergystorm/synergystorm /usr/bin
```
**...or use `install.sh`** (this method will always emulate all installation steps needed after cloning)
```bash
chmod +x ./install.sh && ./install.sh
```

## Usage

```
usage: synergystorm [-h] [--version] [-id [ID]] [--password [PASSWORD]] [--show_webdriver]

A command-line client for making some features of SynergyVue better (and for being a little evil).

optional arguments:
  -h, --help            show this help message and exit
  --version             display the version number and exit
  -id [ID]              Provide a student ID for authentication (requires --password)
  --password [PASSWORD], -p [PASSWORD]
                        Provide a password for authentication (required by -id)
  --show_webdriver, -W  Show Selenium Webdriver instance (removes '--headless' argument)
```

## Features

- **Secure Login System**: Log into SynergyVue from the command-line securely. Entered credentials are not saved to the system.
- **Hall Pass Creation**: Generate hall passes with ease.

## Examples

### Preemptive login with Student ID and Password:

```bash
synergystorm -id YOUR_STUDENT_ID -p YOUR_PASSWORD
```

## Note

This script is for educational purposes only. Use it responsibly and do not violate any terms of service.

## Credits

- **Author**: sudo-matcha
- **Version**: 2.4.1
- **License**: GNU GPL v3

## Support

For any issues or queries, please [open an issue](https://github.com/sudo-matcha/synergystorm/issues). Contributions are welcome!
