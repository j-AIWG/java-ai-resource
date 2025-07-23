---
title: LangChain4j
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
programming-language: "Java"  # or others
---

# LangChain4j

LangChain4j is one of the two popular Java libraries for easy interaction with LLMs.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/langchain4j_logo.png" alt="LangChain4j Logo" style={{width: '30%', display: 'block', margin: 'auto'}} />

<br />

Calling a model is as simple as:

```java
ChatLanguageModel model = OpenAiChatModel.builder()
    .apiKey("your key")
    .modelName("gpt-4o-mini")
    .build();

String answer = model.generate("Hello, how are you?");
System.out.println(answer);
```

And creating an app where the LLM generates Java objects (output parsing), can call tools, has a memory and access to extra context (RAG) would be as simple as:

```java
interface CustomerAssistant {
    @SystemMessage("You are a helpful customer service assistant")
    @UserMessage("You create a stepwise plan for the user that submitted: {{message}}")
    List<String> assist(@MemoryId String customerId, String message);
}

CustomerAssistant assistant = AiServices.builder(CustomerAssistant.class)
    .chatLanguageModel(model)
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .retrievalAugmentor(DefaultRetrievalAugmentor.builder()
        .contentRetriever(serviceTermsEmbeddingStoreRetriever)
        .build())
    .tools(new BookingManagementTools())
    .build();
```

LangChain4j is framework-agnostic: it works standalone (vanilla) and has strong integrations with **Quarkus**, **Spring Boot**, and integrations with **Micronaut** for example.

You can watch an engaging overview of most features in our [LangChain4j overview video](https://www.youtube.com/watch?v=BD1MSLbs9KE).

Read through our [deep dive article](./20-langchain4j-deepdive-with-code.md) to see code examples of these and more advanced features.

Or get your hands dirty and go through our comprehensive, self-explanatory [code tutorial repository](https://github.com/langchain4j/langchain4j-examples/tree/main/tutorials), which includes special folders for [Spring Boot examples](https://github.com/langchain4j/langchain4j-examples/tree/main/spring-boot-example) and [RAG examples](https://github.com/langchain4j/langchain4j-examples/tree/main/rag-examples).

For supported model providers, check out our [model integrations documentation](https://docs.langchain4j.dev/integrations/language-models/), which covers all popular commercial providers like OpenAI's GPT models, Google's Gemini, Anthropic's Claude, etc., as well as local models via Ollama, JLama, and others.

For embedding store integrations, see our [embedding store documentation](https://docs.langchain4j.dev/integrations/embedding-stores/).

You'll find ample examples of how to use each of these features in our [main examples repository](https://github.com/langchain4j/langchain4j-examples).

---

*Written by Lize Raes*
