---
title: "Help us write: {title}"
id: {id}
sidebar_label: "Contribute: {title}"
hide_title: true
---

## Help us write: {title}

> 📄 This page was generated to help you contribute this resource. If you're interested, follow the instructions below and submit your PR!

### 🧩 Context

Find this article here: {article_link}

#### Sibling articles in the same section, so you know what's already been written:
{sibling_articles}

---

### ✍️ How to contribute this article

#### If you have an existing external link
Just fork the repo, or <a href="{file_edit_link}" target="_blank" rel="noopener noreferrer">{filename}</a> directly on GitHub, and submit a PR with your external link (see example below).

#### 🔁 Example: external resource
```yaml
---
title: Building Your First ADK Agent (Dev.to)
type: external
level: beginner
topics: [tutorial, agents]
status: published
visibility: public
author: Your Name (@githubhandle)
link: https://your-article-link.com
---

:::tip External Resource
👉 <a href="https://your-article-link.com" target="_blank" rel="noopener noreferrer">Read the full article</a>
:::
```

#### If you still need to create the content
First, claim the article:
1. **Fork** this repo on GitHub.
2. In your fork, navigate to:
   ```bash
   cd docusaurus-resource/docs/{rel_path_folder}
   ```
3. Open `{filename}` and:
   - Add your name and GitHub handle to the `author` field.
   - Set a realistic `eta` field (e.g. `2025-08-01`).
   - Change `status` to `draft`.
4. **Submit a PR** to claim this article (we'll approve ASAP!).
5. Once accepted (or even before), start writing!

#### 🧠 Example: inline resource
```yaml
---
title: Initializing an ADK Agent
type: tutorial
level: beginner
topics: [agents, initialization, setup]
status: published
visibility: public
author:
  - Your Name (@githubhandle)
---

Intro text here...
```

If it was external, see above for how to add it.

---

### ✅ Once you're done
- Mark the article as `review-needed`
- Submit a pull request

Thank you for helping make this resource better! 💚 