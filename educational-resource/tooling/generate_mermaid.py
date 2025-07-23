import os
import re
import json
from util import get_docs_root_dir, load_style_config, get_docs_url

ROOT_DIR = get_docs_root_dir()
DO_NOT_EDIT = "<!-- AUTO-GENERATED FILE — DO NOT EDIT. Regenerated on merge -->"
STYLE_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "flatmap-style.config.json"))

def get_max_depth():
    """Get the maximum depth from style config."""
    style_config = load_style_config()
    return style_config.get("flatmap_depth", 4)

def parse_frontmatter(file_path):
    """Parse frontmatter from a markdown file and extract tags."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Check if file has frontmatter (starts with ---)
        if not content.startswith("---"):
            return {}
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return {}
        frontmatter_text = frontmatter_match.group(1)
        tags = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            # Ignore commented-out lines
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    # Remove inline comments (everything after #)
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    # Handle array values like topics: [agents, lifecycle]
                    if value.startswith('[') and value.endswith(']'):
                        try:
                            array_content = value[1:-1]
                            if array_content.strip():
                                value = [item.strip() for item in array_content.split(',')]
                            else:
                                value = []
                        except:
                            value = []
                    elif value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    tags[key] = value
    except Exception as e:
        print(f"⚠️  Warning: Could not parse frontmatter from {file_path}: {e}")
        return {}
    return tags

def evaluate_tag_condition(condition, frontmatter):
    """Evaluate a tag condition like 'author:not_empty AND status:draft'."""
    if ' AND ' in condition:
        # Handle AND conditions
        parts = condition.split(' AND ')
        return all(evaluate_simple_condition(part.strip(), frontmatter) for part in parts)
    else:
        # Handle simple conditions
        return evaluate_simple_condition(condition, frontmatter)

def evaluate_simple_condition(condition, frontmatter):
    """Evaluate a simple condition like 'author:not_empty' or 'status:draft'."""
    if ':' not in condition:
        return False
    
    field, value = condition.split(':', 1)
    
    if value == 'not_empty':
        field_value = frontmatter.get(field, '')
        return isinstance(field_value, str) and field_value.strip() != ''
    elif value == 'is_empty':
        field_value = frontmatter.get(field, '')
        return not isinstance(field_value, str) or field_value.strip() == ''
    else:
        # Direct value comparison - case insensitive for all fields
        field_value = frontmatter.get(field)
        if isinstance(field_value, str):
            return field_value.lower() == value.lower()
        else:
            return field_value == value

def extract_tags_from_frontmatter(frontmatter):
    """Extract all possible tags from frontmatter for styling."""
    tags = []
    
    # Direct tag fields
    tag_fields = ['type', 'status', 'level', 'visibility']
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, str):
                tags.append(f"{field}:{value}")
    
    # Handle external-link field
    if 'external-link' in frontmatter:
        value = frontmatter['external-link']
        if isinstance(value, str):
            tags.append(f"external-link:{value}")
    
    # Handle programming-language field (case insensitive)
    if 'programming-language' in frontmatter:
        value = frontmatter['programming-language']
        if isinstance(value, str):
            # Add both the original value and a case-insensitive version
            tags.append(f"programming-language:{value}")
            tags.append(f"programming-language:{value.lower()}")
    
    # Handle topics array
    if 'topics' in frontmatter:
        topics = frontmatter['topics']
        if isinstance(topics, list):
            for topic in topics:
                if isinstance(topic, str) and ':' in topic:
                    tags.append(topic)
    
    # Handle conditional tags
    # author:not_empty - when author field is not empty
    author = frontmatter.get('author', '')
    if isinstance(author, str) and author.strip():
        tags.append('author:not_empty')
    else:
        tags.append('author:is_empty')
    
    # General is_empty/is_not_empty for any field
    for field, value in frontmatter.items():
        if isinstance(value, str):
            if value.strip():
                tags.append(f"{field}:is_not_empty")
            else:
                tags.append(f"{field}:is_empty")
        elif value is None or value == "":
            tags.append(f"{field}:is_empty")
        else:
            tags.append(f"{field}:is_not_empty")
    
    return tags

def apply_styling_to_node(tags, style_config, frontmatter=None):
    """Apply styling to a node based on tags and style config."""
    styles = {
        'left_icons': [],   # Icons for left side
        'right_icons': [],  # Icons for right side
        'border_colors': [],  # List of border colors
        'background_colors': [],  # List of background colors
        'background_opacities': [],  # List of background opacities
        'text_colors': [],  # List of text colors
        'border_styles': [],  # List of border styles
        'border_widths': [],  # List of border widths
        'clickable': True,
        'exclude': False
    }
    
    # Process all config entries to accumulate properties
    for config_tag, tag_properties in style_config.get('tags', {}).items():
        # Check if this config entry matches any of our tags
        tag_matches = False
        
        # Handle simple tags
        if config_tag in tags:
            tag_matches = True
        
        # Handle complex conditions (AND conditions)
        elif ' AND ' in config_tag and frontmatter:
            if evaluate_tag_condition(config_tag, frontmatter):
                tag_matches = True
        
        # Apply all properties from matching tags
        if tag_matches:
            # Handle both list of property tuples and dict format
            if isinstance(tag_properties, list):
                # Old format: list of tuples
                for prop_key, prop_value in tag_properties:
                    if prop_key == 'icon':
                        # Check if this tag has icon_side specified
                        icon_side = 'left'  # default
                        for check_key, check_value in tag_properties:
                            if check_key == 'icon_side':
                                icon_side = check_value
                                break
                        
                        if icon_side == 'right':
                            styles['right_icons'].append(prop_value)
                        else:
                            styles['left_icons'].append(prop_value)
                    elif prop_key == 'border_color':
                        styles['border_colors'].append(prop_value)
                    elif prop_key == 'background_color':
                        styles['background_colors'].append(prop_value)
                    elif prop_key == 'text_color':
                        styles['text_colors'].append(prop_value)
                    elif prop_key == 'border_style':
                        styles['border_styles'].append(prop_value)
                    elif prop_key == 'border_width':
                        styles['border_widths'].append(prop_value)
                    elif prop_key == 'exclude':
                        styles['exclude'] = prop_value
            else:
                # New format: dict
                for prop_key, prop_value in tag_properties.items():
                    if prop_key == 'icon':
                        icon_side = tag_properties.get('icon_side', 'left')
                        if icon_side == 'right':
                            styles['right_icons'].append(prop_value)
                        else:
                            styles['left_icons'].append(prop_value)
                    elif prop_key == 'border_color':
                        styles['border_colors'].append(prop_value)
                    elif prop_key == 'background_color':
                        styles['background_colors'].append(prop_value)
                    elif prop_key == 'background_opacity':
                        styles['background_opacities'].append(prop_value)
                    elif prop_key == 'text_color':
                        styles['text_colors'].append(prop_value)
                    elif prop_key == 'border_style':
                        styles['border_styles'].append(prop_value)
                    elif prop_key == 'border_width':
                        styles['border_widths'].append(prop_value)
                    elif prop_key == 'exclude':
                        styles['exclude'] = prop_value
    
    return styles

def create_mermaid_node_style(styles, default_fill=None):
    """Create Mermaid-compatible styling for a node."""
    style_parts = []
    
    # Use the last background color, or default
    background_colors = styles.get('background_colors', [])
    background_opacities = styles.get('background_opacities', [])
    fill_color = background_colors[-1] if background_colors else default_fill
    
    if fill_color:
        # Apply opacity if specified
        if background_opacities:
            opacity = background_opacities[-1]
            # For Mermaid, we can use rgba or add opacity to hex colors
            if fill_color.startswith('#') and len(fill_color) == 7:
                # Convert hex to rgba for opacity support
                r = int(fill_color[1:3], 16)
                g = int(fill_color[3:5], 16)
                b = int(fill_color[5:7], 16)
                try:
                    opacity_val = float(opacity)
                    style_parts.append(f"fill:rgba({r},{g},{b},{opacity_val})")
                except:
                    style_parts.append(f"fill:{fill_color}")
            else:
                # For named colors, just use the color (Mermaid doesn't support opacity for named colors)
                style_parts.append(f"fill:{fill_color}")
        else:
            style_parts.append(f"fill:{fill_color}")
    
    # Use the last border color if available
    border_colors = styles.get('border_colors', [])
    if border_colors:
        border_color = border_colors[-1]
        border_styles = styles.get('border_styles', [])
        border_style = border_styles[-1] if border_styles else 'solid'
        border_widths = styles.get('border_widths', [])
        border_width = border_widths[-1] if border_widths else '2px'
        
        style_parts.append(f"stroke:{border_color}")
        style_parts.append(f"stroke-width:{border_width}")
        style_parts.append(f"stroke-dasharray:{'5,5' if border_style == 'dashed' else '1,1' if border_style == 'dotted' else '0'}")
    
    # Use the last text color if available
    text_colors = styles.get('text_colors', [])
    if text_colors:
        style_parts.append(f"color:{text_colors[-1]}")
    
    return ",".join(style_parts) if style_parts else None

def has_author_and_draft(frontmatter):
    """Check if an article has an author and is in draft status."""
    status = frontmatter.get('status', '')
    author = frontmatter.get('author', '')
    
    # Check if status is draft
    is_draft = status == 'draft'
    
    # Check if author exists (handle string format: "Name" (@github), "Name" (@github))
    has_author = False
    if isinstance(author, str) and author.strip():
        has_author = True
    
    return is_draft and has_author

def create_node_label(title, styles, is_external=False, external_url=None):
    """Create the label for a node with optional icons and external link."""
    label_parts = []
    
    # Add left icons first
    if styles.get('left_icons'):
        label_parts.extend(styles['left_icons'])
    
    # Add the title
    safe_title = title.replace('"', "'")
    label_parts.append(safe_title)
    
    # Add right icons after the title
    if styles.get('right_icons'):
        label_parts.extend(styles['right_icons'])
    
    label = " ".join(label_parts)
    if is_external and external_url:
        return f"<a href='{external_url}' target='_blank' rel='noopener noreferrer'>{label}</a>"
    return label

def strip_order_prefix(name):
    return re.sub(r"^\d{2,}-", "", name)

def normalize_id(path):
    id_raw = path.replace("/", "_").replace("-", "_").replace(".", "_")
    return f"n_{id_raw}" if re.match(r"^\d", id_raw) else id_raw

def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Try to get title from frontmatter
        if content.startswith("---"):
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                frontmatter_text = match.group(1)
                for line in frontmatter_text.split('\n'):
                    if line.strip().startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
                        if title:
                            return title
        # Fallback: first # heading
        for line in content.splitlines():
            if line.strip().startswith("# "):
                return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"

def get_folder_sidebar_position(folder_path):
    intro_md_path = os.path.join(folder_path, "_intro.md")
    if os.path.isfile(intro_md_path):
        fm = parse_frontmatter(intro_md_path)
        try:
            pos = float(fm.get('sidebar_position', float('inf')))
        except:
            pos = float('inf')
        return pos
    return float('inf')

def extract_title_from_folder(folder_path):
    """Extract title from a folder's index.md or _intro.md file."""
    # Check for index.md first, then _intro.md
    index_md_path = os.path.join(folder_path, "index.md")
    intro_md_path = os.path.join(folder_path, "_intro.md")
    
    if os.path.isfile(index_md_path):
        return extract_title(index_md_path)
    elif os.path.isfile(intro_md_path):
        return extract_title(intro_md_path)
    else:
        # Fallback to folder name processing
        return strip_order_prefix(os.path.basename(folder_path)).replace("-", " ").title() or "Home"

