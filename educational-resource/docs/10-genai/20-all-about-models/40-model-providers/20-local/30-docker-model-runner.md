---
title: Docker Model Runner
sidebar_position: 30
hide_title: true

level: beginner
status: published
visibility: public

# OPTIONAL TAGS:
# external-link: https://somelink.dev  #if the resource is external
# priority: high        # high / medium (for missing articles)
# review-reason: "something that needs double checking or changing"
#                       # required when status = review-needed
programming-language: "Java"  # or others
---

# Docker Model Runner

You love Java? You're already using Docker? And you're exploring AI? Then this one is for you!

Docker launched Docker Model Runner (DMR) in early 2025: it's a model runtime engine that ships with Docker Desktop and model weights that you can pull straight from Docker Hub, just like common images. Think DeepSeek, Gemma3, Phi4, …

DMR makes running language models locally super easy, including GPU-acceleration (for faster inference), OpenAI-compatible APIs, and fully wired into your existing developer setup. You can use it in Java with LangChain4j or SpringAI.

## Why is this cool

Docker just turned running LLMs into something as easy as `docker model run`. You don't need to understand model architecture or inference backends, you just:

```bash
docker model pull ai/gemma3
docker model run ai/gemma3
```

That's it. It's the kind of developer experience we've been missing in the AI tooling world. Fast, familiar, and frictionless. Especially for teams who already use Docker in their stack. They're curating and hosting popular models like **Gemma**, **LLaMA**, and **DeepSeek** directly on [Docker Hub](http://hub.docker.com/u/ai), so you don't have to source weights or worry about sketchy downloads.

It's fast. It's GPU-accelerated. And it plugs directly into your Java app.

## Try it in 5 minutes

**Note:** At the moment only available on Mac (Windows will within a month or so).

First, let's get your Docker Desktop ready for the Model Runner. Make sure to be on a recent Docker version (4.40+ required). In settings, scroll down to Features in Development, and check:

<img src="/java-ai-resource/img/10-genai/20-all-about-models/enable_dmr.webp" alt="Enable Docker Model Runner settings" style={{width: '70%', display: 'block', margin: 'auto'}} />

The first check enables the Model Runner in CLI, the second one makes 
sure we can access it with LangChain4j. Click Apply and Restart.

List the available commands and check if the installation was successful by opening a terminal:

```bash
docker model command
```

Now let's pull and run our first model:

```bash
docker model pull ai/gemma3:latest
docker model run ai/gemma3
```

To use this model directly from Java, I put together a minimal, no-frameworks chatbot with memory using LangChain4j: 👉 [github.com/LizeRaes/docker-model-runner-langchain4j](https://github.com/LizeRaes/docker-model-runner-langchain4j)

<img src="/java-ai-resource/img/10-genai/20-all-about-models/dmr_chat.webp" alt="Docker Model Runner Chatbot" style={{width: '70%', display: 'block', margin: 'auto'}} />

Follow the instructions in the readme, and there you go, you're now chatting with a local model via Java.

The magic happens in `ChatServer.java`:

```java
ChatLanguageModel model = OpenAiChatModel.builder()
    .apiKey("not needed")
    .baseUrl("http://localhost:12434/engines/llama.cpp/v1")
    .modelName("ai/gemma3")
    .build();
```

## What models are available?

Browse [Docker's AI Hub](https://hub.docker.com/u/ai) to see what's already there. More models are added regularly.

To check file size and resources, just open a model page on Docker Hub — you'll see the size, architecture, and version. For example, for Gemma3

<img src="/java-ai-resource/img/10-genai/20-all-about-models/gemma3_size.webp" alt="Gemma3 Model Size" style={{width: '70%', display: 'block', margin: 'auto'}} />

Once you have the model running you can check your GPU usage via (MacOS):
**Activity Monitor → Window → GPU History**

<img src="/java-ai-resource/img/10-genai/20-all-about-models/dmr_gpu.webp" alt="Docker Model Runner GPU Usage" style={{width: '70%', display: 'block', margin: 'auto'}} />

## What's next?

Docker's R&D team works on a very ambitious AI roadmap. DMR is available for Mac and Windows. They already offer containerized MCP servers and are on their way to make all aspects of AI model inference a breeze. Docker Offload lets you run all that on a cloud GPU in one click, and Agent Compose let's you define models and agents 

Your feedback is super valuable for making everything work smoothly, so if you encounter a glitch or miss an essential feature, let the Docker team know via:

```bash
docker feedback
```

Have fun building with it!

---

*Written by Lize Raes*

