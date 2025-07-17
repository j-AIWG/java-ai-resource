import os
import re
import json
import sys
from util import get_docs_root_dir, parse_frontmatter

ROOT_DIR = get_docs_root_dir()
BANNER_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "banners.config.json"))

def load_banner_config():
    """Load banner configuration from JSON file."""
    try:
        with open(BANNER_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load banner config from {BANNER_CONFIG_PATH}: {e}")
        return {"banners": {}}

def create_banner_html(banner_config, review_reason=None):
    """Create HTML banner based on configuration."""
    banner_type = banner_config.get("type", "info")
    title = banner_config.get("title", "")
    content = banner_config.get("content", "")
    content_template = banner_config.get("content_template", "")
    
    # Handle template content (for review-needed)
    if content_template and review_reason:
        content = content_template.format(review_reason=review_reason)
    
    # Determine CSS classes based on type
    if banner_type == "warning":
        css_class = "alert alert--warning"
    elif banner_type == "info":
        css_class = "alert alert--info"
    else:
        css_class = "alert alert--info"
    
    return f""":::note {title}
{content}
:::"""

def remove_existing_banners(content):
    """Remove any existing banners from the content."""
    # Remove Docusaurus alert blocks
    content = re.sub(r':::note.*?\n.*?\n:::', '', content, flags=re.DOTALL)
    content = re.sub(r':::warning.*?\n.*?\n:::', '', content, flags=re.DOTALL)
    content = re.sub(r':::info.*?\n.*?\n:::', '', content, flags=re.DOTALL)
    content = re.sub(r':::tip.*?\n.*?\n:::', '', content, flags=re.DOTALL)
    content = re.sub(r':::caution.*?\n.*?\n:::', '', content, flags=re.DOTALL)
    
    # Remove any other common banner patterns
    content = re.sub(r'<div class="alert.*?</div>', '', content, flags=re.DOTALL)
    
    return content

def split_frontmatter_and_body(content):
    """Split content into frontmatter and body."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = '---' + parts[1] + '---'
            body = parts[2].lstrip('\n')
            return frontmatter, body
    return '', content

def add_banner_to_file(file_path, banner_config):
    """Add appropriate banner to a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter = parse_frontmatter(file_path)
        status = frontmatter.get('status', '')
        
        # Check if we need a banner for this status
        status_key = f"status:{status}"
        if status_key not in banner_config.get("banners", {}):
            return False  # No banner needed
        
        banner_spec = banner_config["banners"][status_key]
        
        # Check if review_reason is required but missing
        if banner_spec.get("requires_review_reason", False):
            review_reason = frontmatter.get('review-reason', '')
            if not review_reason:
                print(f"⚠️  Warning: {file_path} has status '{status}' but no review-reason")
                return False
        
        # Remove existing banners
        content = remove_existing_banners(content)
        
        # Split into frontmatter and body
        frontmatter_text, body = split_frontmatter_and_body(content)
        
        # Create banner
        review_reason = frontmatter.get('review-reason', '') if banner_spec.get("requires_review_reason", False) else None
        banner_html = create_banner_html(banner_spec, review_reason)
        
        # Reconstruct content with banner
        if frontmatter_text:
            new_content = frontmatter_text + "\n\n" + banner_html + "\n\n" + body
        else:
            new_content = banner_html + "\n\n" + body
        
        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"✔️  Added banner to: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def walk_and_add_banners(directory, banner_config):
    """Walk through directory and add banners to markdown files."""
    banner_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.md') and file != '_intro.md':
                file_path = os.path.join(root, file)
                if add_banner_to_file(file_path, banner_config):
                    banner_count += 1
    
    return banner_count

def main():
    """Main function to add banners to all markdown files."""
    print("🎯 Adding banners to markdown files...")
    
    banner_config = load_banner_config()
    if not banner_config.get("banners"):
        print("❌ No banner configuration found")
        return
    
    banner_count = walk_and_add_banners(ROOT_DIR, banner_config)
    
    print(f"✅ Added banners to {banner_count} files")

if __name__ == "__main__":
    main() 