def build_mermaid(folder_path, rel_path, depth, parent_id=None, max_depth_override=None, style_config=None):
    if style_config is None:
        style_config = load_style_config()
    
    lines = []
    clicks = []
    classes = {}
    style_classes = {}
    current_id = normalize_id(rel_path or "root")
    
    # Extract proper title from folder's index.md or _intro.md
    label = extract_title_from_folder(folder_path)
    
    # Apply styling to folder nodes by checking index.md or _intro.md
    folder_styles = {'left_icons': [], 'right_icons': [], 'border_colors': [], 'background_colors': [], 'text_colors': [], 'border_styles': [], 'border_widths': [], 'clickable': True, 'exclude': False}
    
    # Check for index.md first, then _intro.md
    index_md_path = os.path.join(folder_path, "index.md")
    intro_md_path = os.path.join(folder_path, "_intro.md")
    
    folder_frontmatter = {}
    if os.path.isfile(index_md_path):
        folder_frontmatter = parse_frontmatter(index_md_path)
        tags = extract_tags_from_frontmatter(folder_frontmatter)
        folder_styles = apply_styling_to_node(tags, style_config, folder_frontmatter)
    elif os.path.isfile(intro_md_path):
        folder_frontmatter = parse_frontmatter(intro_md_path)
        tags = extract_tags_from_frontmatter(folder_frontmatter)
        folder_styles = apply_styling_to_node(tags, style_config, folder_frontmatter)
    
    # Skip folder if it's excluded
    if folder_styles['exclude']:
        return lines, clicks, classes, style_classes
    
    # Create node label with styling
    node_label = create_node_label(label, folder_styles, is_external=False, external_url=None)
    lines.append(f'{current_id}["{node_label}"]')
    
    if rel_path:
        clean_rel_path = "/".join(strip_order_prefix(p) for p in rel_path.split(os.sep))
        docs_url = get_docs_url(clean_rel_path)
        clicks.append(f'click {current_id} "{docs_url}"')
    if parent_id:
        lines.append(f"{parent_id} --> {current_id}")
    
    # Apply styling to the folder node
    color_for_depth = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"][depth % 5]
    mermaid_style = create_mermaid_node_style(folder_styles, default_fill=color_for_depth)
    if mermaid_style:
        style_classes[current_id] = mermaid_style
    
    effective_max_depth = max_depth_override if max_depth_override is not None else get_max_depth()
    if depth >= effective_max_depth:
        classes[current_id] = depth
        return lines, clicks, classes, style_classes
    entries = sorted(os.listdir(folder_path))
    # Exclude 99-contribute folder
    entries = [e for e in entries if e != '99-contribute']
    # Prepare combined list of (name, is_dir, sidebar_position)
    combined = []
    for e in entries:
        full_path = os.path.join(folder_path, e)
        if os.path.isdir(full_path):
            pos = get_folder_sidebar_position(full_path)
            combined.append((e, True, pos))
        elif e.endswith('.md') and e not in ("index.md", "_intro.md") and not e.startswith("."):
            fm = parse_frontmatter(full_path)
            try:
                pos = float(fm.get('sidebar_position', float('inf')))
            except:
                pos = float('inf')
            combined.append((e, False, pos))
    # Sort by sidebar_position, then name
    combined.sort(key=lambda x: (x[2], x[0]))
    palette = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"]
    for name, is_dir, _ in combined:
        if is_dir:
            full_path = os.path.join(folder_path, name)
            entry_rel_path = os.path.join(rel_path, name) if rel_path else name
            sub_lines, sub_clicks, sub_classes, sub_style_classes = build_mermaid(full_path, entry_rel_path, depth + 1, current_id, max_depth_override, style_config)
            lines.extend(sub_lines)
            clicks.extend(sub_clicks)
            classes.update(sub_classes)
            style_classes.update(sub_style_classes)
        else:
            full_path = os.path.join(folder_path, name)
            entry_rel_path = os.path.join(rel_path, name) if rel_path else name
            title = extract_title(full_path)
            node_id = normalize_id(entry_rel_path)
            is_external, external_url = is_external_doc(full_path)
            frontmatter = parse_frontmatter(full_path)
            tags = extract_tags_from_frontmatter(frontmatter)
            styles = apply_styling_to_node(tags, style_config, frontmatter)
            if styles['exclude']:
                continue
            status = frontmatter.get('status', '')
            if status == 'review-needed' or status != 'review-needed':
                node_label = create_node_label(title, styles, is_external, external_url)
                lines.append(f'{node_id}["{node_label}"]')
                if styles['clickable'] and not is_external:
                    clean_entry_path = get_docs_url("/".join(strip_order_prefix(p) for p in entry_rel_path.replace(".md", "").split(os.sep)))
                    clicks.append(f'click {node_id} "{clean_entry_path}"')
                lines.append(f"{current_id} --> {node_id}")
                color_for_depth = palette[(depth + 1) % len(palette)]
                mermaid_style = create_mermaid_node_style(styles, default_fill=color_for_depth)
                if mermaid_style:
                    style_classes[node_id] = mermaid_style
                classes[node_id] = depth + 1
    classes[current_id] = depth
    return lines, clicks, classes, style_classes

