---
title: Using LLMs in Code
sidebar_position: 10
hide_title: true

level: beginner
status: published
visibility: public

# OPTIONAL TAGS:
# external-link: https://somelink.dev  #if the resource is external
# priority: high        # high / medium (for missing articles)
# review-reason: "something that needs double checking or changing"
#                       # required when status = review-needed
# programming-language: "Java"  # or others
---

# Using LLMs in Code

## Quick Navigation
- [Chatting with Models](#chatting-with-models)
- [Frameworks to the Rescue](#frameworks-to-the-rescue)
- [Beyond Chat: Augmented LLMs](#beyond-chat-augmented-llms)
- [From Augmented LLMs to Agents](#from-augmented-llms-to-agents)

---

Many people know how to use Large Language Models via applications like ChatGPT. But is also possible to talk directly to the underlying model (e.g., GPT-4) via API through code.

This opens up very interesting use cases, from building a chatbot to your own flavor, up to creating agents that can manage your payments, orchestrate complex workflows, and control the lights in your house.

## Chatting with Models

In its simplest form, your code sends a request with a text message to the LLM in a syntax that's compatible with what it expects. For OpenAI models (the ones behind ChatGPT), it looks something like this:

```
// Basic OpenAI API call
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer your_openai_key
Content-Type: application/json

{
    "model": "gpt-4",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

// Expected output: (this should be the Hi X, how can I assist you today)
```

## Frameworks to the Rescue

This raw API approach is quite verbose. Thankfully, there are frameworks available to make this much easier. For example, [LangChain4j](/docs/genai/using-llms-in-code/frameworks/langchain4j/) and [SpringAI](/docs/genai/using-llms-in-code/frameworks/springai/) make it as simple as:

```java
// LangChain4j example
ChatLanguageModel model = OpenAiChatModel.builder()
    .apiKey("your_openai_key")
    .modelName("gpt-4")
    .build();

String response = model.generate("Hello, how are you?");
// Expected output: Hi! I'm doing well, thank you for asking...

// SpringAI example
@Autowired
private ChatClient chatClient;

String response = chatClient.call("Hello, how are you?");
// Expected output: Hi! I'm doing well, thank you for asking...
```

## Beyond Chat: Augmented LLMs

Once we have code access to a model, we can do much more than just chatting. We can turn it into a so-called 'augmented LLM' that can:

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/augmented_llm.png" alt="Augmented LLM Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

- **Set instructions** to make the model behave a certain way
- **Keep conversation memory** (or manipulate memory using few-shot approaches - see [Memory](/docs/genai/using-llms-in-code/functionality/memory/))
- **Retrieve information** from extra resources like your business documents or a weather forecast API (not just what the model was trained on)
- **Call your code** by telling it what methods are available (= [tool calling](/docs/genai/using-llms-in-code/functionality/tool-calling/), also called function calling). Once the LLM can call your code, your code can call anything: robots, home equipment, you name it.

## From Augmented LLMs to Agents

Augmented LLMs that can 'act' this way start to behave like agents, specialized to solve specific tasks. You can combine agents to orchestrate bigger processes or plug them into deterministic workflows. More about that in the chapter on [Agentic AI](/docs/agentic-ai/).

---

**Ready to dive in?** Start with the [basics](/docs/genai/using-llms-in-code/basics/), check in more detail how things like [memory](/docs/genai/using-llms-in-code/functionality/memory/), [RAG](/docs/genai/using-llms-in-code/functionality/content-retrieval/) and [tool calling](/docs/genai/using-llms-in-code/functionality/tool-calling/) work in [functionality](/docs/genai/using-llms-in-code/functionality/) or jump straight to your preferred [framework](/docs/genai/using-llms-in-code/frameworks/).
