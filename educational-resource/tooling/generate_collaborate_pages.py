import os
import re
import json
import datetime
from util import parse_frontmatter, normalize_id, strip_order_prefix, get_section_title, build_url_path, extract_title, parse_ymd_date, get_file_modification_date_as_date, make_breadcrumb_to_article, make_breadcrumb_to_contribute_page, make_dashboard_breadcrumb_link, make_full_breadcrumb, load_style_config, get_docs_root_dir, extract_tags_from_frontmatter, get_docs_url, get_repository_link_from_config

ROOT_DIR = get_docs_root_dir()
OUTPUT_DIR = os.path.join(ROOT_DIR, "99-contribute")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "collaborate-page-template.md")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def clean_collaborate_folder():
    if not os.path.exists(OUTPUT_DIR):
        return
    for fname in os.listdir(OUTPUT_DIR):
        if fname.endswith(".md") and fname.startswith("collaborate-"):
            os.remove(os.path.join(OUTPUT_DIR, fname))

def get_author_info(author_field):
    """Extract author name and handle from author field."""
    if isinstance(author_field, list) and len(author_field) > 0:
        # Handle array format: ["Name (@github)", "Name (@github)"]
        author = author_field[0]  # Take the first author for now
    elif isinstance(author_field, str):
        author = author_field
    else:
        return "Unknown Author", "unknown"
    
    # Handle the format: "Name (@github)"
    # Pattern to match: "Name (@github)" or just "Name"
    author_pattern = r'"([^"]+)"\s*\(@([^)]+)\)'
    match = re.search(author_pattern, author)
    
    if match:
        # Format: "Name (@github)"
        author_name = match.group(1).strip()
        handle = match.group(2).strip()
    else:
        # Try to extract handle from @username format in the string
        handle_match = re.search(r'@(\w+)', author)
        handle = handle_match.group(1) if handle_match else "unknown"
        
        # Clean up author name - remove the @handle part and any parentheses
        author_name = re.sub(r'@\w+', '', author).strip()
        author_name = re.sub(r'\([^)]*\)', '', author_name).strip()  # Remove any existing parentheses
        author_name = re.sub(r'^["\']|["\']$', '', author_name).strip()  # Remove quotes
        
        # If no name left after removing handle and parentheses, return just the handle
        if not author_name:
            return f"@{handle}", handle
    
    return author_name, handle

def create_location_breadcrumb(rel_path, article_title):
    """Create a breadcrumb showing the article's location, matching the contribute page format."""
    parts = rel_path.split(os.sep)
    filename = parts[-1] if parts else ""
    
    # Handle index.md files specially - link to folder, not file
    if filename == "index.md":
        # Remove the index.md part and link to the folder
        parts = parts[:-1]
        if len(parts) > 0:
            location_parts = []
            for i in range(len(parts)):
                folder_path = os.path.join(ROOT_DIR, *parts[:i+1])
                folder_title = get_section_title(folder_path)
                url_path = build_url_path(parts[:i+1])
                docs_url = get_docs_url(url_path)
                location_parts.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{folder_title}</a>')
            location = " > ".join(location_parts)
        else:
            location = "Root"
    else:
        # Handle regular files
        if parts[-1].endswith('.md'):
            parts[-1] = parts[-1][:-3]
        
        if len(parts) > 1:
            location_parts = []
            for i in range(len(parts)-1):
                folder_path = os.path.join(ROOT_DIR, *parts[:i+1])
                folder_title = get_section_title(folder_path)
                url_path = build_url_path(parts[:i+1])
                docs_url = get_docs_url(url_path)
                location_parts.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{folder_title}</a>')
            # Add the article title as the final part
            url_path = build_url_path(parts)
            docs_url = get_docs_url(url_path)
            location_parts.append(f'<a href="{docs_url}" target="_blank" rel="noopener noreferrer">{article_title}</a>')
            location = " > ".join(location_parts)
        else:
            location = "Root"
    
    return location

def create_discussion_link(title, author_handle, style_config):
    """Create a GitHub discussion link with pre-filled content."""
    repo_link = get_repository_link_from_config()
    discussion_url = f"{repo_link}/discussions/new"
    
    # URL encode the parameters
    import urllib.parse
    params = {
        'category': 'collaboration',
        'title': f"I'd like to collaborate on {title}",
        'body': f"Hi @{author_handle}, I'd love to help with the \"{title}\" article.\nLet me know how best to team up!"
    }
    
    query_string = "&".join([f"{k}={urllib.parse.quote(v)}" for k, v in params.items()])
    return f"{discussion_url}?{query_string}"