def split_frontmatter_and_body(md_content):
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = '---' + parts[1] + '---'
            body = parts[2].lstrip('\n')
            return frontmatter, body
    return '', md_content

def generate_index_md(folder_path, rel_path):
    folder_name = os.path.basename(folder_path)
    human_title = strip_order_prefix(folder_name).replace("-", " ").title() or "Home"
    frontmatter = f"---\ntitle: {human_title}\nhide_title: true\n---"
    intro_md_path = os.path.join(folder_path, "_intro.md")
    intro_frontmatter = ''
    intro_body = ''
    if os.path.isfile(intro_md_path):
        with open(intro_md_path, "r", encoding="utf-8") as f:
            intro_content = f.read().strip()
        intro_frontmatter, intro_body = split_frontmatter_and_body(intro_content)
    custom_intro = [
        f"### {human_title}",
        '<p class="margin-top-negative"><em>Click any block below to navigate directly to that section.</em></p>',
        ""
    ]
    style_config = load_style_config()
    lines, clicks, classes, style_classes = build_mermaid(folder_path, rel_path, depth=0, style_config=style_config)
    class_lines = []
    for d in range(get_max_depth() + 1):
        color = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"][d % 5]
        class_lines.append(f"classDef col{d} fill:{color},stroke:none;")
    for node_id, col in classes.items():
        if node_id not in style_classes:
            class_lines.append(f"class {node_id} col{col};")
    style_counter = 0
    for node_id, style in style_classes.items():
        style_class_name = f"custom{style_counter}"
        class_lines.append(f"classDef {style_class_name} {style};")
        class_lines.append(f"class {node_id} {style_class_name};")
        style_counter += 1
    output = []
    if os.path.isfile(intro_md_path):
        output.append(intro_frontmatter)
        output.append(intro_body)
        output.append("## What's in this chapter?")
        output += custom_intro
    else:
        output.append(frontmatter)
        output.append(DO_NOT_EDIT)
        output += custom_intro
    output += [
        "```mermaid",
        "graph LR",
    ] + lines + clicks + class_lines + [
        "linkStyle default interpolate basis",
        "```"
    ]
    legend_items = create_compact_legend(style_classes, style_config)
    if legend_items:
        output.extend(legend_items)
    index_md_path = os.path.join(folder_path, "index.md")
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"✔️  Wrote: {index_md_path}")

