from pathlib import Path
import shutil

def clean_public():
    public_dir = Path(__file__).parent.parent / "public"

    if public_dir.exists():
        for item in public_dir.iterdir():
            if item.name == '__init__.py':
                continue
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

def process_content():
    content_dir = Path(__file__).parent.parent / "content"

    if content_dir.exists():
        for cont in content_dir.iterdir():
            pass

def convert_page():
    pass

def convert_block():
    pass

def fill_public():
    pass