def get_suggested_contributions(topics, level):
    """Generate suggested contributions based on topics and level."""
    suggestions = []
    
    if topics:
        if isinstance(topics, list):
            topic_list = topics
        else:
            topic_list = [topics]
        
        for topic in topic_list:
            if 'tutorial' in topic.lower():
                suggestions.append("step-by-step examples")
            elif 'benchmark' in topic.lower():
                suggestions.append("performance data")
            elif 'api' in topic.lower():
                suggestions.append("code samples")
            elif 'overview' in topic.lower():
                suggestions.append("explanatory content")
    
    if level:
        level_lower = level.lower()
        if 'beginner' in level_lower:
            suggestions.append("beginner-friendly explanations")
        elif 'advanced' in level_lower or 'expert' in level_lower:
            suggestions.append("advanced techniques")
    
    if not suggestions:
        suggestions = ["examples", "improvements", "additional content"]
    
    return " or ".join(suggestions[:3])  # Limit to 3 suggestions

def create_collaboration_page(md_path, rel_path, frontmatter, style_config):
    title = frontmatter.get("title", extract_title(md_path))
    id = f"collaborate-{normalize_id(rel_path)}"
    filename = os.path.basename(md_path)
    
    # Extract author information
    author_field = frontmatter.get("author", "")
    author_name, author_handle = get_author_info(author_field)
    
    # Create author display with handle
    if author_handle != "unknown":
        # If author_name is just the handle with @ prefix, don't show it twice
        if author_name == f"@{author_handle}":
            author_display = f'<a href="https://github.com/{author_handle}" target="_blank" rel="noopener noreferrer">@{author_handle}</a>'
        else:
            # Show name and handle in parentheses format: "Name (@handle)"
            author_display = f"{author_name} (<a href=\"https://github.com/{author_handle}\" target=\"_blank\" rel=\"noopener noreferrer\">@{author_handle}</a>)"
    else:
        author_display = author_name
    
    # Create location breadcrumb
    location = create_location_breadcrumb(rel_path, title)
    
    # Create discussion link
    discussion_link = create_discussion_link(title, author_handle, style_config)
    
    # Get suggested contributions
    topics = frontmatter.get("topics", [])
    level = frontmatter.get("level", "")
    suggested_contributions = get_suggested_contributions(topics, level)
    
    # Format topics for display
    if isinstance(topics, list):
        topics_display = ", ".join(topics)
    else:
        topics_display = str(topics) if topics else "Not specified"
    
    # Get description from collaboration-topic or use default
    collaboration_topic = frontmatter.get("collaboration-topic", "")
    if collaboration_topic:
        description = f"This article needs collaboration to be completed. Here's what the author wrote: {collaboration_topic}"
    else:
        description = "This article needs collaboration to be completed. The author is looking for help with content, examples, or improvements."
    
    # Get status and ETA
    status = frontmatter.get("status", "draft")
    eta = frontmatter.get("eta", "Not specified")
    
    template = load_template()
    content = template.format(
        title=title,
        id=id,
        author=author_display,
        author_handle=author_handle,
        location=location,
        discussion_link=discussion_link,
        suggested_contributions=suggested_contributions,
        topics=topics_display,
        level=level or "Not specified",
        status=status,
        eta=eta,
        description=description,
        filename=filename
    )

    output_path = os.path.join(OUTPUT_DIR, id + ".md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created collaboration page: {output_path}")

def walk_docs():
    clean_collaborate_folder()
    style_config = load_style_config()
    
    collaboration_articles = []
    
    for root, _, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith(".md") and f != "index.md":
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                frontmatter = parse_frontmatter(abs_path)
                
                # Normalize all frontmatter keys to lowercase
                frontmatter = {k.lower(): v for k, v in frontmatter.items()}
                
                status = frontmatter.get("status", "")
                collaboration = frontmatter.get("collaboration", "")
                author = frontmatter.get("author", "")
                
                # Check if article is open for collaboration and not published
                if (status in ["draft", "wip", "review-needed"] and 
                    collaboration == "open" and 
                    author and 
                    status != "published"):
                    
                    collaboration_articles.append({
                        'abs_path': abs_path,
                        'rel_path': rel_path,
                        'frontmatter': frontmatter
                    })
                    
                    create_collaboration_page(abs_path, rel_path, frontmatter, style_config)
    
    print(f"📊 Found {len(collaboration_articles)} articles open for collaboration")
    return collaboration_articles

if __name__ == "__main__":
    walk_docs() 