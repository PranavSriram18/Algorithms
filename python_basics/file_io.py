import json
import csv
import shutil
from pathlib import Path
from typing import List, Dict, Any
import tempfile

########################
# Basic File Operations #
########################

def read_write_basics():
    """Basic patterns for reading and writing files."""
    
    # Reading entire file at once
    with open('file.txt', 'r') as f:
        content = f.read()  # entire file as string
        
    # Reading line by line (memory efficient for large files)
    with open('file.txt', 'r') as f:
        for line in f:  # file object is an iterator
            print(line.strip())
    
    # Reading all lines into list
    with open('file.txt', 'r') as f:
        lines = f.readlines()  # list of strings with newlines
        # or
        lines = [line.strip() for line in f]  # list without newlines
    
    # Writing strings
    with open('output.txt', 'w') as f:  # 'w' overwrites
        f.write('hello\n')
        f.write('world\n')
    
    with open('output.txt', 'a') as f:  # 'a' appends
        f.write('more content\n')
    
    # Writing multiple lines at once
    lines = ['line1', 'line2', 'line3']
    with open('output.txt', 'w') as f:
        f.writelines(f"{line}\n" for line in lines)

def binary_file_operations():
    """Patterns for binary file operations."""
    
    # Reading binary data
    with open('file.bin', 'rb') as f:
        data = f.read()  # reads as bytes
    
    # Writing binary data
    with open('file.bin', 'wb') as f:
        f.write(b'binary data')

###################
# JSON Operations #
###################

def json_operations():
    """Common JSON patterns."""
    
    # Writing JSON
    data = {
        'name': 'John',
        'age': 30,
        'cities': ['New York', 'London']
    }
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)  # pretty print
    
    # Reading JSON
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    # String operations
    json_str = json.dumps(data)  # to string
    data = json.loads(json_str)  # from string
    
    # Custom encoding
    class CustomClass:
        def __init__(self, value):
            self.value = value
    
    def custom_encoder(obj):
        if isinstance(obj, CustomClass):
            return {'value': obj.value}
        raise TypeError(f'Object of type {type(obj)} not serializable')
    
    with open('custom.json', 'w') as f:
        json.dump({'obj': CustomClass(42)}, f, default=custom_encoder)

##################
# CSV Operations #
##################

def csv_operations():
    """Common CSV patterns."""
    
    # Writing CSV
    data = [
        ['name', 'age', 'city'],
        ['John', 30, 'New York'],
        ['Mary', 25, 'London']
    ]
    
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    # Writing CSV with dictionary
    dict_data = [
        {'name': 'John', 'age': 30, 'city': 'New York'},
        {'name': 'Mary', 'age': 25, 'city': 'London'}
    ]
    
    with open('dict_data.csv', 'w', newline='') as f:
        fieldnames = ['name', 'age', 'city']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_data)
    
    # Reading CSV
    with open('data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name, age, city = row
    
    # Reading CSV as dictionaries
    with open('data.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['name'], row['age'])

############################
# Directory Operations     #
############################

def directory_operations():
    """Common directory operation patterns."""
    
    # Current directory
    current = Path.cwd()
    
    # Home directory
    home = Path.home()
    
    # Creating directories
    Path('new_dir').mkdir(exist_ok=True)
    Path('parent/child/grandchild').mkdir(parents=True, exist_ok=True)
    
    # Listing directory contents
    p = Path('.')
    
    # Iterating over directory
    for item in p.iterdir():
        if item.is_file():
            print(f"File: {item}")
        elif item.is_dir():
            print(f"Directory: {item}")
    
    # Finding files by pattern
    python_files = list(p.glob('*.py'))  # current directory
    all_python_files = list(p.rglob('*.py'))  # recursive
    
    # Removing files and directories
    Path('file.txt').unlink(missing_ok=True)  # delete file
    Path('empty_dir').rmdir()  # delete empty directory
    shutil.rmtree('dir_with_contents')  # delete directory and contents

#########################
# Temporary Files       #
#########################

def temp_file_operations():
    """Patterns for working with temporary files."""
    
    # Temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=True) as tmp:
        tmp.write('temporary content')
        tmp.flush()
        # Use tmp.name to get the file path
    
    # Temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file_path = Path(tmpdir) / 'file.txt'
        temp_file_path.write_text('content')

#########################
# Safe File Operations  #
#########################

def safe_file_operations():
    """Patterns for safely handling files."""
    
    def atomic_write(file_path: Path, content: str):
        """Write file atomically using temporary file."""
        temp_path = file_path.with_suffix('.tmp')
        try:
            temp_path.write_text(content)
            temp_path.replace(file_path)  # atomic on most systems
        except Exception as e:
            temp_path.unlink(missing_ok=True)
            raise
    
    def safe_copy(src: Path, dst: Path):
        """Safely copy file with backup."""
        if dst.exists():
            backup = dst.with_suffix('.bak')
            dst.replace(backup)
        shutil.copy2(src, dst)
    
    # Example of checking file access before operations
    path = Path('file.txt')
    if path.exists() and path.is_file() and os.access(path, os.R_OK):
        content = path.read_text()

#########################
# Path Operations       #
#########################

def path_operations():
    """Common path operation patterns."""
    
    p = Path('path/to/file.txt')
    
    # Path components
    print(p.name)      # file.txt
    print(p.stem)      # file
    print(p.suffix)    # .txt
    print(p.parent)    # path/to
    print(p.anchor)    # root (e.g., 'C:\' on Windows)
    
    # Path operations
    new_path = p.with_name('newname.txt')
    new_path = p.with_suffix('.md')
    abs_path = p.absolute()
    
    # Path joining
    path = Path('dir') / 'subdir' / 'file.txt'
    
    # Relative paths
    rel_path = p.relative_to(Path('path'))
    
    # Path existence and type checks
    if p.exists():
        if p.is_file():
            pass
        elif p.is_dir():
            pass
        elif p.is_symlink():
            pass

if __name__ == '__main__':
    # Example usage
    read_write_basics()
    json_operations()
    csv_operations()
    directory_operations()
    temp_file_operations()
    safe_file_operations()
    path_operations()