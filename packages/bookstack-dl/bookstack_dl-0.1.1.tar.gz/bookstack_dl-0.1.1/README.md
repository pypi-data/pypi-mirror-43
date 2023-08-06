# bookstack-dl

Python module to help automatically export all pages in a bookstack instances.
This will crawl through the web api, listing all books, chapters, and pages.
Then, it will download them in a folder heirarchy.

## Installation

```bash
pip install bookstack_dl
```

## Usage

```python
from bookstack_dl import BookstackAPI

# Initiate and log in.
bs = BookstackAPI("https://your.bookstackinstall.com", "user@email.com", "userpassword")

# kick off gathering meta data
bs.get_all_books()

# download all
bs.download_all("<full_path_to_root_download_dir>")
```

## Python Dependencies

Currently, this requires Python 3.6+ due to the use of f-strings.
The os.makedirs exist_ok option requires 3.5+.
Contributions are welcome to help lower the minimum required version.
