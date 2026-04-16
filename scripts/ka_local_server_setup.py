#!/usr/bin/env python3
"""
Knowledge Atlas Local Development Server Setup

Sets up and launches a local development server that mirrors the production xrlab server.
- Checks/installs required dependencies
- Initializes data directory structure
- Sets up authentication database
- Launches fastapi server on port 8765
"""

import subprocess
import sys
from pathlib import Path
import shutil
import secrets
import json

def run_command(cmd, check=True, capture_output=False):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Return code: {e.returncode}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        raise

def check_and_install_dependencies():
    """Check for required packages and install missing ones."""
    print("Checking Python dependencies...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'python-jose',
        'passlib',
        'python-multipart',
        'aiofiles',
        'pdfplumber',
        'PyPDF2',
        'requests'  # For testing
    ]

    missing_packages = []
    for package in required_packages:
        result = subprocess.run(
            "python3 -c 'import {}'".format(package.replace("-", "_")),
            shell=True,
            capture_output=True
        )
        if result.returncode != 0:
            missing_packages.append(package)

    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            run_command(f"pip3 install {package} --break-system-packages")
    else:
        print("✓ All dependencies installed")

def setup_data_directory():
    """Initialize data directory structure."""
    print("Setting up data directory structure...")
    repo_root = Path(__file__).parent.parent
    data_dir = repo_root / "data"

    # Create data directory
    data_dir.mkdir(exist_ok=True)
    print(f"✓ Data directory: {data_dir}")

    # Create subdirectories
    storage_dir = data_dir / "storage"
    storage_dir.mkdir(exist_ok=True)
    print(f"✓ Storage directory: {storage_dir}")

    payloads_dir = data_dir / "ka_payloads"
    payloads_dir.mkdir(exist_ok=True)
    print(f"✓ Payloads directory: {payloads_dir}")

    # Set up authentication database
    db_file = data_dir / "ka_auth.db"
    if not db_file.exists():
        # Check for server backup
        server_backup = data_dir / "ka_auth.server_2026-04-12.db"
        if server_backup.exists():
            print(f"Copying server backup to {db_file.name}...")
            shutil.copy(server_backup, db_file)
            print(f"✓ Database copied from server backup")
        else:
            # Create minimal SQLite database
            print("Creating new authentication database...")
            try:
                import sqlite3
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()

                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        hashed_password TEXT NOT NULL,
                        full_name TEXT,
                        track TEXT DEFAULT 'track1',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                conn.commit()
                conn.close()
                print(f"✓ Database initialized: {db_file}")
            except Exception as e:
                print(f"Warning: Could not initialize SQLite database: {e}")
                print("The server will create the database on first run.")
    else:
        print(f"✓ Database exists: {db_file}")

    # Set up workflow database
    workflow_db = data_dir / "ka_workflow.db"
    if not workflow_db.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(workflow_db))
            cursor = conn.cursor()

            # Create basic workflow tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS claims (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_id TEXT NOT NULL,
                    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            conn.close()
            print(f"✓ Workflow database initialized: {workflow_db}")
        except Exception as e:
            print(f"Warning: Could not initialize workflow database: {e}")

def setup_authentication_secret():
    """Generate ka_auth_secret.txt if it doesn't exist."""
    print("Setting up authentication secret...")
    repo_root = Path(__file__).parent.parent
    secret_file = repo_root / "ka_auth_secret.txt"

    if not secret_file.exists():
        # Generate a secure random secret
        secret = secrets.token_urlsafe(32)
        secret_file.write_text(secret)
        secret_file.chmod(0o600)
        print(f"✓ Secret generated: {secret_file}")
    else:
        print(f"✓ Secret exists: {secret_file}")

def setup_config():
    """Update ka_config.js to use local server."""
    print("Updating configuration for local server...")
    repo_root = Path(__file__).parent.parent
    config_file = repo_root / "ka_config.js"

    if config_file.exists():
        content = config_file.read_text()
        # Update apiBase to same-origin
        if "apiBase" in content:
            updated = content.replace(
                "apiBase: 'http://",
                "apiBase: '"  # Empty string for same-origin
            )
            # Handle any production URLs
            if "xrlab" in updated:
                lines = updated.split('\n')
                new_lines = []
                for line in lines:
                    if "apiBase" in line and "xrlab" in line:
                        new_lines.append("  apiBase: '',  // Local development")
                    else:
                        new_lines.append(line)
                content = '\n'.join(new_lines)
            config_file.write_text(content)
            print(f"✓ Config updated for local server")
        else:
            print(f"Note: ka_config.js does not have apiBase setting, may need manual update")
    else:
        print(f"Note: ka_config.js not found at {config_file}")

def check_server_file():
    """Check if ka_auth_server.py exists."""
    repo_root = Path(__file__).parent.parent
    server_file = repo_root / "ka_auth_server.py"

    if not server_file.exists():
        print(f"\n⚠️  Warning: ka_auth_server.py not found at {server_file}")
        print("Cannot start server. Please ensure ka_auth_server.py exists.")
        return False
    return True

def start_server():
    """Start the FastAPI server with uvicorn."""
    print("\nStarting Knowledge Atlas local server...")
    repo_root = Path(__file__).parent.parent
    server_file = repo_root / "ka_auth_server.py"

    print(f"Server file: {server_file}")
    print("\n" + "="*70)
    print("LOCAL DEVELOPMENT SERVER STARTING")
    print("="*70)
    print(f"Server URL:  http://localhost:8765")
    print(f"API Base:    http://localhost:8765/api")
    print(f"Auth Base:   http://localhost:8765/auth")
    print(f"\nDatabase:    {repo_root}/data/ka_auth.db")
    print(f"Storage:     {repo_root}/data/storage/")
    print(f"Payloads:    {repo_root}/data/ka_payloads/")
    print("\nTest credentials (if default user exists):")
    print("  Email: test_student@ucsd.edu")
    print("  Password: (check ka_auth_server.py for default)")
    print("\nTo stop the server, press Ctrl+C")
    print("="*70 + "\n")

    try:
        # Change to repo root directory and launch uvicorn
        run_command(
            f"cd {repo_root} && python3 -m uvicorn ka_auth_server:app --host 0.0.0.0 --port 8765 --reload"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)

def main():
    """Main setup flow."""
    print("\n" + "="*70)
    print("KNOWLEDGE ATLAS LOCAL SERVER SETUP")
    print("="*70 + "\n")

    try:
        # Step 1: Check dependencies
        check_and_install_dependencies()

        # Step 2: Set up data directory
        setup_data_directory()

        # Step 3: Set up authentication secret
        setup_authentication_secret()

        # Step 4: Update configuration
        setup_config()

        # Step 5: Check for server file
        if not check_server_file():
            sys.exit(1)

        # Step 6: Start server
        start_server()

    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
