# Scripts Organizer

## Overview
The **Scripts Organizer** is a Python-based tool designed to help manage and organize various scripts. Whether you’re dealing with large collections of scripts or simply need an efficient way to group and categorize them, this tool provides a streamlined solution.

## Features
- Organize scripts by type, functionality, or custom categories.
- Automatically group scripts based on file extensions.
- Create directories for categorized scripts for better accessibility.
- Easy to extend for additional organization logic.

## Requirements
- Python 3.7+
- Required Python libraries:
  - `os`
  - `shutil`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/membaby/scripts-organizer.git
   cd scripts-organizer
   ```

2. Ensure Python is installed on your system. Verify the version:
   ```bash
   python --version
   ```

3. Install additional dependencies (if needed).

## Usage
1. Place the scripts you want to organize in the designated folder or specify the directory in the script.
2. Run the `scripts_organizer.py` file:
   ```bash
   python scripts_organizer.py
   ```
3. Organized scripts will be moved into categorized directories within the specified location.

### Customization
- **Change categories:**
  Update the categorization logic in the script to group scripts based on your specific needs, such as by:
  - Programming language (e.g., `.py`, `.js`, `.sh`).
  - Purpose (e.g., `data_analysis`, `automation`).

- **Destination directory:**
  Modify the script to change the default directory where organized scripts are saved.

## Code Structure
1. **File categorization:**
   The script scans a directory for files and organizes them based on predefined rules (e.g., file extension).

2. **Directory creation:**
   Creates subdirectories for each category if they do not exist.

3. **File movement:**
   Moves each file to its corresponding directory.

## Example
If the input folder contains:
```
data_analysis.py
automation_tool.sh
web_scraper.js
```
After running the script, the directory might look like:
```
organized_scripts/
  Python/
    data_analysis.py
  Shell_Scripts/
    automation_tool.sh
  JavaScript/
    web_scraper.js
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Inspired by the need to keep large collections of scripts tidy.
- Thanks to the Python community for providing excellent libraries and resources.
