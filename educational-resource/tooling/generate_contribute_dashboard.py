import sys
import os

# Ensure the script directory is in the path
sys.path.append(os.path.dirname(__file__))

from generate_contribute_pages import walk_docs as generate_contribute_pages

def main():
    print("Generating all contribute and collaboration pages...")
    generate_contribute_pages()
    print("All contribute and collaboration pages, and the dashboard, have been generated.")

if __name__ == "__main__":
    main() 