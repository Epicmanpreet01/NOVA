import os
import shutil
import sys

def prepare_build():
    """Prepare the build environment and create executable"""
    # Install required packages if not already installed
    os.system('pip install pyinstaller eel')
    
    # Create build command with all necessary dependencies and data files
    cmd = (
        'pyinstaller --noconfirm '  # Don't ask for confirmation
        '--add-data "static;static" '  # Include static folder with all assets
        '--add-data "engine;engine" '  # Include engine folder
        '--add-data ".env;." '  # Include .env file
        '--hidden-import eel '
        '--hidden-import multiprocessing '
        '--hidden-import engineio.async_drivers.threading '
        '--hidden-import sqlite3 '
        '--hidden-import werkzeug '
        '--hidden-import engineio '
        '--hidden-import sounddevice '
        '--hidden-import speech_recognition '
        '--hidden-import webbrowser '  # Added for browser handling
        '--hidden-import threading '    # Added for Timer
        '--collect-submodules engine '
        '--icon=static/assets/img/Icon.ico '
        '--noconsole '
        '--name Nova '
        '--onefile '  # Create a single executable file
        '--runtime-hook add_path.py '  # Add runtime hook
        'run.py'
    )
    
    # Create runtime hook to fix multiprocessing
    with open('add_path.py', 'w') as f:
        f.write("""
import os
import sys

def _append_run_path():
    if getattr(sys, 'frozen', False):
        pathlist = []
        
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        pathlist.append(sys._MEIPASS)
        
        # the application runtime repository
        pathlist.append(os.path.dirname(os.path.realpath(sys.argv[0])))
        
        # extend sys.path with our paths
        for path in pathlist:
            if path not in sys.path:
                sys.path.append(path)

_append_run_path()
""")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Execute the build command
    os.system(cmd)
    
    # Clean up runtime hook
    if os.path.exists('add_path.py'):
        os.remove('add_path.py')
    
    # Copy additional required files to the dist folder
    if os.path.exists('dist/Nova.exe'):
        print("Build completed! The executable is located at: dist/Nova.exe")
    else:
        print("Build failed! Check for errors above.")

if __name__ == "__main__":
    prepare_build()