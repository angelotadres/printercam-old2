# Printer Cam

Printer Cam is a user-friendly web application designed to visualize and make webcam video feeds available to Prusa Connect while providing tools to create video time-lapses.

Follow the steps below to set up the project and run it on your local machine.

## Prerequisites

- Python 3.9
- Pipenv

## Installation

Clone the repository:

```bash
Copy code
git clone https://github.com/angelotadres/printercam.git
cd printercam
```

Install dependencies using Pipenv:

```bash
pipenv install
```

## Usage

First, initialize the database with the following command:

```bash
pipenv run flask --app printercam init-db
```

The, run the PrinterCam application:

```bash
pipenv run flask --app printercam run --debug
```

The application will be accessible at <http://localhost:5000> in your web browser.