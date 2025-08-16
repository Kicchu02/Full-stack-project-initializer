#!/usr/bin/env python3
"""
Project Initializer Script - GUI Version
A simple GUI interface for cloning the Fullstack-boilerplate repository and executing the appropriate bootstrap file.
"""

import os
import sys
import subprocess
import platform
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading


class ProjectInitializerGUI:
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Project Initializer")
        self.root.resizable(False, False)  # Fixed size to fit content
        
        # Variables
        self.project_name = tk.StringVar(value="")
        self.project_path = tk.StringVar(value="")
        self.repo_url = "https://github.com/Kicchu02/Fullstack-boilerplate.git"
        
        # Create widgets
        self.create_widgets()
        
        # Start system checks
        self.check_git_async()
        
        # Auto-fit window to content
        self.root.update_idletasks()
        self.root.geometry("")  # Let Tkinter calculate optimal size
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill="both", expand=True)
        
        # Title - centered
        title_label = ttk.Label(main_frame, text="Project Initializer", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Description - centered
        desc_label = ttk.Label(main_frame, text="Initialize a Fullstack-boilerplate project by cloning the repository and executing the bootstrap script.\n\nProvide the FULL PATH where you want to create your new project directory.", 
                              wraplength=600, justify="center", font=("Arial", 10))
        desc_label.pack(pady=(0, 30))
        
        # Project Name Section
        name_label = ttk.Label(main_frame, text="Project Name (Required):", font=("Arial", 11, "bold"))
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill="x", pady=(0, 20))
        
        self.name_entry = ttk.Entry(name_frame, textvariable=self.project_name, width=50, font=("Arial", 10))
        self.name_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Add placeholder text
        self.name_entry.insert(0, "Enter project name (e.g., my-app)")
        
        # Project Path Section
        path_label = ttk.Label(main_frame, text="Project Path (Required):", font=("Arial", 11, "bold"))
        path_label.pack(anchor="w", pady=(0, 5))
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill="x", pady=(0, 30))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.project_path, width=50, font=("Arial", 10))
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side="right")
        
        # Add placeholder text
        self.dir_entry.insert(0, "Enter path (e.g., C:\\Projects or .)")
        
        # OS Detection Display
        os_frame = ttk.LabelFrame(main_frame, text="System Information", padding="15")
        os_frame.pack(fill="x", pady=(0, 30))
        
        # OS info in a grid within the frame
        os_frame.columnconfigure(1, weight=1)
        
        ttk.Label(os_frame, text="Operating System:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.os_label = ttk.Label(os_frame, text="Detecting...", font=("Arial", 10))
        self.os_label.grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        ttk.Label(os_frame, text="Git Status:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.git_label = ttk.Label(os_frame, text="Checking...", font=("Arial", 10))
        self.git_label.grid(row=1, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # System Ready Indicator
        ttk.Label(os_frame, text="System Status:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.system_status_label = ttk.Label(os_frame, text="Checking...", font=("Arial", 10), foreground="orange")
        self.system_status_label.grid(row=2, column=1, sticky=tk.W, padx=(15, 0), pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=(0, 20))
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Performing system checks...", font=("Arial", 10))
        self.status_label.pack(pady=(0, 30))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        # Initialize button (initially disabled)
        self.init_btn = ttk.Button(button_frame, text="Initialize Project", command=self.initialize_project, 
                                  state="disabled", style="Accent.TButton")
        self.init_btn.pack(side="left", padx=(0, 20))
        
        # Quit button
        quit_btn = ttk.Button(button_frame, text="QUIT", command=self.root.quit, style="Accent.TButton")
        quit_btn.pack(side="left")
        
        # Bind Enter key to Initialize button
        self.root.bind('<Return>', lambda event: self.initialize_project() if self.init_btn['state'] == 'normal' else None)
        
        # Bind Escape key to Quit
        self.root.bind('<Escape>', lambda event: self.root.quit())
    
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(
            title="Select Project Directory",
            initialdir=os.getcwd()
        )
        if directory:
            self.project_path.set(directory)
    
    def update_status(self, message):
        """Update status label and log to console."""
        self.status_label.config(text=message)
        print(message)
        self.root.update_idletasks()
    
    def initialize_project(self):
        """Initialize the project in a separate thread."""
        # Get project details
        project_name = self.project_name.get().strip()
        project_path = self.project_path.get().strip()
        
        # Validate inputs
        if not project_name or project_name == "Enter project name (e.g., my-app)":
            messagebox.showerror("Error", "Please enter a valid project name.")
            return
            
        if not project_path or project_path == "Enter path (e.g., C:\\Projects or .)":
            messagebox.showerror("Error", "Please enter a valid project path.")
            return
        
        # Validate project name
        if not self.validate_project_name(project_name):
            return
        
        # Validate project path
        if not self.validate_project_path(project_path):
            return
        
        # Construct the full project directory path
        if os.path.isabs(project_path):
            full_project_dir = os.path.join(project_path, project_name)
        else:
            full_project_dir = os.path.abspath(os.path.join(project_path, project_name))
        
        # Disable the initialize button to prevent multiple clicks
        self.init_btn.config(state="disabled")
        self.progress.start()
        
        # Start initialization in a separate thread
        thread = threading.Thread(target=self._initialize_project_thread, 
                                args=(full_project_dir,), daemon=True)
        thread.start()
    
    def _initialize_project_thread(self, full_project_dir):
        """Thread function for project initialization."""
        try:
            # Create project directory
            os.makedirs(full_project_dir, exist_ok=True)
            self.root.after(0, lambda: self.update_status(f"Project directory created: {full_project_dir}"))
            
            # Clone repository
            if not self.clone_repository(self.repo_url, full_project_dir):
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to clone repository"))
                return
            
            # Execute bootstrap
            os_type = self.get_os_type()
            if not self.execute_bootstrap(full_project_dir, os_type):
                self.root.after(0, lambda: messagebox.showerror("Error", "Bootstrap execution failed"))
                return
            
            # Success
            self.root.after(0, lambda: self.update_status("Project initialization completed successfully!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"Project initialized successfully!\n\nYour project is ready in:\n{full_project_dir}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Error: {e}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {e}"))
        finally:
            # Re-enable the initialize button and stop progress
            self.root.after(0, lambda: self.init_btn.config(state="normal"))
            self.root.after(0, lambda: self.progress.stop())
    
    def validate_project_name(self, project_name):
        """Validate the project name."""
        # Check for invalid characters
        invalid_chars = '<>:"|?*\\/'
        if any(char in project_name for char in invalid_chars):
            messagebox.showerror("Error", f"Project name contains invalid characters: {invalid_chars}")
            return False
        
        # Check for reserved names
        reserved_names = ['.', '..', 'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        if project_name.upper() in [name.upper() for name in reserved_names]:
            messagebox.showerror("Error", f"Cannot use reserved name: {project_name}")
            return False
        
        return True
    
    def validate_project_path(self, project_path):
        """Validate the project path."""
        # Check for invalid characters
        invalid_chars = '<>|?*'
        if any(char in project_path for char in invalid_chars):
            messagebox.showerror("Error", f"Project path contains invalid characters: {invalid_chars}")
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
                messagebox.showerror("Error", f"Cannot write to directory: {parent_dir}")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error validating project path: {e}")
            return False
        
        return True
    
    def clone_repository(self, repo_url, target_dir):
        """Clone the repository to the target directory."""
        self.update_status(f"Cloning repository from {repo_url}...")
        
        if os.path.exists(target_dir):
            self.update_status(f"Directory {target_dir} already exists. Removing it...")
            shutil.rmtree(target_dir)
        
        try:
            # Clone with verbose output to see what's happening
            result = subprocess.run(['git', 'clone', '--verbose', repo_url, target_dir], 
                                  check=True, capture_output=True, text=True)
            
            # Verify the clone actually worked by checking if files exist
            if os.path.exists(target_dir) and os.listdir(target_dir):
                items = os.listdir(target_dir)
                self.update_status(f"Repository cloned successfully to {target_dir}")
                self.update_status(f"Cloned {len(items)} items: {', '.join(items[:5])}{'...' if len(items) > 5 else ''}")
                
                # Check for key files
                expected_files = ['README.md', 'bootstrap.bat', 'bootstrap.sh']
                found_files = [f for f in expected_files if os.path.exists(os.path.join(target_dir, f))]
                if found_files:
                    self.update_status(f"Found key files: {', '.join(found_files)}")
                else:
                    self.update_status("Warning: No expected key files found")
                
                # Remove existing Git repository and initialize new one
                self.update_status("Removing existing Git repository...")
                git_dir = os.path.join(target_dir, '.git')
                if os.path.exists(git_dir):
                    try:
                        # Use OS-specific commands to remove Git repository
                        if platform.system().lower() == "windows":
                            # Windows: Use rmdir with /s /q for recursive deletion
                            subprocess.run(['rmdir', '/s', '/q', git_dir], shell=True, check=True, capture_output=True)
                            self.update_status("Existing Git repository removed successfully (Windows)")
                        else:
                            # Linux/Mac: Use rm -rf
                            subprocess.run(['rm', '-rf', git_dir], check=True, capture_output=True)
                            self.update_status("Existing Git repository removed successfully (Unix)")
                    except subprocess.CalledProcessError as e:
                        self.update_status(f"Warning: Could not remove existing Git repository: {e}")
                        # Try alternative method
                        try:
                            if platform.system().lower() == "windows":
                                # Windows: Force delete using PowerShell
                                ps_command = f'Remove-Item -Path "{git_dir}" -Recurse -Force'
                                subprocess.run(['powershell', '-Command', ps_command], check=True, capture_output=True)
                                self.update_status("Existing Git repository removed successfully (PowerShell)")
                            else:
                                # Linux/Mac: Use find and rm
                                subprocess.run(['find', git_dir, '-type', 'f', '-exec', 'rm', '-f', '{}', '+'], check=True, capture_output=True)
                                subprocess.run(['find', git_dir, '-type', 'd', '-exec', 'rmdir', '{}', '+'], check=True, capture_output=True)
                                self.update_status("Existing Git repository removed successfully (find/rm)")
                        except Exception as e2:
                            self.update_status(f"Warning: Alternative removal method also failed: {e2}")
                            self.update_status("Continuing with existing Git repository...")
                
                # Initialize new Git repository
                self.update_status("Initializing new Git repository...")
                try:
                    subprocess.run(['git', 'init'], cwd=target_dir, check=True, capture_output=True, text=True)
                    self.update_status("New Git repository initialized successfully")
                    
                    # Add all files to the new repository
                    subprocess.run(['git', 'add', '.'], cwd=target_dir, check=True, capture_output=True, text=True)
                    self.update_status("All files added to new Git repository")
                    
                    # Make initial commit
                    subprocess.run(['git', 'commit', '-m', 'Initial commit from Fullstack-boilerplate'], 
                                 cwd=target_dir, check=True, capture_output=True, text=True)
                    self.update_status("Initial commit created successfully")
                    
                except subprocess.CalledProcessError as e:
                    self.update_status(f"Warning: Could not initialize new Git repository: {e}")
                    if e.stderr:
                        self.update_status(f"Git error: {e.stderr}")
                
                return True
            else:
                self.update_status(f"Clone appeared successful but directory is empty")
                return False
                
        except subprocess.CalledProcessError as e:
            self.update_status(f"Error cloning repository: {e}")
            if e.stderr:
                self.update_status(f"Git error: {e.stderr}")
            return False
        except Exception as e:
            self.update_status(f"Unexpected error during clone: {e}")
            return False
    
    def execute_bootstrap(self, target_dir, os_type):
        """Execute the appropriate bootstrap file based on OS."""
        if os_type == "windows":
            bootstrap_file = os.path.join(target_dir, "bootstrap.bat")
            if os.path.exists(bootstrap_file):
                self.update_status("Executing Windows bootstrap script...")
                try:
                    subprocess.run(bootstrap_file, shell=True, check=True, cwd=target_dir, capture_output=True)
                    self.update_status("Windows bootstrap completed successfully!")
                    return True
                except subprocess.CalledProcessError as e:
                    self.update_status(f"Error executing Windows bootstrap: {e}")
                    return False
            else:
                self.update_status(f"Windows bootstrap file not found: {bootstrap_file}")
                return False
        
        elif os_type == "unix":
            bootstrap_file = os.path.join(target_dir, "bootstrap.sh")
            if os.path.exists(bootstrap_file):
                self.update_status("Executing Unix bootstrap script...")
                try:
                    os.chmod(bootstrap_file, 0o755)
                    subprocess.run([bootstrap_file], check=True, cwd=target_dir, capture_output=True)
                    self.update_status("Unix bootstrap completed successfully!")
                    return True
                except subprocess.CalledProcessError as e:
                    self.update_status(f"Error executing Unix bootstrap: {e}")
                    return False
            else:
                self.update_status(f"Unix bootstrap file not found: {bootstrap_file}")
                return False
        
        else:
            self.update_status(f"Unsupported operating system: {platform.system()}")
            return False
    
    def check_git_async(self):
        """Check Git installation asynchronously."""
        def check():
            # Check OS first
            os_type = self.get_os_type()
            os_name = platform.system()
            self.root.after(0, lambda: self.os_label.config(text=f"{os_name} ({os_type})"))
            
            # Then check Git
            if self.check_git_installed():
                self.root.after(0, lambda: self.git_label.config(text="✓ Git is installed", foreground="green"))
                self.root.after(0, lambda: self.system_status_label.config(text="✓ Ready", foreground="green"))
                self.root.after(0, lambda: self.status_label.config(text="System checks completed. Ready to initialize project."))
                self.root.after(0, lambda: self.init_btn.config(state="normal"))
                # Force update to ensure button is visible
                self.root.after(0, lambda: self.root.update_idletasks())
                print("Git check completed - Initialize button should now be enabled")
            else:
                self.root.after(0, lambda: self.git_label.config(text="✗ Git not found", foreground="red"))
                self.root.after(0, lambda: self.system_status_label.config(text="✗ Not Ready", foreground="red"))
                self.root.after(0, lambda: self.status_label.config(text="Please install Git to continue"))
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def check_git_installed(self):
        """Check if git is installed and available in PATH."""
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def check_repository_accessible(self, repo_url):
        """Check if the repository URL is accessible."""
        try:
            # Try to get repository info without cloning
            result = subprocess.run(['git', 'ls-remote', '--heads', repo_url], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout.strip():
                return True, None
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout: Repository access took too long"
        except Exception as e:
            return False, str(e)
    
    def get_os_type(self):
        """Determine the operating system type."""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system in ["linux", "darwin"]:  # darwin is macOS
            return "unix"
        else:
            return "unknown"


def main():
    """Main function to start the GUI application."""
    root = tk.Tk()
    app = ProjectInitializerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
