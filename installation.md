# Module 2 First-Time Software Installation

## Hardware Requirements
- Desktop/laptop computer running the latest version of macOS/Linux/Windows operating system (OS)
- Recommended 16GB onboard memory (RAM) 
- Recommended 50GB available hard disk storage space (HDD/SSD)
- Webcam and microphone for online Zoom sessions

## Software Requirements

- WSL (for Windows users only)
- Visual Studio Code (VSCode) or any source code editor
- Git Command-Line Interface (CLI)
- Conda/Miniconda

## Conda Environments

Install conda environments required for the rest of module. Go to the `environments` folder and create the conda environments based on the `environment.yml` file. Each `yml` file is prefixed with the environment name. 

For example, to create the `bde` environment, first navigate into the `environments` folder by running `cd environments`, then run the following command:

`conda env create --file bde-environment.yml`

To replace an existing environment:

`conda env update --file bde-environment.yml --prune`

### Environments

Create all the environments in the `environments` folder at this point. 

Here is where the environments will be used:
- `bde`: Lesson 2.1 onwards
- `elt`: Lesson 2.5 onwards
- `dagster`: Lesson 2.6 onwards
- `ooc`: Lesson 2.7
- `kafka`: Lesson 2.10

Please prepare your environments before each lesson. Reach out to your cohort of Discord if you have any questions.

### For Windows WSL Users

If you get an error message when creating the `bde` environment, e.g.
> ERROR: Could not build wheels for thriftpy2, which is required to install pyproject.toml-based projects.

Run the following CLI command from your terminal:

`sudo apt install build-essential`
