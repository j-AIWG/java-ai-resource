import os
import re

BASE_PATH = os.path.join(os.getcwd(), "docs")

# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------

def clean_title(raw_name):
    """
    Convert e.g. 10_langchain4j.md → Langchain4j
    Convert folder names like 20_tool-calling → Tool Calling
    """
    name = re.sub(r"^\d+_", "", raw_name)
    name = name.replace(".md", "")
    name = name.replace("-", " ")
    name = name.replace("_", " ")
    return name.strip().title()

def guess_topics(path):
    path_lower = path.lower()
    topics = []
    if "genai" in path_lower:
        topics.append("domain:genai")
    if "ml" in path_lower:
        topics.append("domain:ml")
    if "agentic" in path_lower:
        topics.append("domain:agentic-ai")
    if "coding" in path_lower:
        topics.append("domain:ai-assisted-coding")
    if "finance" in path_lower:
        topics.append("domain:finance")
    if "healthcare" in path_lower:
        topics.append("domain:healthcare")
    if "accessibility" in path_lower:
        topics.append("domain:accessibility")
    if "research" in path_lower:
        topics.append("domain:scientific-research")
    if "education" in path_lower:
        topics.append("domain:education")
    if "ecommerce" in path_lower:
        topics.append("domain:ecommerce")
    if "learning-paths" in path_lower:
        topics.append("domain:learning-paths")
    return topics if topics else ["domain:general"]

def generate_frontmatter(title, sidebar_position, topics, linked_resource=None, is_intro=False):
    """
    Build the exact YAML frontmatter block with comments
    """

    topics_yaml = "\n".join(f"  - {t}" for t in topics)

    # Core frontmatter fields
    lines = [
        "---",
        f"title: {title}",
        f"sidebar_position: {sidebar_position}",
        "hide_title: true",
        ""
    ]

    if linked_resource:
        lines.append(f"linked_resource: {linked_resource}")
        lines.append("")

    # Comments block (EXACTLY as user provided)
    lines += [
        "# REQUIRED TAGS — fill in all of these:",
        "",
        "level: beginner        # beginner / intermediate / advanced / expert",
        "type: overview         # tutorial / overview / code / benchmark / opinion / api-doc",
        "status: placeholder          # draft / review-needed / published / missing",
        "visibility: public     # public",
        "",
        "topics:",
        f"{topics_yaml}",
        "  # Add one or more topical tags.",
        "  # Where appropriate, use prefixes for easy filtering like provider:, framework:, tool:, runtime: whenever possible.",
        "",
        "# 🧩 OPTIONAL TAGS:",
        "",
        "# article-priority: high   # high / medium — omit if not important",
        "",
        "# collaboration: open      # set if author welcomes collaborators",
        '# collaboration-topic: "need help implementing Spring Boot starter examples"',
        "#                        # explain what help is welcome (appears on the dashboard & collab page)",
        "",
        '# review-reason: "seems not to be on the right topic"',
        "#                        # required when status: review-needed — will show on the article and in the dashboard",
        "",
        '# author: ["Lize Lala (@lizela)", "Data Science Central (@datasciencecentral)"]',
        "",
        "# eta: 2025-07-01           # Set only if status is draft",
        "",
        "# Feature-related tags (only if this doc describes a feature or gap in Java+AI):",
        "# feature-status: preview        # missing / experimental / preview / stable / specified",
        "# feature-priority: high         # suggested / medium / high",
        "# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>",
        "---"
    ]

    # Body text
    if is_intro:
        lines.append("")
        lines.append("Help us write this landing page")
    else:
        lines.append("")
        lines.append("Help us write this resource")

    return "\n".join(lines)

def linked_resource_path(filename):
    """
    Convert:
        10_link_10_genai_40_llm-architectures.md
    Into:
        ../10-genai/40-llm-architectures.md
    """
    parts = filename.split("_link_")[1].replace(".md", "").split("_")

    file_name = parts[-1] + ".md"
    folders = parts[:-1]

    # e.g. ["10", "genai"] → "10-genai"
    if folders:
        folders_path = "-".join(folders)
        return f"../{folders_path}/{file_name}"
    else:
        return f"../{file_name}"

# -------------------------------------------------------
# YOUR NEW FILE STRUCTURE
# -------------------------------------------------------

