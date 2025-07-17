# flatmap-tools/util.py
import os
import re
import json
import datetime

STYLE_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "flatmap-style.config.json"))


def load_style_config():
    try:
        with open(STYLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        config = {"tags": {}}
        
        # Find the tags section
        tags_start = content.find('"tags":')
        if tags_start == -1:
            return config
        
        # Extract everything from tags: to the end
        tags_content = content[tags_start:]
        
        # Find the opening brace of tags object
        brace_start = tags_content.find('{')
        if brace_start == -1:
            return config
        
        # Find the matching closing brace
        brace_count = 1
        brace_end = brace_start + 1
        while brace_count > 0 and brace_end < len(tags_content):
            if tags_content[brace_end] == '{':
                brace_count += 1
            elif tags_content[brace_end] == '}':
                brace_count -= 1
            brace_end += 1
        
        if brace_count > 0:
            return config
        
        tags_section = tags_content[brace_start + 1:brace_end - 1]
        
        # Parse each tag entry
        current_pos = 0
        while current_pos < len(tags_section):
            # Find the next quote (start of key)
            quote_start = tags_section.find('"', current_pos)
            if quote_start == -1:
                break
            
            # Find the end of the key
            quote_end = tags_section.find('"', quote_start + 1)
            if quote_end == -1:
                break
            
            key = tags_section[quote_start + 1:quote_end]
            
            # Find the opening brace of the value
            brace_start = tags_section.find('{', quote_end)
            if brace_start == -1:
                break
            
            # Find the closing brace of the value
            brace_count = 1
            brace_end = brace_start + 1
            while brace_count > 0 and brace_end < len(tags_section):
                if tags_section[brace_end] == '{':
                    brace_count += 1
                elif tags_section[brace_end] == '}':
                    brace_count -= 1
                brace_end += 1
            
            if brace_count > 0:
                break
            
            value_section = tags_section[brace_start + 1:brace_end - 1]
            
            # Parse the value object
            properties = []
            
            # Split by commas and parse each property
            prop_parts = value_section.split(',')
            for part in prop_parts:
                part = part.strip()
                if ':' in part:
                    # Find the colon
                    colon_pos = part.find(':')
                    prop_key = part[:colon_pos].strip().strip('"')
                    prop_value = part[colon_pos + 1:].strip().strip('"')
                    
                    if prop_key and prop_value:
                        properties.append((prop_key, prop_value))
            
            # Add or merge the tag
            if key in config["tags"]:
                # Key already exists, extend the list
                config["tags"][key].extend(properties)
            else:
                # New key, create list
                config["tags"][key] = properties
            
            # Move to next tag
            current_pos = brace_end
            comma_pos = tags_section.find(',', current_pos)
            if comma_pos == -1:
                break
            current_pos = comma_pos + 1
        
        return config
    except Exception as e:
        print(f"⚠️  Warning: Could not load style config: {e}")
        return {"tags": {}}


def get_base_folder():
    """Get the base folder name from config, with fallback to auto-detection."""
    config = load_style_config()
    config_base_folder = config.get("base_folder")
    
    # Auto-detect: find the folder that contains flatmap-tools
    current_dir = os.path.dirname(__file__)  # flatmap-tools directory
    parent_dir = os.path.dirname(current_dir)  # parent of flatmap-tools
    detected_base_folder = os.path.basename(parent_dir)
    
    # If config value exists but doesn't match reality, use the detected value
    if config_base_folder and config_base_folder != detected_base_folder:
        print(f"⚠️  Config base_folder '{config_base_folder}' doesn't match actual folder '{detected_base_folder}'. Using detected value.")
        return detected_base_folder
    
    # If config value exists and matches reality, use it
    if config_base_folder:
        return config_base_folder
    
    # Fallback to auto-detection
    return detected_base_folder


def get_docs_root_dir():
    """Get the absolute path to the docs directory within the base folder."""
    base_folder = get_base_folder()
    # Find the absolute path to the base folder (parent of flatmap-tools)
    flatmap_tools_dir = os.path.dirname(__file__)
    base_folder_path = os.path.dirname(flatmap_tools_dir)
    return os.path.abspath(os.path.join(base_folder_path, "docs"))


def parse_frontmatter(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            return {}
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        frontmatter_text = match.group(1)
        tags = {}
        lines = frontmatter_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Skip empty lines, comments, and section headers
            if not line or line.startswith('#') or line.startswith('🧩'):
                i += 1
                continue
            # Look for key-value pairs
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                # Skip if the key is a comment or section marker
                if key.startswith('#') or key.startswith('🧩'):
                    i += 1
                    continue
                
                # Handle array values first
                if value.startswith('[') and value.endswith(']'):
                    array_content = value[1:-1]
                    value = [item.strip() for item in array_content.split(',')] if array_content.strip() else []
                # Handle quoted strings
                elif value.startswith(('"', "'")) and value.endswith(('"', "'")):
                    value = value[1:-1]
                
                # Strip comments from values (everything after #)
                if isinstance(value, str):
                    value = value.split('#')[0].strip()
                
                tags[key] = value
            i += 1
        return tags
    except Exception as e:
        print(f"⚠️  Could not parse frontmatter from {file_path}: {e}")
        return {}


def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("# "):
                    return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"


def extract_tags_from_frontmatter(frontmatter):
    tags = []
    tag_fields = ['type', 'status', 'level', 'visibility', 'collaboration', 'feature-priority']
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, str):
                tags.append(f"{field}:{value}")
    if 'topics' in frontmatter and isinstance(frontmatter['topics'], list):
        for topic in frontmatter['topics']:
            if isinstance(topic, str):
                tags.append(topic)
    return tags


def normalize_id(path):
    id_raw = path.replace("/", "_").replace("-", "_").replace(".", "_")
    return id_raw


def strip_order_prefix(name):
    return re.sub(r"^\d{2,}-", "", name)


def get_rel_path_from_root(path, root_dir="docs"):
    abs_path = os.path.abspath(path)
    root_path = os.path.abspath(os.path.join(os.getcwd(), root_dir))
    return os.path.relpath(abs_path, root_path)


def get_file_modification_date(path):
    try:
        return os.path.getmtime(path)
    except:
        return 0


def get_section_title(folder_path):
    """Extract the title from a folder's index.md file, or fallback to folder name."""
    index_path = os.path.join(folder_path, "index.md")
    if os.path.exists(index_path):
        frontmatter = parse_frontmatter(index_path)
        return frontmatter.get("title", os.path.basename(folder_path).replace("-", " ").title())
    else:
        return os.path.basename(folder_path).replace("-", " ").title()


def build_url_path(parts):
    """Join folder parts, stripping numeric prefixes, to form a correct URL path."""
    return "/".join(strip_order_prefix(part) for part in parts)


def parse_ymd_date(date_str):
    """Parse a YYYY-MM-DD string to a datetime.date, or None if invalid."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def get_file_modification_date_as_date(path):
    try:
        ts = os.path.getmtime(path)
        return datetime.date.fromtimestamp(ts)
    except Exception:
        return None


def make_breadcrumb_to_article(rel_path, article_title=None, root_dir=None):
    if root_dir is None:
        raise ValueError('root_dir must be provided')
    parts = rel_path.split(os.sep)
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    crumbs = []
    for i, part in enumerate(parts[:-1]):
        folder_path = os.path.join(root_dir, *parts[:i+1])
        title = get_section_title(folder_path)
        url_path = build_url_path(parts[:i+1])
        docs_url = get_docs_url(url_path)
        crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{title}</a>')
    art_title = article_title if article_title else extract_title(os.path.join(root_dir, rel_path))
    url_path = build_url_path(parts)
    docs_url = get_docs_url(url_path)
    crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{art_title}</a>')
    return " > ".join(crumbs)


def make_breadcrumb_to_contribute_page(rel_path, article_title=None, root_dir=None):
    if root_dir is None:
        raise ValueError('root_dir must be provided')
    parts = rel_path.split(os.sep)
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    crumbs = []
    for i, part in enumerate(parts[:-1]):
        folder_path = os.path.join(root_dir, *parts[:i+1])
        title = get_section_title(folder_path)
        url_path = build_url_path(parts[:i+1])
        docs_url = get_docs_url(url_path)
        crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{title}</a>')
    art_title = article_title if article_title else extract_title(os.path.join(root_dir, rel_path))
    id = f"contribute-{normalize_id(rel_path)}"
    docs_url = get_docs_url(f"contribute/{id}")
    crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{art_title}</a>')
    return " > ".join(crumbs)


def make_dashboard_breadcrumb_link(rel_path, article_title=None, to_contribute_page=False, root_dir=None):
    if root_dir is None:
        raise ValueError('root_dir must be provided')
    parts = rel_path.split(os.sep)
    # Remove .md from last part
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    # Max 2 upstreams
    upstreams = parts[:-1][-2:]
    crumb_text = []
    for i, part in enumerate(upstreams):
        folder_path = os.path.join(root_dir, *parts[:-(len(upstreams)-i)])
        title = get_section_title(folder_path)
        crumb_text.append(title)
    
    # Get the article title
    art_title = article_title if article_title else extract_title(os.path.join(root_dir, rel_path))
    
    # Check if this is an index.md file (last part is index)
    is_index_file = rel_path.endswith('index.md')
    
    # For index.md files, don't add the article title if it's the same as the last folder name
    if is_index_file and len(parts) > 1:
        last_folder_path = os.path.join(root_dir, *parts[:-1])
        last_folder_title = get_section_title(last_folder_path)
        if art_title == last_folder_title:
            # Don't add the article title to avoid duplication
            text = " > ".join(crumb_text)
        else:
            # Add the article title if it's different
            crumb_text.append(art_title)
            text = " > ".join(crumb_text)
    else:
        # For regular files, always add the article title
        crumb_text.append(art_title)
        text = " > ".join(crumb_text)
    
    if to_contribute_page:
        id = f"contribute-{normalize_id(rel_path)}"
        docs_url = get_docs_url(f"contribute/{id}")
        url = docs_url
    else:
        url_path = build_url_path(parts)
        docs_url = get_docs_url(url_path)
        url = docs_url
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'


def make_full_breadcrumb(rel_path, article_title=None, root_dir=None):
    if root_dir is None:
        raise ValueError('root_dir must be provided')
    parts = rel_path.split(os.sep)
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    crumbs = []
    for i, part in enumerate(parts[:-1]):
        folder_path = os.path.join(root_dir, *parts[:i+1])
        title = get_section_title(folder_path)
        url_path = build_url_path(parts[:i+1])
        docs_url = get_docs_url(url_path)
        crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{title}</a>')
    art_title = article_title if article_title else extract_title(os.path.join(root_dir, rel_path))
    url_path = build_url_path(parts)
    docs_url = get_docs_url(url_path)
    crumbs.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{art_title}</a>')
    return " > ".join(crumbs)


def get_base_url():
    """Get the base URL for the site by reading from docusaurus.config.js."""
    # Find the docusaurus.config.js file
    flatmap_tools_dir = os.path.dirname(__file__)
    base_folder_path = os.path.dirname(flatmap_tools_dir)
    config_path = os.path.join(base_folder_path, "docusaurus.config.js")
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for baseUrl: '/something/'
        import re
        match = re.search(r"baseUrl:\s*['\"]([^'\"]*)['\"]", content)
        if match:
            base_url = match.group(1)
            # Remove trailing slash if present
            if base_url.endswith('/'):
                base_url = base_url[:-1]
            return base_url
    except Exception as e:
        print(f"⚠️  Warning: Could not read baseUrl from docusaurus.config.js: {e}")
    
    # Fallback: no base URL
    return ''


def get_docs_url(path=""):
    """Generate a docs URL with proper base URL handling."""
    base_url = get_base_url()
    docs_path = f"/docs/{path}" if path else "/docs"
    return f"{base_url}{docs_path}"


def get_repository_link_from_config():
    try:
        with open(STYLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if '"repository_link"' in line:
                    # Extract the value between the first pair of double quotes after the colon
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        value = parts[1].strip().strip(',').strip().strip('"')
                        value = value.replace('"', '').replace(',', '').strip()
                        if value:
                            return value
        # fallback
        return "https://github.com/YOUR_USERNAME/YOUR_REPO"
    except Exception as e:
        print(f"⚠️  Warning: Could not load repository_link from style config: {e}")
        return "https://github.com/YOUR_USERNAME/YOUR_REPO"
