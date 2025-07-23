---
title: Local Models
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

# Local Models

## Quick Navigation
- [The Advantages](#-the-advantages)
- [The Disadvantages](#️-the-disadvantages)
- [How to Choose the Right Local Model](#how-to-choose-the-right-local-model)
- [How to Run Local Models](#how-to-run-local-models)

---

You can run LLMs and other AI models locally, on your own computer or specialized hardware in your home or company (on-prem).

You will typically run an **Open Source Model**, where you can download the weights and some runtime to actually run your model.

## 🎯 The Advantages

- **They work offline** - No internet connection required once the model is downloaded
- **Your data stays private** - Any questions or documents you send to the model do not leave your system
- **No SaaS model usage costs** - No API key or per-request charges
- **With the right setup, local models can be very fast** - No network latency, direct GPU access

## ⚠️ The Disadvantages

- **On your laptop you can only run models that are an order of magnitude smaller** than the SaaS models, depending on your hardware
- **Hardware to run big models (50GB+) is expensive** - Requires high-end GPUs and lots of RAM
- **Model switching is inefficient** - The weights need to be loaded in memory each time you use another model (gigabytes)
- **Smaller models mean notably worse quality** - Issues with complex tasks and tool calling, etc.
- **Use up a lot of memory** from your local machine
- **They don't scale well for large-scale deployments** - Concurrency issues when different users try to simultaneously use the model, unless you set up a kubernetes cluster to manage availability and throughput

## How to Choose the Right Local Model

The best model for your use case depends on factors like:

- **Available memory** on the local machine
- **Required speed** for your application
- **Required quality** for your specific tasks
- **Model specialization** (coding, reasoning, etc.)
- **Required context window size**

Models like **Qwen3** are said to perform better for coding and tool calling. A model like **DeepSeek** does reasoning to tackle complex tasks better.

You can check performance in leader boards or benchmarks like [HuggingFace's Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/) (with categories like 'For Edge Devices' and 'For the GPU Rich', ...) and its [Open LLM Comparator](https://huggingface.co/spaces/open-llm-leaderboard/comparator).

## How to Run Local Models

Here are the most popular ways to run local models:

- **[🤗 HuggingFace](10-huggingface.md)** - Easy model hosting and inference. Use the HuggingFace ecosystem to download and run models with their optimized libraries.

- **[🦙 Ollama](20-ollama.md)** - Simple local model management. Pull and run models with a single command, perfect for quick experimentation.

- **[🐳 Docker Model Runner](30-docker-model-runner.md)** - Containerized model inference. Run models in Docker containers with GPU acceleration and OpenAI-compatible APIs.

- **[💻 LM Studio](40-lm-studio.md)** - Desktop GUI for model management. User-friendly interface for downloading, managing, and running local models.

- **[🚀 GPT4All](50-gpt4all.md)** - Lightweight model runner. Optimized for running smaller models efficiently on consumer hardware.

- **[🌐 In-browser](60-in-browser.md)** - Run models directly in your browser. Use WebAssembly and WebGPU to run models without any installation.

---

*Written by Lize Raes*