ALL_PATHS = [
    # new genai structure
    "10_genai/10_genai-basics.md",
    "10_genai/20_all-about-models/10_llm-architecture.md",
    "10_genai/20_all-about-models/20_model-parameters.md",
    "10_genai/20_all-about-models/30_which-model-to-choose.md",
    "10_genai/20_all-about-models/40_model-providers/10_commercial/10_openai.md",
    "10_genai/20_all-about-models/40_model-providers/10_commercial/20_gemini.md",
    "10_genai/20_all-about-models/40_model-providers/20_local/10_huggingface.md",
    "10_genai/20_all-about-models/40_model-providers/20_local/20_ollama.md",
    "10_genai/30_using-llms-in-code/10_basics.md",
    "10_genai/30_using-llms-in-code/20_functionality/10_chatbots.md",
    "10_genai/30_using-llms-in-code/20_functionality/20_memory.md",
    "10_genai/30_using-llms-in-code/20_functionality/30_tool-calling/10_overview.md",
    "10_genai/30_using-llms-in-code/20_functionality/30_tool-calling/20_function-calling.md",
    "10_genai/30_using-llms-in-code/20_functionality/30_tool-calling/30_mcp.md",
    "10_genai/30_using-llms-in-code/20_functionality/40_content-retrieval/10_semantic-search.md",
    "10_genai/30_using-llms-in-code/20_functionality/40_content-retrieval/20_chunking.md",
    "10_genai/30_using-llms-in-code/20_functionality/40_content-retrieval/30_vector-dbs/10_overview.md",
    "10_genai/30_using-llms-in-code/20_functionality/40_content-retrieval/30_vector-dbs/20_providers.md",
    "10_genai/30_using-llms-in-code/30_frameworks/10_langchain4j.md",
    "10_genai/30_using-llms-in-code/30_frameworks/20_springai.md",
    "10_genai/40_inference/10_local.md",
    "10_genai/40_inference/20_cloud.md",

    # ml
    "20_ml/10_fundamentals.md",
    "20_ml/20_architectures/10_classification.md",
    "20_ml/20_architectures/20_neural-networks.md",
    "20_ml/20_architectures/30_image-recognition.md",
    "20_ml/30_training/10_basics.md",
    "20_ml/30_training/20_data-prep.md",
    "20_ml/30_training/30_finetuning.md",
    "20_ml/30_training/40_evaluation.md",
    "20_ml/40_frameworks.md",
    "20_ml/50_gpu.md",

    # agentic-ai
    "30_agentic-ai/10_patterns.md",
    "30_agentic-ai/20_frameworks/10_adk.md",
    "30_agentic-ai/20_frameworks/20_langgraph4j.md",
    "30_agentic-ai/30_applications.md",

    # ai-assisted-coding
    "40_ai-assisted-coding/10_coding-tools.md",
    "40_ai-assisted-coding/20_productivity.md",

    # domain-use-cases
    "50_domain-use-cases/10_finance.md",
    "50_domain-use-cases/20_healthcare.md",
    "50_domain-use-cases/30_accessibility.md",
    "50_domain-use-cases/40_scientific-research.md",
    "50_domain-use-cases/50_education.md",
    "50_domain-use-cases/60_ecommerce.md",
]

# Add learning-paths
ALL_PATHS += [
    # learning-paths
    "60_learning-paths/10_new-to-java-for-ai/10_welcome.md",
    "60_learning-paths/10_new-to-java-for-ai/20_link_40_ai-assisted-coding_10_coding-tools.md",
    "60_learning-paths/10_new-to-java-for-ai/30_link_10_genai_30_using-llms-in-code_30_frameworks_10_langchain4j.md",
    "60_learning-paths/10_new-to-java-for-ai/40_your-first-bot.md",
    "60_learning-paths/10_new-to-java-for-ai/50_add-memory.md",
    "60_learning-paths/10_new-to-java-for-ai/60_link_10_genai_30_using-llms-in-code_20_functionality_30_tool-calling_10_overview.md",
    "60_learning-paths/10_new-to-java-for-ai/70_deploy.md",
    "60_learning-paths/10_new-to-java-for-ai/80_optional-java-tricks.md",
    "60_learning-paths/10_new-to-java-for-ai/90_now-what.md",
]

# -------------------------------------------------------
# GENERATE FILES
# -------------------------------------------------------

folders = {}

for path in ALL_PATHS:
    folder = os.path.dirname(path)
    file = os.path.basename(path)
    folders.setdefault(folder, []).append(file)

for folder, files in folders.items():
    files.sort()

    folder_path = os.path.join(BASE_PATH, folder)
    os.makedirs(folder_path, exist_ok=True)

    # Create index.md
    if folder:
        prefix = int(folder.split("_")[0])
        intro_title = clean_title(folder.split("/")[-1])
        topics = guess_topics(folder)
        intro_content = generate_frontmatter(
            title=intro_title,
            sidebar_position=prefix,
            topics=topics,
            is_intro=True
        )
        intro_path = os.path.join(folder_path, "index.md")
        with open(intro_path, "w", encoding="utf-8") as f:
            f.write(intro_content)
        print(f"✔ Created {intro_path}")

    # Create files in this folder
    for filename in files:
        prefix = int(filename.split("_")[0])
        full_path = os.path.join(folder_path, filename)

        if "_link_" in filename:
            link_path = linked_resource_path(filename)
            title = clean_title(filename)
            topics = guess_topics(link_path)
            content = generate_frontmatter(
                title=title,
                sidebar_position=prefix,
                topics=topics,
                linked_resource=link_path,
                is_intro=False
            )
        else:
            title = clean_title(filename)
            topics = guess_topics(os.path.join(folder, filename))
            content = generate_frontmatter(
                title=title,
                sidebar_position=prefix,
                topics=topics,
                is_intro=False
            )

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✔ Created {full_path}")
