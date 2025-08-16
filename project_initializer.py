#!/usr/bin/env python3
"""
Project Initializer Script
Clones the Fullstack-boilerplate repository and executes the appropriate bootstrap file
based on the operating system (Windows or Linux/Mac).
"""

import os
import sys
import subprocess
import platform
import shutil
import argparse
from pathlib import Path


def check_git_installed():
    """Check if git is installed and available in PATH."""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def clone_repository(repo_url, target_dir):
    """Clone the repository to the target directory."""
    print(f"Cloning repository from {repo_url}...")
    
    # Ensure target_dir is a proper path
    if not os.path.isabs(target_dir):
        # If it's a relative path, make it absolute relative to current directory
        target_dir = os.path.abspath(target_dir)
    
    print(f"Target directory: {target_dir}")
    
    if os.path.exists(target_dir):
        print(f"Directory {target_dir} already exists. Removing it...")
        try:
            shutil.rmtree(target_dir)
        except PermissionError as e:
            print(f"Error: Cannot remove existing directory {target_dir}: {e}")
            print("Please close any applications using this directory and try again.")
            return False
        except Exception as e:
            print(f"Error removing directory: {e}")
            return False
    
    try:
        # Clone with verbose output
        result = subprocess.run(['git', 'clone', '--verbose', repo_url, target_dir], 
                              check=True, capture_output=True, text=True)
        print(f"Repository cloned successfully to {target_dir}")
        
        # Verify the clone actually worked
        if os.path.exists(target_dir) and os.listdir(target_dir):
            items = os.listdir(target_dir)
            print(f"Cloned {len(items)} items: {', '.join(items[:5])}{'...' if len(items) > 5 else ''}")
            
            # Remove existing Git repository and initialize new one
            print("Removing existing Git repository...")
            git_dir = os.path.join(target_dir, '.git')
            if os.path.exists(git_dir):
                try:
                    # Use OS-specific commands to remove Git repository
                    if platform.system().lower() == "windows":
                        # Windows: Use rmdir with /s /q for recursive deletion
                        subprocess.run(['rmdir', '/s', '/q', git_dir], shell=True, check=True, capture_output=True)
                        print("Existing Git repository removed successfully (Windows)")
                    else:
                        # Linux/Mac: Use rm -rf
                        subprocess.run(['rm', '-rf', git_dir], check=True, capture_output=True)
                        print("Existing Git repository removed successfully (Unix)")
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Could not remove existing Git repository: {e}")
                    # Try alternative method
                    try:
                        if platform.system().lower() == "windows":
                            # Windows: Force delete using PowerShell
                            ps_command = f'Remove-Item -Path "{git_dir}" -Recurse -Force'
                            subprocess.run(['powershell', '-Command', ps_command], check=True, capture_output=True)
                            print("Existing Git repository removed successfully (PowerShell)")
                        else:
                            # Linux/Mac: Use find and rm
                            subprocess.run(['find', git_dir, '-type', 'f', '-exec', 'rm', '-f', '{}', '+'], check=True, capture_output=True)
                            subprocess.run(['find', git_dir, '-type', 'd', '-exec', 'rmdir', '{}', '+'], check=True, capture_output=True)
                            print("Existing Git repository removed successfully (find/rm)")
                    except Exception as e2:
                        print(f"Warning: Alternative removal method also failed: {e2}")
                        print("Continuing with existing Git repository...")
            
            # Initialize new Git repository
            print("Initializing new Git repository...")
            try:
                subprocess.run(['git', 'init'], cwd=target_dir, check=True, capture_output=True, text=True)
                print("New Git repository initialized successfully")
                
                # Add all files to the new repository
                subprocess.run(['git', 'add', '.'], cwd=target_dir, check=True, capture_output=True, text=True)
                print("All files added to new Git repository")
                
                # Make initial commit
                subprocess.run(['git', 'commit', '-m', 'Initial commit from Fullstack-boilerplate'], 
                             cwd=target_dir, check=True, capture_output=True, text=True)
                print("Initial commit created successfully")
                
            except subprocess.CalledProcessError as e:
                print(f"Warning: Could not initialize new Git repository: {e}")
                if e.stderr:
                    print(f"Git error: {e.stderr}")
            
            return True
        else:
            print("Error: Clone appeared successful but directory is empty")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        if e.stderr:
            print(f"Git error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error during clone: {e}")
        return False


