import os
import re
import json
import datetime
from util import parse_frontmatter, normalize_id, strip_order_prefix, get_section_title, build_url_path, extract_title, parse_ymd_date, get_file_modification_date_as_date, make_breadcrumb_to_article, make_breadcrumb_to_contribute_page, make_dashboard_breadcrumb_link, make_full_breadcrumb, load_style_config, get_docs_root_dir, extract_tags_from_frontmatter, get_docs_url

ROOT_DIR = get_docs_root_dir()
OUTPUT_DIR = os.path.join(ROOT_DIR, "99-contribute")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "review-page-template.md")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def clean_review_folder():
    if not os.path.exists(OUTPUT_DIR):
        return
    for fname in os.listdir(OUTPUT_DIR):
        if fname.endswith(".md") and fname.startswith("review-"):
            os.remove(os.path.join(OUTPUT_DIR, fname))

def create_location_breadcrumb(rel_path, article_title):
    """Create a breadcrumb showing the article's location."""
    parts = rel_path.split(os.sep)
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

def get_review_reason(frontmatter):
    """Extract review reason from frontmatter or generate default."""
    review_reason = frontmatter.get("review-reason", "")
    if review_reason:
        return review_reason
    
    # Generate default reason based on status and other fields
    status = frontmatter.get("status", "")
    if status == "review-needed":
        return "This article is ready for review and feedback before publication."
    
    # Check for other indicators
    if frontmatter.get("needs-review", ""):
        return frontmatter.get("needs-review", "")
    
    return "This article needs review to ensure quality and accuracy."

def create_review_page(md_path, rel_path, frontmatter, style_config):
    title = frontmatter.get("title", extract_title(md_path))
    id = f"review-{normalize_id(rel_path)}"
    filename = os.path.basename(md_path)
    
    # Create location breadcrumb
    location = create_location_breadcrumb(rel_path, title)
    
    # Get review reason
    review_reason = get_review_reason(frontmatter)
    
    # Get repository link for edit URL
    repo_link = style_config.get("repository_link", "https://github.com/YOUR_ORG/YOUR_REPO")
    edit_link = f"{repo_link}/edit/main/docs/{rel_path}"
    
    # Get status and other metadata
    status = frontmatter.get("status", "review-needed")
    author = frontmatter.get("author", "Unknown")
    topics = frontmatter.get("topics", [])
    level = frontmatter.get("level", "")
    
    # Format topics for display
    if isinstance(topics, list):
        topics_display = ", ".join(topics)
    else:
        topics_display = str(topics) if topics else "Not specified"
    
    template = load_template()
    content = template.format(
        title=title,
        id=id,
        location=location,
        review_reason=review_reason,
        edit_link=edit_link,
        filename=filename,
        status=status,
        author=author,
        topics=topics_display,
        level=level or "Not specified"
    )

    output_path = os.path.join(OUTPUT_DIR, id + ".md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created review page: {output_path}")

def walk_docs():
    clean_review_folder()
    style_config = load_style_config()
    
    review_articles = []
    
    for root, _, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith(".md") and f != "index.md":
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                frontmatter = parse_frontmatter(abs_path)
                
                # Normalize all frontmatter keys to lowercase
                frontmatter = {k.lower(): v for k, v in frontmatter.items()}
                
                status = frontmatter.get("status", "")
                
                # Check if article needs review
                if status == "review-needed":
                    review_articles.append({
                        'abs_path': abs_path,
                        'rel_path': rel_path,
                        'frontmatter': frontmatter
                    })
                    
                    create_review_page(abs_path, rel_path, frontmatter, style_config)
    
    print(f"📊 Found {len(review_articles)} articles needing review")
    return review_articles

if __name__ == "__main__":
    walk_docs() 