def generate_root_index_md():
    # Custom frontmatter for the root index.md
    frontmatter = (
        '---\n'
        'sidebar_position: 1\n'
        'title: Site Overview\n'
        'hide_title: true\n'
        '---'
    )
    custom_intro = [
        '### Welcome',
        '<small>Here\'s an overview of the first layers of this resource. Simply click on the boxes to get directly to your article of choice, or use the sidebar to navigate.</small>',
        ''
    ]
    lines, clicks, classes, style_classes = build_mermaid(ROOT_DIR, '', depth=0)
    class_lines = []
    for d in range(get_max_depth() + 1):
        color = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"][d % 5]
        class_lines.append(f"classDef col{d} fill:{color},stroke:none;")
    for node_id, col in classes.items():
        if node_id not in style_classes:
            class_lines.append(f"class {node_id} col{col};")
    style_counter = 0
    for node_id, style in style_classes.items():
        style_class_name = f"custom{style_counter}"
        class_lines.append(f"classDef {style_class_name} {style};")
        class_lines.append(f"class {node_id} {style_class_name};")
        style_counter += 1
    output = [
        frontmatter,
        DO_NOT_EDIT,
        ''
    ]
    output += custom_intro + [
        '```mermaid',
        'graph LR',
    ] + lines + clicks + class_lines + [
        'linkStyle default interpolate basis',
        '```'
    ]
    style_config = load_style_config()
    legend_items = create_compact_legend(style_classes, style_config)
    if legend_items:
        output.extend(legend_items)
    index_md_path = os.path.join(ROOT_DIR, "index.md")
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"✔️  Wrote root flatmap: {index_md_path}")

