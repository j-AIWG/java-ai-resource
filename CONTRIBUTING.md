# 🤝 Contributing to Java & AI Resource Hub

Thanks for helping build the most useful, well-structured resource landscape for Java and AI!

We aim to make the resource:

- **Easy to navigate**, even at depth
- **Structured**, tagged, and filterable
- **Low maintenance**, yet dynamically visualized
- **Equally useful for beginners and experts**

---

## 📝 How to Add a Resource

Not sure where to start? Have a look at the last topic in the sidebar, `Contribute` for a dashboard with resources / reviews we'd love to have. If you have your own idea, go ahead as follow:

### Option 1: Add an Existing Resource?

Found a great external resource (documentation, tutorial, tool) that should be included? Here's how to add it:

1. Find the correct folder inside [`/docs/`](./docs)
2. Copy [`docs/.template.md`](./docs/.template.md) into that folder
3. Rename the file (e.g., `framework-docs.md`, `tool-overview.md`, etc.). Attention: `index.md` is reserved for the landing page of folders.
4. Fill in the frontmatter:
   - Set `status: published` (since it's an existing resource)
   - Add `external-link: https://your-resource-url.com` in the optional tags section
5. Write a brief description and add the prominent link like this:
   ```
   **<h2><a href="https://your-resource-url.com" target="_blank" rel="noopener noreferrer">👉 Visit the Official Resource Name ↗</a></h2>**
   
   Brief description of what this resource provides.
   ```
6. Make a PR 🙌

### Option 2: Write New Content?

1. Find the correct folder inside [`/docs/`](./docs)
2. Copy [`docs/.template.md`](./docs/.template.md) into that folder
3. Rename the file (e.g., `overview.md`, `setup-guide.md`, etc.). Attention: `index.md` is reserved for the landing page of folders.
4. Fill in the frontmatter (YAML block at the top) as described in the template
5. Write your content under the frontmatter (after the second `---`)
6. Make a PR 🙌 


---

## 📌 About `index.md` Pages

Each folder can contain an `index.md` file that:

- Serves as the **landing page** for that topic
- Should be **short and to the point** (5 paragraphs max)
- Should **dispatch readers** toward subtopics depending on their persona:
    - **Expected readers**: new to the topic / experienced / educators

---

Thanks again for contributing 🙌  
If you have ideas, improvements, need support, or are just to lazy to find the right spot for the article but still want to share it with us: open a Discussion or contact the maintainers.
