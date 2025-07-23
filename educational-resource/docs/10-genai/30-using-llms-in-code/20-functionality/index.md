---
title: Functionality
sidebar_position: 10
hide_title: true

level: intermediate
status: published
visibility: public

# OPTIONAL TAGS:
# external-link: https://somelink.dev  #if the resource is external
# priority: high        # high / medium (for missing articles)
# review-reason: "something that needs double checking or changing"
#                       # required when status = review-needed
# programming-language: "Java"  # or others
---

# Functionality on Top of LLMs

LLMs basic function is to answer to questions or instructions. We can however, build a lot of interesting functionality around that to give them superpowers.

In this chapter you'll find all the details on:

- **[Chatbots](10-chatbots.md)** - Build conversational interfaces
- **[Memory management](20-memory.md)** - Keep context across conversations
- **[Passing along extra context](40-content-retrieval/)** - Retrieval-Augmented Generation (RAG)
- **[Tool calling or function calling](30-tool-calling/)** - Let LLMs call your code
- **[Output parsing](70-output-parsing.md)** - Retrieve Java or JSON objects from the LLM instead of Strings
- **[Guardrails and moderation](80-guardrails.md)** - Keep your augmented LLM in check
- **[Agentic behavior and orchestration](../../30-agentic-ai/)** - For complex workflows and agent systems

You'll end up with a super powerful LLM that in theory is capable of knowing everything and doing everything. An **augmented LLM**. Handle with care ;)

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/augmented_llm.png" alt="Augmented LLM Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Unless you want to do very fancy and special things, use your favorite framework to make all of the above a breeze :)

---

*Written by Lize Raes*