def generate_full_sitemap():
    # Custom frontmatter for the full sitemap
    frontmatter = (
        '---\n'
        'title: Full Site Map\n'
        'sidebar_label: Full Site Map\n'
        'sidebar_position: 2\n'
        'hide_title: true\n'
        '---'
    )
    custom_intro = [
        '### Full Site Map',
        '<small>Complete overview of all content in this resource. This map shows everything at maximum depth - it\'s quite detailed!</small>',
        ''
    ]
    # Use a much deeper depth for the full sitemap
    lines, clicks, classes, style_classes = build_mermaid(ROOT_DIR, '', depth=0, max_depth_override=10)
    class_lines = []
    for d in range(11):  # Support up to depth 10
        color = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0", "#ffe6cc", "#e6f3ff", "#f0e6ff", "#ffe6e6", "#e6ffe6", "#fff2e6"][d % 11]
        class_lines.append(f"classDef col{d} fill:{color},stroke:none;")
    for node_id, col in classes.items():
        if node_id not in style_classes:
            class_lines.append(f"class {node_id} col{col};")
    style_counter = 0
    for node_id, style in style_classes.items():
        style_class_name = f"custom{style_counter}"
        class_lines.append(f"classDef {style_class_name} {style};")
        class_lines.append(f"class {node_id} {style_class_name};")
        style_counter += 1
    output = [
        frontmatter,
        DO_NOT_EDIT,
        ''
    ]
    output += custom_intro + [
        '```mermaid',
        'graph LR',
    ] + lines + clicks + class_lines + [
        'linkStyle default interpolate basis',
        '```'
    ]
    style_config = load_style_config()
    legend_items = create_compact_legend(style_classes, style_config)
    if legend_items:
        output.extend(legend_items)
    sitemap_path = os.path.join(ROOT_DIR, "full-sitemap.md")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"✔️  Wrote full sitemap: {sitemap_path}")

