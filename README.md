# Project Initializer Script

A Python script that automatically clones the [Fullstack-boilerplate](https://github.com/Kicchu02/Fullstack-boilerplate.git) repository and executes the appropriate bootstrap file based on your operating system.

**Two versions available:**

- **Command Line Version**: `project_initializer.py` - For automation and scripting
- **GUI Version**: `project_initializer_gui.py` - For easy-to-use graphical interface

## Features

- **Cross-platform compatibility**: Automatically detects Windows, Linux, or macOS
- **Automatic repository cloning**: Clones the latest version of the Fullstack-boilerplate
- **OS-specific bootstrap execution**: Runs the appropriate bootstrap script for your system
- **Smart Git repository handling**: Removes existing Git history and initializes fresh repository
- **Path flexibility**: Supports both relative and absolute paths
- **Input validation**: Comprehensive validation for project names and paths
- **Error handling**: Robust error handling with OS-specific solutions
- **Git dependency checking**: Verifies Git is installed before proceeding

## Prerequisites

- **Python 3.6 or higher**
- **Git** installed and available in your system PATH
- **tkinter** (usually included with Python standard library)

## Usage

### GUI Version (Recommended for most users)

```bash
# Launch the graphical interface
python project_initializer_gui.py
```

The GUI provides:

- **Project Name Input**: Enter your desired project name
- **Path Selection**: Browse and select target directory (supports relative/absolute paths)
- **System Information**: Shows OS detection and Git status
- **Progress Tracking**: Visual progress bar and status updates
- **Auto-fit Window**: Window automatically sizes to fit content
- **User-Friendly**: No command-line knowledge required

### Command Line Version (For automation)

```bash
# Basic usage with two required parameters
python project_initializer.py "Project Name" "Path"

# Examples:
python project_initializer.py "my-app" "C:\Users\username\Projects"
python project_initializer.py "my-project" "C:\Projects"
python project_initializer.py "new-project" "D:\Development"
python project_initializer.py "test-app" "."

# Get help
python project_initializer.py --help
```

**Parameters:**

- **Project Name** (REQUIRED): Name of the project directory to create
- **Path** (REQUIRED): Path where the project directory should be created (can be relative or absolute)

### Windows

```powershell
# Examples:
python project_initializer.py "my-app" "C:\Users\kicch\Dev Drive"
python project_initializer.py "test-project" "."
```

### Linux/macOS

```bash
# Examples:
python3 project_initializer.py "my-app" "/home/username/projects"
python3 project_initializer.py "test-project" "."

# Make executable and run directly
chmod +x project_initializer.py
./project_initializer.py "my-app" "/home/username/projects"
```

## What the Script Does

1. **Validates inputs**: Checks project name and path for validity
2. **Checks prerequisites**: Verifies Git is installed
3. **Detects OS**: Identifies whether you're on Windows, Linux, or macOS
4. **Creates project directory**: Builds the full project path
5. **Clones repository**: Downloads the Fullstack-boilerplate from GitHub
6. **Manages Git repository**:
   - Removes existing Git history using OS-specific commands
   - Initializes fresh Git repository
   - Adds all files and creates initial commit
7. **Executes bootstrap**: Runs the appropriate bootstrap file:
   - Windows: `bootstrap.bat` (using `rmdir /s /q` and PowerShell fallback)
   - Linux/macOS: `rm -rf` with `find` command fallback
8. **Provides feedback**: Shows progress and completion status

## OS-Specific Features

### Windows

- Uses `rmdir /s /q` for Git repository removal
- PowerShell `Remove-Item -Recurse -Force` as fallback
- Executes `bootstrap.bat` with proper shell handling

### Linux/macOS

- Uses `rm -rf` for Git repository removal
- `find` command with `rm` and `rmdir` as fallback
- Executes `bootstrap.sh` with executable permissions

## Output

The script will create a new project directory with your specified name in the target path and execute the bootstrap process. You'll see real-time progress updates and any error messages if something goes wrong.

## Project Structure

After successful execution, you'll have:

```
[Your-Project-Name]/
├── FE/                 # React frontend application
├── WS/                 # Kotlin backend workspace
├── bootstrap.bat       # Windows bootstrap script
├── bootstrap.sh        # Unix bootstrap script
├── README.md           # Project documentation
└── .git/               # Fresh Git repository with initial commit
```

## Troubleshooting

### Git not found

- Install Git from [https://git-scm.com/](https://git-scm.com/)
- Ensure Git is added to your system PATH