def get_os_type():
    """Determine the operating system type."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system in ["linux", "darwin"]:  # darwin is macOS
        return "unix"
    else:
        return "unknown"


def execute_bootstrap(target_dir, os_type):
    """Execute the appropriate bootstrap file based on OS."""
    # Ensure target_dir is a proper path
    if not os.path.isabs(target_dir):
        target_dir = os.path.abspath(target_dir)
    
    print(f"Executing bootstrap from directory: {target_dir}")
    
    if os_type == "windows":
        bootstrap_file = os.path.join(target_dir, "bootstrap.bat")
        if os.path.exists(bootstrap_file):
            print("Executing Windows bootstrap script...")
            try:
                # Use shell=True for Windows batch files
                subprocess.run(bootstrap_file, shell=True, check=True, cwd=target_dir)
                print("Windows bootstrap completed successfully!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error executing Windows bootstrap: {e}")
                return False
        else:
            print(f"Windows bootstrap file not found: {bootstrap_file}")
            print(f"Available files in {target_dir}: {os.listdir(target_dir) if os.path.exists(target_dir) else 'Directory does not exist'}")
            return False
    
    elif os_type == "unix":
        bootstrap_file = os.path.join(target_dir, "bootstrap.sh")
        if os.path.exists(bootstrap_file):
            print("Executing Unix bootstrap script...")
            try:
                # Make the script executable
                os.chmod(bootstrap_file, 0o755)
                # Execute the shell script
                subprocess.run([bootstrap_file], check=True, cwd=target_dir)
                print("Unix bootstrap completed successfully!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error executing Unix bootstrap: {e}")
                return False
        else:
            print(f"Unix bootstrap file not found: {bootstrap_file}")
            print(f"Available files in {target_dir}: {os.listdir(target_dir) if os.path.exists(target_dir) else 'Directory does not exist'}")
            return False
    
    else:
        print(f"Unsupported operating system: {platform.system()}")
        return False
    
    return True


def validate_project_name(project_name):
    """Validate the project name."""
    # Check if project name is provided
    if not project_name or not project_name.strip():
        print("Error: Please enter a valid project name.")
        return False
    
    # Check for invalid characters in project name
    invalid_chars = '<>:"|?*\\/'
    if any(char in project_name for char in invalid_chars):
        print(f"Error: Project name contains invalid characters: {invalid_chars}")
        return False
    
    # Check for reserved names
    reserved_names = ['.', '..', 'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if project_name.upper() in [name.upper() for name in reserved_names]:
        print(f"Error: Cannot use reserved name: {project_name}")
        return False
    
    return True


def validate_project_path(project_path):
    """Validate the project path (can be relative or absolute)."""
    # Check if path is provided
    if not project_path or not project_path.strip():
        print("Error: Please enter a valid project path.")
        return False
    
    # Check for invalid characters in the path
    invalid_chars = '<>|?*'
    if any(char in project_path for char in invalid_chars):
        print(f"Error: Project path contains invalid characters: {invalid_chars}")
        return False
    
    # Check if the path is accessible for creation
    try:
        if os.path.isabs(project_path):
            # Absolute path - check if parent directory is writable
            parent_dir = project_path
        else:
            # Relative path - check if current directory is writable
            parent_dir = os.getcwd()
        
        if not os.access(parent_dir, os.W_OK):
            print(f"Error: Cannot write to directory: {parent_dir}")
            return False
    except Exception as e:
        print(f"Error validating project path: {e}")
        return False
    
    return True


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize a Fullstack-boilerplate project by cloning the repository and executing the bootstrap script.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python project_initializer.py "my-project" "C:\\Users\\username\\Projects"
  python project_initializer.py "my-app" "C:\\Projects"
  python project_initializer.py "new-project" "D:\\Development"
  python project_initializer.py "test-app" "."
        """
    )
    
    parser.add_argument(
        'project_name',
        help='Name of the project directory to create (REQUIRED)'
    )
    
    parser.add_argument(
        'project_path',
        help='Path where the project directory should be created (REQUIRED) - can be relative or absolute'
    )
    
    return parser.parse_args()


def main():
    """Main function to orchestrate the project initialization."""
    print("=== Project Initializer Script ===")
    print("Initializing Fullstack-boilerplate project...")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Get the project name and path from arguments
    project_name = args.project_name
    project_path = args.project_path
    
    # Validate project name
    if not validate_project_name(project_name):
        print("Invalid project name. Exiting.")
        sys.exit(1)
    
    # Validate project path
    if not validate_project_path(project_path):
        print("Invalid project path. Exiting.")
        sys.exit(1)
    
    # Construct the full project directory path
    if os.path.isabs(project_path):
        # Absolute path
        full_project_dir = os.path.join(project_path, project_name)
    else:
        # Relative path - convert to absolute
        full_project_dir = os.path.abspath(os.path.join(project_path, project_name))
    
    print(f"Project name: {project_name}")
    print(f"Project path: {project_path}")
    print(f"Full project directory: {full_project_dir}")
    
    # Create the project directory if it doesn't exist
    try:
        os.makedirs(full_project_dir, exist_ok=True)
        print(f"Project directory created/verified: {full_project_dir}")
    except Exception as e:
        print(f"Error creating project directory: {e}")
        sys.exit(1)
    
    # Configuration
    repo_url = "https://github.com/Kicchu02/Fullstack-boilerplate.git"
    
    # Check if git is installed
    if not check_git_installed():
        print("Error: Git is not installed or not available in PATH.")
        print("Please install Git and try again.")
        sys.exit(1)
    
    # Determine OS type
    os_type = get_os_type()
    print(f"Detected operating system: {platform.system()} ({os_type})")
    
    if os_type == "unknown":
        print("Warning: Unknown operating system. Bootstrap execution may fail.")
    
    # Clone the repository
    if not clone_repository(repo_url, full_project_dir):
        print("Failed to clone repository. Exiting.")
        sys.exit(1)
    
    # Execute the appropriate bootstrap file
    if not execute_bootstrap(full_project_dir, os_type):
        print("Bootstrap execution failed. Exiting.")
        sys.exit(1)
    
    print("\n=== Project initialization completed successfully! ===")
    print(f"Your project is ready in the '{full_project_dir}' directory.")
    print("You can now start developing your full-stack application!")


if __name__ == "__main__":
    main()