def is_external_doc(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'^type:\s*external\s*$', content, re.MULTILINE)
            if not match:
                return False, None
            link_match = re.search(r'^link:\s*(\S+)', content, re.MULTILINE)
            return True, link_match.group(1) if link_match else None
    except:
        return False, None

def color_to_dot(color):
    """Map a color name to a colored dot emoji."""
    color = color.lower()
    color_map = {
        'red': '🔴',
        'orange': '🟠',
        'yellow': '🟡',
        'green': '🟢',
        'blue': '🔵',
        'purple': '🟣',
        'pink': '🩷',
        'black': '⚫',
        'white': '⚪',
        'grey': '⬤',  # Use filled circle for grey
        'gray': '⬤',
        'lightgrey': '⬤',
        'lightgray': '⬤',
        'lightgreen': '🟢',
        'lightcoral': '🔴',
        # fallback for custom colors
    }
    # Try to match CSS hex colors to a dot (very basic)
    if color.startswith('#'):
        # Could do more advanced mapping here
        return '⬤'
    return color_map.get(color, '⬤')

def create_compact_legend(style_classes, style_config):
    """Create a compact legend showing all styles from the config, with color dots for border/background."""
    # Group tags by their visual properties
    icon_tags = []
    border_tags = []
    background_groups = {}
    
    for tag, tag_config in style_config.get('tags', {}).items():
        # Convert list of tuples to dict for easier access
        tag_props = dict(tag_config) if isinstance(tag_config, list) else tag_config
        
        # Skip invisible/excluded tags
        if tag_props.get('exclude', False):
            continue
            
        icon = tag_props.get('icon', '')
        border_color = tag_props.get('border_color', '')
        background_color = tag_props.get('background_color', '')
        background_opacity = tag_props.get('background_opacity', '')
        
        if icon:
            # Handle AND conditions specially
            if ' AND ' in tag:
                icon_tags.append(f"**{icon}** {tag}")
            else:
                icon_tags.append(f"**{icon}** {tag}")
        
        if border_color:
            border_dot = color_to_dot(border_color)
            border_tags.append(f"**border:{border_dot}** {tag}")
        
        if background_color:
            # Add opacity info to the background color key if present
            bg_key = background_color
            if background_opacity:
                bg_key = f"{background_color} (opacity: {background_opacity})"
            
            if bg_key not in background_groups:
                background_groups[bg_key] = []
            background_groups[bg_key].append(tag)
    
    legend_lines = []
    
    # Icons line
    if icon_tags:
        legend_lines.append(" | ".join(icon_tags))
    
    # Border colors line
    if border_tags:
        legend_lines.append(" | ".join(border_tags))
    
    # Background colors line - all on one line with text descriptions
    if background_groups:
        bg_parts = []
        for bg_color, tags in background_groups.items():
            if bg_color == "lightgrey":
                bg_parts.append(f"**bg grey:** {', '.join(tags)}")
            elif bg_color == "lightgreen":
                bg_parts.append(f"**bg green:** {', '.join(tags)}")
            else:
                bg_parts.append(f"**bg {bg_color}:** {', '.join(tags)}")
        legend_lines.append(" | ".join(bg_parts))
    
    if not legend_lines:
        return []
    
    legend_text = "<br />".join(legend_lines)
    return [
        "",
        f"<small><strong>Legend:</strong><br />{legend_text}</small>"
    ]

# Generate the full sitemap
generate_full_sitemap()
