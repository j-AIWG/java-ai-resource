import os
import re
import sys
from util import get_docs_root_dir, parse_frontmatter

ROOT_DIR = get_docs_root_dir()
TEMPLATE_PATH = os.path.join(ROOT_DIR, ".template.md")

def load_template():
    """Load the template file and extract the frontmatter section."""
    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract frontmatter from template
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                template_frontmatter = '---' + parts[1] + '---'
                return template_frontmatter
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return None

def extract_existing_tags(file_path):
    """Extract existing tag values from a file's frontmatter."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.startswith('---'):
            return {}
        
        # Parse existing frontmatter
        frontmatter = parse_frontmatter(file_path)
        
        # Extract title from content if not in frontmatter
        if 'title' not in frontmatter:
            # Look for first # heading
            for line in content.split('\n'):
                if line.strip().startswith('# '):
                    frontmatter['title'] = line.strip().lstrip('# ').strip()
                    break
        
        return frontmatter
    except Exception as e:
        print(f"⚠️  Warning: Could not parse {file_path}: {e}")
        return {}

def update_file_template(file_path, template_frontmatter):
    """Update a file to use the new template while preserving existing values."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract existing tags
        existing_tags = extract_existing_tags(file_path)
        
        # Split content into frontmatter and body
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2].lstrip('\n')
            else:
                body = content
        else:
            body = content
        
        # Start with template frontmatter
        new_frontmatter_lines = template_frontmatter.split('\n')
        
        # Replace template values with existing values
        for i, line in enumerate(new_frontmatter_lines):
            line = line.strip()
            if ':' in line and not line.startswith('#') and not line.startswith('🧩'):
                # Extract key from template line
                key = line.split(':', 1)[0].strip()
                
                # If we have an existing value for this key, replace it
                if key in existing_tags:
                    value = existing_tags[key]
                    if isinstance(value, list):
                        # Handle array values
                        new_frontmatter_lines[i] = f"{key}: [{', '.join(value)}]"
                    else:
                        # Handle string values
                        new_frontmatter_lines[i] = f"{key}: {value}"
        
        # Reconstruct the file
        new_frontmatter = '\n'.join(new_frontmatter_lines)
        new_content = new_frontmatter + "\n\n" + body
        
        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"✔️  Updated template: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def walk_and_update_templates(directory, template_frontmatter):
    """Walk through directory and update all markdown files."""
    update_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.md') and file != '.template.md':
                file_path = os.path.join(root, file)
                if update_file_template(file_path, template_frontmatter):
                    update_count += 1
    
    return update_count

def main():
    """Main function to update all markdown files to use the new template."""
    print("🔄 Updating all markdown files to use new template...")
    
    # Load the template
    template_frontmatter = load_template()
    if not template_frontmatter:
        print("❌ Could not load template")
        return
    
    print("📋 Template loaded successfully")
    
    # Update all files
    update_count = walk_and_update_templates(ROOT_DIR, template_frontmatter)
    
    print(f"✅ Updated {update_count} files to use new template")

if __name__ == "__main__":
    main() 