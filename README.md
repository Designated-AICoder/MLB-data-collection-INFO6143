### Project 02 INFO6143

# MLB Data Collection Project

## Overview

This project is part of the INFO6143 course at Fanshawe College. The goal is to create a Python application that retrieves MLB game data from a public API, processes the JSON data, and outputs the relevant information into a CSV file. This project emphasizes file handling and data extraction techniques in Python.

## Features

- Fetches MLB game data from provided URLs.
- Processes JSON data to extract specific fields.
- Outputs the extracted data into a CSV file with a predefined header.
- Handles multiple dates by reading URLs from a file.

## Requirements

- Python 3.x
- Requests library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Group_07_project02.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Group_07_project02
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the `urls.txt` file in the same directory as your Python script. This file should contain the URLs to fetch data from, one per line.
2. Run the Python script:
   ```bash
   python mlb_data_collection.py
   ```
3. The output CSV file `MLBData.csv` will be generated in the same directory.

## Project Structure

```
Group_07_project02/
├── urls.txt
├── mlb_data_collection.py
├── MLBData.csv
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

Thanks to Fanshawe College and Professor Jim Cooper for the course and project guidance.

````

### `requirements.txt`
```plaintext
requests


### Summary
- **Directory**: `Group_07_project02`
- **Files**: `urls.txt`, `mlb_data_collection.py`, `requirements.txt`, `README.md`
- **Error Handling**: Enhanced for both file reading and network requests.
- **CSV Output**: Created in the same directory with the name `MLBData.csv`.
````
