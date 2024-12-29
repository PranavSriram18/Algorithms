import requests
import asyncio
import aiohttp  # Common with asyncio for HTTP
import argparse
import logging
import sys
from typing import List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

#################
# requests      #
#################

def requests_patterns():
    """Common patterns with the requests library."""
    
    # Basic GET request
    response = requests.get('https://api.example.com/data')
    data = response.json()  # Parse JSON response
    
    # Query parameters
    params = {
        'key1': 'value1',
        'key2': 'value2'
    }
    response = requests.get('https://api.example.com/search', params=params)
    
    # POST request with JSON
    data = {'name': 'John', 'age': 30}
    response = requests.post('https://api.example.com/users',
                           json=data)  # Automatically serializes to JSON
    
    # POST with form data
    files = {'file': open('example.txt', 'rb')}
    data = {'key': 'value'}
    response = requests.post('https://api.example.com/upload',
                           files=files,
                           data=data)
    
    # Headers
    headers = {
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://api.example.com/protected',
                          headers=headers)
    
    # Session for multiple requests
    with requests.Session() as session:
        session.headers.update({'Authorization': 'Bearer token123'})
        response1 = session.get('https://api.example.com/data1')
        response2 = session.get('https://api.example.com/data2')
    
    # Error handling
    try:
        response = requests.get('https://api.example.com/data')
        response.raise_for_status()  # Raises exception for 400/500 status codes
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    # Timeout
    try:
        response = requests.get('https://api.example.com/data',
                              timeout=5)  # 5 seconds
    except requests.Timeout:
        print("Request timed out")

#################
# asyncio       #
#################

async def asyncio_patterns():
    """Common patterns with asyncio."""
    
    # Basic coroutine
    async def fetch_data():
        await asyncio.sleep(1)  # Simulate IO operation
        return "data"
    
    # Running a coroutine
    data = await fetch_data()
    
    # Running multiple coroutines concurrently
    async def fetch_all():
        tasks = [
            fetch_data(),
            fetch_data(),
            fetch_data()
        ]
        results = await asyncio.gather(*tasks)
        return results
    
    # HTTP requests with aiohttp
    async def fetch_url(url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    # Multiple HTTP requests concurrently
    async def fetch_urls(urls: List[str]) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(session.get(url))
            responses = await asyncio.gather(*tasks)
            return [await r.json() for r in responses]
    
    # Task creation and cancellation
    task = asyncio.create_task(fetch_data())
    # ... do other things ...
    if not task.done():
        task.cancel()
    
    # Timeouts
    try:
        async with asyncio.timeout(1.0):
            await fetch_data()
    except asyncio.TimeoutError:
        print("Operation timed out")

# Running asyncio code
def run_async_code():
    """Helper to run async code."""
    asyncio.run(asyncio_patterns())

#################
# argparse      #
#################

def setup_argparse() -> argparse.ArgumentParser:
    """Common patterns with argparse."""
    
    parser = argparse.ArgumentParser(
        description="Example program",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Positional arguments
    parser.add_argument("input_file",
                       type=Path,
                       help="Input file path")
    
    # Optional arguments
    parser.add_argument("--output", "-o",
                       type=Path,
                       default=Path("output.txt"),
                       help="Output file path")
    
    # Boolean flags
    parser.add_argument("--verbose", "-v",
                       action="store_true",
                       help="Increase output verbosity")
    
    # Choices
    parser.add_argument("--mode",
                       choices=["train", "test", "eval"],
                       default="train",
                       help="Operation mode")
    
    # Multiple values
    parser.add_argument("--numbers",
                       type=int,
                       nargs="+",
                       help="List of numbers")
    
    # Argument groups
    group = parser.add_argument_group("Advanced options")
    group.add_argument("--threshold",
                      type=float,
                      default=0.5)
    
    # Mutually exclusive arguments
    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument("--quiet", action="store_true")
    mutex_group.add_argument("--debug", action="store_true")
    
    return parser

def parse_and_validate_args(parser: argparse.ArgumentParser):
    """Parse and validate command line arguments."""
    
    args = parser.parse_args()
    
    # Custom validation
    if args.input_file.exists():
        if not args.input_file.is_file():
            parser.error(f"{args.input_file} is not a file")
    else:
        parser.error(f"{args.input_file} does not exist")
    
    return args

#################
# logging       #
#################

def setup_logging(
    log_file: Path = None,
    level: str = "INFO"
) -> logging.Logger:
    """Configure logging with common patterns."""
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    # Console handler (simple format)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (detailed format)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger

def logging_examples(logger: logging.Logger):
    """Examples of logging usage."""
    
    # Basic logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    
    # Logging with variables
    name = "John"
    age = 30
    logger.info(f"User {name} is {age} years old")
    
    # Logging exceptions
    try:
        raise ValueError("Example error")
    except Exception as e:
        logger.exception("An error occurred")  # Includes traceback
    
    # Logging with extra fields
    extra = {'user_id': 123}
    logger.info("User action", extra=extra)

#################
# sys           #
#################

def sys_patterns():
    """Common patterns with sys module."""
    
    # Command line arguments
    script_name = sys.argv[0]
    arguments = sys.argv[1:]
    
    # Standard streams
    sys.stdout.write("Normal output\n")
    sys.stderr.write("Error output\n")
    
    # Reading from stdin
    for line in sys.stdin:  # Only works in interactive/pipe context
        print(f"Got line: {line.strip()}")
    
    # Exit codes
    sys.exit(0)  # Success
    sys.exit(1)  # Error
    
    # Python version
    version = sys.version_info
    if version >= (3, 9):
        print("Using Python 3.9+")
    
    # Platform
    if sys.platform == "win32":
        print("Running on Windows")
    elif sys.platform == "linux":
        print("Running on Linux")
    
    # Module paths
    for path in sys.path:
        print(f"Python will look for modules in: {path}")
    
    # Memory usage
    size = sys.getsizeof([1, 2, 3])  # Size of object in bytes

def main():
    # Setup argument parser
    parser = setup_argparse()
    args = parse_and_validate_args(parser)
    
    # Setup logging
    logger = setup_logging(
        log_file=Path("app.log") if args.verbose else None,
        level="DEBUG" if args.verbose else "INFO"
    )
    
    # Main program logic
    try:
        # Synchronous operations
        requests_patterns()
        
        # Asynchronous operations
        run_async_code()
        
        # System operations
        sys_patterns()
        
    except Exception as e:
        logger.exception("Program failed")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()