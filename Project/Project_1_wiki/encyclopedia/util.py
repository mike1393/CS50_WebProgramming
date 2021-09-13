from logging import exception
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

import random

def search_entries(search_term=None):
    _, filenames = default_storage.listdir("entries")
    if search_term is not None:
        file_list=[]
        for filename in filenames:
            if filename.endswith(".md"):
                file = re.sub(r"\.md$", "", filename)
                if search_term.lower() == file.lower():
                    file_list.append(file)
                    return (0,file_list)
                elif search_term.lower() in file.lower():
                    file_list.append(file)
        return (1,file_list)
    else:
        return (0,list(sorted(re.sub(r"\.md$", "", filename)
                    for filename in filenames if filename.endswith(".md"))))




def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                    for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    try:
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return True
    except:
        filename = f"entries/{title}.md"
        default_storage.delete(filename)
        return False


def save_entry_safe(title, content):
    try:
        save_entry(title, content)
        return True
    except:
        if old_content is None:
            filename = f"entries/{title}.md"
            default_storage.delete(filename)
            return False
        else:
            save_entry_safe(title, old_content)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def show_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        md2 = Markdown()
        return md2.convert(f.read().decode("utf-8"))
    except FileNotFoundError:
        return None

def random_list():
    return random.choice(list_entries())