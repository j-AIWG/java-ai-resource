---
title: Langchain4j Deep Dive with Code
sidebar_position: 10
hide_title: true

level: intermediate
status: published
visibility: public

# OPTIONAL TAGS:
# external-link: https://docs.langchain4j.dev/  #if the resource is external
# priority: high        # high / medium (for missing articles)
# review-reason: "something that needs double checking or changing"
#                       # required when status = review-needed
programming-language: "Java"  # or others
---

# Langchain4j Deep Dive with Code

*as [published in JAVAPRO](https://javapro.io/2025/04/23/build-ai-apps-and-agents-in-java-hands-on-with-langchain4j/) - 30 Years of Java Edition*

## Table of Contents

- [Intro to LangChain4j](#intro-to-langchain4j)
- [Architecture of AI-Powered Apps](#architecture-of-ai-powered-apps)
  - [Basic Blocks](#basic-blocks)
  - [Multimodality](#multimodality)
  - [Architecture of Augmented LLMs](#architecture-of-augmented-llms)
- [Hello world, how can I assist you today?](#hello-world-how-can-i-assist-you-today)
- [Using Models](#using-models)
  - [Language Models and their parameters](#language-models-and-their-parameters)
  - [Image Models](#image-models)
  - [Audio models](#audio-models)
- [Message Roles](#message-roles)
- [AI Services](#ai-services)
  - [Input parameters and structured outputs](#input-parameters-and-structured-outputs)
- [Memory](#memory)
  - [Few Shot Examples](#few-shot-examples)
- [Tools](#tools)
  - [Human as a tool](#human-as-a-tool)
  - [MCP servers](#mcp-servers)
- [RAG](#rag)
- [Agentic Systems](#agentic-systems)
  - [Basic Agent: LLM calls code](#basic-agent-llm-calls-code)
  - [State Machine: Code calls LLM calls code](#state-machine-code-calls-llm-calls-code)
  - [Combinations](#combinations)
- [Production Features](#production-features)
- [Important links](#important-links)
- [Thank you and FAQ](#thank-you-and-faq)


LangChain4j is a java library to make **interactions with AI models and LLMs in Java** easy, with unified APIs that wrap different models. It also provides tools to let you build more **complex use cases on top of basic functionality**. At this 2nd anniversary of LangChain4j, we are thrilled to give you a walkthrough of the functionality that enables you to build basic and advanced AI-powered apps in Java.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/langchain4j_logo.png" alt="LangChain4j Logo" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

The goal of this article is to show you the most important features of LangChain4j, starting from the basics, building up to more advanced and cooler examples. Are you curious how to use LLMs in Java but never tried it yourself? Read on, this article is for you! Did you already build some apps but you're curious to learn more advanced features and use cases? Skip the first chapters and jump right to the topic of your fancy.

Intro to LangChain4j
--------------------

LangChain4j is all about interacting with AI models. Using a model is called **inference**. We can stay in our DevOps space and interact with the model via API, without caring too much about all the details in the layer below. What LangChain4j it NOT about:

*   needing to understand how AI Models work under the hood: we can leave that to the data scientists.
*   training or fine tuning models: if you want to do that, have a look at Tribuo for classic machine learning strategies like regression, or at DeepLearning4j for deep learning and neural networks.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/devops_mlops.png" alt="DevOPS vs MLOPS" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

The main building blocks of LangChain4j are **LLMs**, but also **image models**, **audio models** and so called **multi-modal models** that do more than one of the aforementioned things at the same time (dealing with multiple kinds of input and output).

You can use vanilla LangChain4j, but we also have a smooth integration with **Quarkus** (see [github.com/quarkiverse/quarkus-langchain4j](https://github.com/quarkiverse/quarkus-langchain4j)) and **Spring Boot** (see spring-boot-example in [github.com/langchain4j/langchain4j-examples](http://github.com/langchain4j/langchain4j-examples)). Links to the relevant repositories can be found at the end of this article.

Architecture of AI-Powered Apps
-------------------------------

Here we give a high-level overview of the components of LangChain4j. Later in the article we will dive in the details and the code for each of them.

### Basic Blocks

**AI Models and Large Language Models (LLM):** LangChain4j was initially built for LLMs as basic blocks.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/basic_llm.png" alt="DevOPS vs MLOPS" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

The LLM itself is basically a huge calculation scheme that will take words in and produce an answer that (often sounds like it) makes sense. It’s not important to understand how LLMs work under the hood to use LangChain4j. It is good to know that models vary in quality and capabilities, closely correlated with the model size.

**Other model types:** LangChain4j supports specific image and audio models, as well as multimodal models that combine multiple input and/or output types. It is also possible to plug in and invoke any type of AI model, for example from HuggingFace (kind of Github for open source models).

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/multimodality.png" alt="Multimodality in AI Models" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />


### Architecture of Augmented LLMs

An LLM can work with a number of surrounding blocks to extend its functionality, making it very easy to turn them into very versatile and slightly risky agents. LLMs can be enhanced with general **behavioral instructions, memory, extra context from content retrievers** and the possibility to **call tools** to help it execute certain tasks. In the schema you see these components, along with their high level LangChain4j interface.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/augmented_llm.png" alt="Augmented LLM Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Hello world, how can I assist you today?
----------------------------------------

Now let’s build something! To make a call to a model you will need to obtain an **API key** for the service you want to use. In this example we will be using OpenAI, you can obtain a key there really easily. I recommend **storing the key in the environment variables** to avoid accidentally pushing it to Github. You can also temporarily use LangChain4j’s demo key, which we provide for free for demonstration purposes (does not support advanced functionality!)

We always import the **langchain4j** (core) functionality:

```
<groupId>dev.langchain4j</groupId>
<artifactId>langchain4j</artifactId>
<version>1.0.0-beta1</version>
```


You also need to import a model provider. For the code examples we are using `<artifactId>**langchain4j-open-ai**</artifactId>`, but you can easily use other model providers, for example [**langchain4j-anthropic**](https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-anthropic) etc. Now we’re ready to code

```
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
...
String apiKey = System.getenv("OPENAI_API_KEY");
// or String apiKey = "demo";

ChatLanguageModel model = OpenAiChatModel.builder()
   .apiKey(apiKey)
   .modelName("gpt-4o-mini")
   .build();

String answer = model.chat("Say 'Hello World'");
System.out.println(answer);
```


This will sometimes return “Hello World”, and sometimes something else. Welcome to nondeterministic programming!

**Using Models**
----------------

### Language Models and their parameters

Above we’ve seen the most basic invocation of OpenAI’s (the **provider**) GPT4-0 mini (the **model**). We support many more **commercial providers** (where you need a key), such as Gemini, Azure OpenAI, Anthropic, Mistral, Amazon Bedrock, etc. 

We also support running **local models**, via **Ollama** (this downloads OSS models for you and serves them on localhost) and **JLama** (inference directly in Java, leveraging VectorAPI). Some reasons to use local models include privacy, cost, and also just using llama2-uncensored 👼  
An overview of **all supported model integrations**: [docs.langchain4j.dev/integrations/language-models/](https://docs.langchain4j.dev/integrations/language-models/)

Each model comes with its own set of **parameters** that you can set to tweak its behavior. What parameters are available and what they do can be found on the model provider’s website. This is how you set some of them for the OpenAI example:

```
ChatLanguageModel model = OpenAiChatModel.builder()
       .apiKey(ApiKeys.OPENAI_API_KEY)
       .modelName(GPT_4_O_MINI)
       .temperature(0.3)
       .timeout(ofSeconds(60))
       .logRequests(true)
       .logResponses(true)
       .build();
```


As you can see it allows us to set a **timeout** and define if requests and responses will be logged (try this in combination with **log level** `debug` to see the real calls to OpenAI). Higher values for **temperature** make the model more creative, lower values result in a more deterministic result.

The former example (`model.generate(String)`) returns a **synchronous** answer which includes waiting and then receiving lots of text at the same time. Models can also answer in **streaming mode** and return token by token, which allows for a much nicer user experience in chat applications. **Tokens** are chunks of text that are typically a couple of characters long. They are the model’s minimal meaningful unit, but we don’t really need to care, except that model prices are typically expressed per token.

```
StreamingChatLanguageModel model = OpenAiStreamingChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName(GPT_4_O_MINI)
        .build();

String userMessage = "Write a poem about NullPointers";

model.chat(userMessage, new StreamingChatResponseHandler() {

    @Override
    public void onPartialResponse(String partialResponse) {
        System.out.print(partialResponse);
    }

    @Override
    public void onCompleteResponse(ChatResponse completeResponse) {
        System.out.println("\n\nDone streaming");
    }

    @Override
    public void onError(Throwable error) {
        error.printStackTrace();
    }
});
```


### **Image Models**

Image models generate images based on a text prompt. LangChain4j has integrations with **Dall-E, Imagen** and some more image models that you can find under [docs.langchain4j.dev/category/image-models](https://docs.langchain4j.dev/category/image-models) .

```
ImageModel model = OpenAiImageModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName(DALL_E_3)
                .build();
Response<Image> response = model.generate("java duke with loom, virtual threads and cat ");
System.out.println(response.content().url());
```


If you prefer storing the image directly, you can set the following parameters on the ImageModel:

```
ImageModel model = OpenAiImageModel.builder()
       .apiKey(System.getenv("OPENAI_API_KEY"))
       .modelName(DALL_E_3)
       .quality(DALL_E_QUALITY_HD)
       .persistTo(Paths.get("src/main/resources/result-images"))
       .build();
```


The result (impossible to get the true Java Duke out of Dall-E 😢 )

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/duke_loom.png" alt="Java Duke with Loom and Virtual Threads" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

_Funny cats, wasting computational resources since the invention of the internet_

Make sure the folder is created beforehand. Image generation is calculation intensive. Generation can take a while and costs much more than text generation, for example $0.02 for a Dall-E 2 image and $0.08 for Dall-E 3.

Keep in mind that image generation is typically subject to **rate limits** that depend on your payment options, so before you launch your app on a big scale, make sure your subscription can keep up.

### **Audio models**

LangChain4j supports **speech-to-text** conversion with **Gemini** (support for more models is coming). The input is a String of the audio file in base64 format. Gemini will typically take your audio instructions (like “_who created Java_” and immediately take action, by replying “_James Gosling_”). If instead you want to obtain a literal transcription of your audio, you can prompt it as in the code example below.

```
ChatLanguageModel model = GoogleAiGeminiChatModel.builder()
       .apiKey(System.getenv("GEMINI_TOKEN"))
       .modelName("gemini-1.5-flash-001")
       .build();


ChatResponse response = model.chat(
       SystemMessage.from("repeat the text from the audio message"),
       new UserMessage(AudioContent.from(base64, "audio/mp3")));


String message = response.aiMessage().text();
```


Message Roles
-------------

Before we continue, we need to introduce some important implementations of LangChain4j’s **`ChatMessage`** API:

*   **`SystemMessage`**: a message that we can optionally set to give general instructions to a model that will apply for the entire conversation. Eg. “_You are a java programmer talking to a 3 year old_ ”.
*   **`UserMessage`**: the user input (query, prompt)
*   **`AiMessage`**: the reply of the model

They can be used like this:

```
UserMessage userMessage = UserMessage.from("How can I program my cat to fetch sticks for me?");
AiMessage firstAiMessage = model.chat(userMessage).aiMessage();
```


AI Services
-----------

Now we know how to perform basic interactions with models, I want to introduce you to a somewhat strange but very powerful concept in LangChain4j: AiServices, your companion for every problem. I introduce them early on because they make the **syntax** to plug in other components (memory, tools, …) much **more concise**.

AiServices consist of an **interface** that describes what you want to happen. After which you can use a **builder to create the implementation** for you, specifying what **components** you want to add to it (model, RAG, tools, …).

Some examples can explain this better than 1000 words. Here’s a basic AiService:

```
interface Programmer {
   @SystemMessage("You are a java programmer talking to a 3 year old")
   String answer(String question);
}
```


The interface describes what we want: a `Programmer` object with one method: `answer(String)`. We specify a `SystemMessage` (this is optional).

*   The input is a `String`, so LangChain4j will infer that this is the `UserMessage`.
*   The output is a `String`, so LangChain4j will automatically infer that this is the model output.

Now we want to create and use such a `Programmer` object (in the code below, `model` is a `ChatLanguageModel` that we created beforehand).

```
Programmer programmer = AiServices.create(Programmer.class, model);

String answer = programmer.answer("How can I program my cat to fetch sticks for me? Be concise");
```


Running this code will return something like (love this!):

```
Oh, little coder! 🐱✨ You can’t *program* a cat like a computer, but you can *train* it! Just like Java has loops, training takes **repetition**! 

1. **Give treat** 🍗 when kitty touches the stick. 

2. **Move stick a little** ➡️ and give treat again! 

3. **Throw stick** and reward when kitty brings it back! 

Like a while-loop: 

`while(cat_fetches) { giveTreat(); }` 

But remember, cats have their own "Garbage Collector"—they ignore stuff when bored! 😹
```


### Input parameters and structured outputs

Now starts the real fun! LangChain4j allows you to get **java objects out of LLMs** so you can just code on instead of parsing Strings all the time. Here are some examples of how to use these **structured outputs**, and what kind of combinations are possible in the input parameters with `@UserMessage` and `@SystemMessage`. `TextUtils`, our AiService, has 3 methods this time:

```
interface TextUtils {

   @SystemMessage("You are a professional translator into {{language}}")
   @UserMessage("Translate the following text: {{text}}")
   String translate(@V("text") String text, @V("language") String language);

   @SystemMessage("Summarize the user messag in {{n}} bullet points. Provide only bullet points.")
   List<String> summarize(@UserMessage String text, @V("n") int n);

   @UserMessage("Extract date and time from {{it}}")
   LocalDateTime extractDateTimeFrom(String text);
}
```

We create an instance, so we can actually use them:

```
TextUtils utils = AiServices.create(TextUtils.class, model);
```


`translate()` will return a `String`, so the direct output of the model.

```
String translation = utils.translate("Hello, how are you?", "italian");
```


`summarize()` will return a Java object `List<String>`.

```
String text = "AI is a branch of computer science that aims to create machines that mimic human intelligence. E.g. recognizing patterns or making decisions or predictions.";
List<String> bulletPoints = utils.summarize(text, 3);
```


`extractDateTimeFrom()` is my favorite, done with endless parsing of date formats (if you can live with something that is _mostly_ right but not always!)

```
text = "Three days before St. Valentine's Day of 2024, " +
       "just 15 minutes shy of midnight, " +
       "Jane discovered Jim was more in love with his IDE than with her.";
LocalDateTime dateTime = utils.extractDateTimeFrom(text);
```

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/prefect_date.png" alt="Prefect Date Example" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Good to know: you can also make them return a self-defined POJO 🔥 For example a Person object:

```
static class Person {
   @Description("first name of a person") // optional description for LLM
   private String firstName;
   private String lastName;
   private LocalDate birthDate;
   }
```


And an AiService to extract all Persons from text fragments (great for analyzing archives)

```
interface PersonExtractor {
   @UserMessage("Extract all different persons from the following text: {{it}}")
   List<Person> extractPersonFrom(String text);
}
```


Memory
------

Models are **stateless**, so if you want them to remember what has been said before, you have to **send the history along every time**. Most models' APIs provide a way to pass older messages from the conversation. LangChain4j wraps all the different syntaxes under one interface: `**ChatMemory**`. This is what memory looks like when we send it to an LLM

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/20-functionality/memory.png" alt="Memory Management in LLMs" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

In theory we could keep the whole conversation in the memory, but it is sent along with every request. Memory eats tokens, and at some point we hit the size of the **context window**, the maximal number of tokens that a model accepts as input (model dependent). So we will need a **strategy to reduce the memory size**. LangChain4j comes with 2 default implementations:

*   `**MessageWindowChatMemory**`, which will drop the oldest messages

```
ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);
```


*   Or `**TokenWindowChatMemory**`, which will drop the oldest tokens

```
ChatMemory chatMemory = TokenWindowChatMemory.withMaxTokens(1000, new OpenAiTokenizer());
```


`ChatMemory` is an interface, so you can write any implementation that makes sense for you, for example a `**SummarizingChatMemory**` that will keep track of important context based on your use case.

A `ChatMemory` is basically a **list of `ChatMessages`** (see before), and you can manually add the messages for every `UserMessage` you send and every `AiMessage` you receive back. But if you **combine `ChatMemory` with an `AiService`**, LangChain4j will take care of updating the memory for you. For example

```
Programmer programmer = AiServices.builder(Programmer.class)
       .chatLanguageModel(model)
       .chatMemory(chatMemory)
       .build();
```


If you want to test if the memory is functioning properly, tell the model your name and ask ‘_what is my name_’ as the next question.

In a real application you will typically want to maintain and persist a memory per user. LangChain4j provides `MemoryId` functionality for this

```
interface Programmer {
   String chat(@MemoryId int memoryId, @UserMessage String userMessage);
}
```


In our langchain4j-examples repo (see link at the end), in the folder `tutorials`, you find this example fully elaborated with the memory per user persisted to a database.

### Few Shot Examples

Do you want your model to behave in a certain way, but it’s not listening very well to your prompts and instructions? A more powerful technique is to pretend that the LLM behaved in the correct way by providing a **fake memory pre-filled with examples**, like this (if you need help setting boundaries 😉)

```
fewShotHistory.add(UserMessage.from("My mom wants me to call every day.")); fewShotHistory.add(AiMessage.from("You're not a podcast."));  
fewShotHistory.add(UserMessage.from("My partner always lets me do the laundry.")); 
fewShotHistory.add(AiMessage.from("Did their hands fall off?"));  
fewShotHistory.add(UserMessage.from("Toddler is crying bcs he didn’t get the pink cup.")); 
fewShotHistory.add(AiMessage.from("Tragic. For them."));
```


Now add this `fewShotHistory` as memory to your `AiService`, ask it anything and enjoy your boundary coach!

Until now the models have returned text, images and java objects. A lot of models have an extra capability that makes them really powerful (and dangerous): calling your code. Are you in camp 🥳 or camp 😱 ?

You can provide a **method that a model can call**, such as sending an email, calculating interest or writing something to the database. Models that support **function calling (tool calling)** will reply with a function call including method name and parameter values when they think the question requires using the tool. We will run the called method and send the result back to the model, which will use the answer in its final reply.

LangChain4j makes that super easy, by using the **`@Tool` annotation** as follows (the tools are part of class `ShoppingTools` in this example)

```
@Tool
public List<String> getProductList() {
// custom code to obtain the list
}

@Tool("returns product description, price and availability")
public String getProductDetails(@P("5 digits product ID") int prodID) {
// custom code to obtain the product details
}
```


If we have a `ShoppingAssistant` interface declared with a method `giveProductSuggestion(String userMessage)`, we can make the tools available as follows

```
ShoppingAssistant shoppingAssistant = AiServices.builder(ShoppingAssistant.class)
       .chatLanguageModel(model)
       .tools(new ShoppingTools())
```


If we now run 

```
shoppingAssistant.giveProductSuggestion("I’m looking for a statue of Yoda that can sing Xmas songs"); 
```


the model will (in most of the cases) call `getProductList()`, see if there’s anything in there that seems to match my request, and if yes, it will call `getProductDetails()` with the `productID` that it got as a result from `getProductList()`.  
It will then use all that information to craft a reply, like _“It seems like we don’t have a Yoda statue that sings Christmas songs, but I did find a singing Christmas goat in our catalog for 15.99$”_.

Good models are able to **call tools sequentially and in parallel**. In the example, it will first ask for the product list, and only then get specific product details. If it finds multiple singing Yoda’s that might carry my fancy, it will then call `getProductDetails` multiple times in parallel with the different product IDs.

Model calls and its subsequent tool calls are often **high latency**, so virtual threads come in handy to free resources while waiting for results.

Good to know: tools don’t work with all models, you can find the supported ones in the model integration list ([docs.langchain4j.dev/integrations/language-models](https://docs.langchain4j.dev/integrations/language-models/)).

You can do a lot more things with tools: **adding tools from different classes, specifying tools dynamically, returning the tool result as final answer**, … you can find how to do all that in our documentation [docs.langchain4j.dev/tutorials/tools](https://docs.langchain4j.dev/tutorials/tools/)

### Human as a tool

LLMs executing tools, placing orders and accessing the database is dangerous. Depending on the **risks or resources involved in executing a tool call**, you may want to have some hard **code checks** in place (for example authentication) or ask the user for **permission** to proceed. The latter is called **human-as-a-tool or human-in-the-loop**, and can be obtained by adding a request for permission to run the tool as first thing in the tool code. If the answer is yes, the code continues, if no, you can throw an error back to the model that the user (or the verification code) did not allow the operation.

### MCP servers

If you’re anything like me, you’re probably hyperventilating by now and seeing all kinds of new automations that will make your life so much easier. Triage my emails, extract the TODOs, place them smartly in my agenda based on priorities and my existing calendar entries and and and… The new bottleneck for developers is **writing all the tools** that allow the LLM to execute these requests.

At the moment integrating with different services requires a different syntax and sometimes execution environment for almost anything you try to do. Github? git + ssh. Database? SQL + sqlplus. Local file system? Bash + terminal. Weather service? Custom REST API + curl. That’s a steep learning curve and quite hard to automate.

But the good news is, last November, Anthropic published the **Model Context Protocol (MCP)**, an open standard for **exposing LLM-readable tools**. The protocol got a lot of traction, and by now you can find hundreds of MCP servers on Github, just google ‘MCP server PostgreSQL’ (or Grafana, Github, Atlassian Gmail, … you name it). You can also **create and publish your own MCP server** really easily using Quarkus. Once you find a server, you can use it via LangChain4j’s integration like this:

```
McpTransport transport = new StdioMcpTransport.Builder()
       .command(List.of("/usr/local/bin/docker", "run", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "-i", "mcp/github"))
       .logEvents(true)
       .build();

McpClient mcpClient = new DefaultMcpClient.Builder()
       .transport(transport)
       .build();

ToolProvider toolProvider = McpToolProvider.builder()
       .mcpClients(List.of(mcpClient))
       .build();

Bot bot = AiServices.builder(Bot.class)
       .chatLanguageModel(model)
       .toolProvider(toolProvider)
       .build();
```


You’ll typically need some **API key to connect to services** giving access to personal information, like `GITHUB_PERSONAL_ACCESS_TOKEN` in the example.  
This example uses `**stdio**` for communicating with your process. There are also servers that use `**http**`, see langchain4j-examples for the details.

The server exposes **descriptions of available methods and parameters to the LLM**. The server also takes care of **translating parameters** it is called with **into the right syntax**, and to **execute** the request, skipping all the difficulty of the previous diagram. The example above let's an LLM create new branches and inspect PRs. Beautiful. Dangerous.

<img src="/java-ai-resource/img/10-genai/mcp_architecture.png" alt="MCP Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Ease of integration with MCP servers

Important note: LLMs can be manipulated and unpredictable. Watch out before granting your LLM the rights to wipe your database or send emails autonomously!

Career tip: Developers may be at risk of losing their job to AI, but if you go into (LLM) security, you’re guaranteed to stay in demand 😅

<img src="https://javapro.io/wp-content/uploads/2025/02/image-74.png" alt="MCP Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />


RAG
---

By now we can build really interesting LLM-powered apps. One last thing to address is that each model was **trained on a specific dataset**. We can’t hope for it to give us any information that was not present in its training data, such as the weather today, your company-specific procedures, your product database. In the best case it will say that it doesn’t know, in the worst (and more prevalent) case, it will hallucinate something that sounds plausible. So we need a way to let the model know about all that extra information that was not part of its training data.

One solution would be to ask our question and send all the available data along. It would probably work but you will pay a lot for all those tokens. If everything would fit in the context window in the first place. That is why we want to only pass the extra information to the model that is **relevant** to our question. This is called **Retrieval-Augmented Generation (RAG)** and this is how it looks schematically:

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/20-functionality/basic_rag.png" alt="Basic RAG Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Side note: if you think RAG is an ugly name, so do its creators. Quote Patrick Lewis: _"We always planned to have a nicer sounding name, but when it was time to write the paper, no one had a better idea."_

The relevant fragments of information, we need to search in the context that we offer to the model. LangChain4j has an interface `**ContentRetriever**` where you can implement your own retriever. We also provide the 4 most used ways out of the box (examples for each can be found under `/rag` in `langchain4j-examples`):

*   **WebSearchEngineContentRetriever**: the LLM turns the original prompt into a web search query and a number of search results are used as context
*   **SqlContentRetriever**: the LLM is given the database schema and turns the original prompt into SQL to retrieve information that will be used as context
*   **Neo4jContentRetriever**: the LLM is given the schema and turns the original prompt into Cypher (neo4j query) to retrieve information that will be used as context
*   **EmbeddingStoreContentRetriever**: to retrieve relevant fragments from all documents that we provide (text, excel, images, audio, …). To find relevant fragments, we need to prepare our sources in advance in an **ingestion step**: We first **chunk** our sources into fragments, then we calculate a numerical **vector representation (embedding)** that encodes the meaning of each fragment (or image, table, …), using an **embedding model**. Finally, all embeddings are saved in an `**EmbeddingStore**` together with the original fragments. When the user asks a question, we will create an embedding of the question and **retrieve** the closest matches in our `EmbeddingStore`. This is called **semantic similarity search**.

<img src="https://javapro.io/wp-content/uploads/2025/02/image-55.png" alt="rag_schematic" style={{width: '80%', display: 'block', margin: 'auto'}} />

<br />

Lazy tip: In Quarkus, you can add an `EmbeddingStoreContentRetriever` to your `AiService` by simply adding the dependency `**quarkus-langchain4j-easy-rag**` and specifying `quarkus.langchain4j.easy-rag.path` in `application.properties`. This will use all documents stored in that folder as RAG sources.

Expert tip: Embeddings (vectors) can also be used to group topics or to find categories in data, by grouping the closest vectors together.

RAG works much better when we add some **advanced RAG** components around the `ContentRetriever` and its ContentInjector. Here are the available interfaces with their out-of-the-box implementations mentioned underneath:

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/20-functionality/advanced_rag.png" alt="Advanced RAG Architecture" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Advanced RAG (courtesy: Dmytro Liubarskyi)

*   **`QueryTransformers`**: they are very important to make RAG work properly. Imagine your RAG system has access to web search. The LLM asks you if you want to proceed with, say, the selected products. You say ‘yes please’, and off it goes searching the internet for ‘_yes please_’. You don’t want that, especially not in production. You will want a **`CompressingQueryTransformer`** that will take the rest of the conversation into account when forming its query, and turn ‘_yes please_’ in eg. ‘_proceed with selection of products: singing Yoda and Christmas goat_’. **`ExpandingQueryTransformer`** works similarly, but may create multiple queries to ensure an answer is found.
*   If you wish to use **different `ContentRetrievers` in parallel**, you can store them in a map, like this

```
Map<ContentRetriever, String> retrieverToDescription:
literatureDocsRetriever -> "Scientific literature on antibodies"
webSearchContentRetriever -> "Web search"
sequenceDbContentRetriever -> "Protein database with sequences" 
```


*   A **`QueryRouter`** will choose which `ContentRetriever(s)` the question should be sent to. You can write an own implementation, for example based on keywords, or use the `**LanguageModelQueryRouter**` that uses another LLM to route the question and transform it into queries for the different retriever types.
*   **`ContentAggregator`**: the **`DefaultContentAggregator`** will simply put all selected fragments one after the other. However, very often (especially with `EmbeddingStoreContentRetriever`) fragments are found that are not related to the question and will only confuse the LLM if we send them along. You can use a **`ReRankingQueryTransformer`** to remove unrelated fragments. It uses a tiny and super fast scoring model specialized in scoring how relevant a piece of information is for a question.
*   The **`ContentInjector`** simply wraps your original message plus the extra fragments of content as follows:  
    `"{{userMessage}} \n\n "Answer using the following information: \n {{contents}}"`  
    If you want another message here or if you are using a different language, you can overwrite this as shown in the example below. The example also shows how all parts come together

```
RetrievalAugmentor retrievalAugmentor = DefaultRetrievalAugmentor.builder()
       .queryTransformer(queryTransformer)
       .queryRouter(queryRouter)
       .contentAggregator(contentAggregator)
       .contentInjector(DefaultContentInjector.builder()
               .promptTemplate(
                       PromptTemplate.from("{{userMessage}}\n" +
                               "\n" +
                               "you can use the following information:\n" +
                               "{{contents}}"))
               .build())
       .build();
```


We can add this `RetrievalAugmentor` to our `Programmer` AiService like this

```
AiServices.builder(Programmer.class)
                       .chatLanguageModel(model)
                       .retrievalAugmentor(retrievalAugmentor)
                       .build();

```


Good to know: In **RAG** everything happens in parallel and **in one shot**. This means it will fail for questions that require sequential searching like _‘find the sequence of an antigen of disease xyz’_, because it will need to find the antigen first before it can query the database for it’s sequence (that would be step 2). If you want to allow **iterative searching**, you can **wrap your `ContentRetrievers` as `Tools`** and the model will know which ones to call in which order.

In [github.com/langchain4j/langchain4j-examples/tree/main/rag-examples](http://github.com/langchain4j/langchain4j-examples/tree/main/rag-examples) you can find examples of all the above, as well as examples where **sources** are retrieved and passed along, and an example of the use of **metadata** stored with the fragments (to store read permissions or sources for example).

Agentic Systems
---------------

AI Agents is a very wide term that can cover anything from an LLM augmented with tools to a full-blown complex workflow system with multiple LLMs, orchestrators, workers, gatekeepers and sophisticated interactions with the environment.

### Basic Agent: LLM calls code

As a rule of thumb, **build only the complexity that you need**. For example, commercial LLMs can often perform quite complex tasks if you tell them the **steps** they need to run through, and the **tools** they need to use. If their tools include means to **perform actions and observe the result**, we have a basic AI Agent.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/basic_agent.png" alt="Basic Agent Diagram" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Inspired by Anthropic agent architectures

As you can see, a LangChain4j `AiService` can easily do that, the programmatic difficulty lies mainly in creating good tools. MCP servers made that part a lot easier.

### State Machine: Code calls LLM calls code

If you need more **control over the workflow**, you may consider structuring your process as a state machine, with the different **steps (nodes)** and **transition criteria (edges)** programmatically defined. The functionality inside of the **nodes** can be performed by **AiServices** (like determining which financial profile the customer has via guided chat) or nodes can be **purely algorithmic** (like running the calculations for the loan based on the financial profile – where using an LLM makes no sense). 

The advantage here is more control and **separation of concerns (and responsibilities)** so LLMs don't overstep their boundaries. It makes it much easier to **add security checks** and **limit permissions** for each node. It also allows us to outsource to code what better happens in code, and to pick **tiny models for simple tasks** and **specialized models for specialized tasks**. For example, for node transitions after a chat, you often get a situation like 

```
Model: Can you confirm your product selection?
User: I still want to add a singing goat doll!
```


To determine whether this means that you can move on to the next node (verify basket), or you stay in the current node a bit longer (select products), you can easily train a Bayesian classifier on 30 examples. It will do a great job and requires orders of magnitude less resources and latency.

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/shopping_state_machine.png" alt="Shopping State Machine" style={{width: '80%', display: 'block', margin: 'auto'}} />

<br />

It's easier to program than it sounds: state machines are easy to code, and you can call AiServices in the nodes or on the edges, wherever it makes sense. Often you'll also need an object to store the state, eg. the state of the shopping basket, the user profile, …

### Combinations

It gets really interesting when we wrap AiServices in tools. For example:

```
@Tool
void determineFinancialProfile(){
    FinancialProfileAiService.determineProfile(); // AiService 
    // that has access to chat and tools 
    // to complete a FinancialProfile object that keeps the state
}
```


Now we can let another AiService, for example `BankChatBot` (the **orchestrator**) determine which other AiServices (wrapped in tools) to call. When the user asks the `BankChatBot` for a loan for example, the bot will know to call `determineFinancialProfile()` and `checkDebtRecords(String personID)`. That would be a variant of this architecture

<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/orchestrator_synthesizer.png" alt="Orchestrator Synthesizer" style={{width: '80%', display: 'block', margin: 'auto'}} />

<br />

Inspired by Anthropic agent architectures

If the quality of the result is important, you can implement a pattern where a second LLM or AiService **evaluates** the first one:

<img src="https://javapro.io/wp-content/uploads/2025/02/image-80.png" alt="Evaluator" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

Inspired by Anthropic agent architectures

All these patterns are combinable, adaptable to your specific use case and surprisingly easy to program using `AiServices` and `Tools`. Where suitable tools can wrap other AiServices.

An important thing to keep in mind here is that model calls and tool calls introduce significant **latency**: depending on model and number of consumed/generated tokens it can be anything from 100s of milliseconds to 10s of seconds. So if your process allows it, keep the number of LLM calls low and use small (fast, cheap) specialized models.

Further reading: some more agentic architectures are covered in this article by Anthropic www.anthropic.com/research/building-effective-agents

Production Features
-------------------

LLMs + production = nightmare? I feel you! But we can mitigate a lot with a number of more production-oriented features. In the second part of this JAVAPRO edition, we’ll get a whole article dedicated to those, but for the people that can’t wait, here are a couple of pointers to get you started (more details can be found online).

**Moderation**: some models like `AzureOpenAI` come with built-in moderation that will check the model output for aspects like violence, so it allows you to filter out those responses.

**GuardRails**: at the time of writing only available in `quarkus-langchain4j`, but coming soon to vanilla LangChain4j. `**InputGuardrails**` and `**OutputGuardrails**` are very powerful gatekeepers that will check if the prompt or the model input/output match certain criteria before sending it on. You can even use another LLM to do the check.

**Observability**: `ChatModelListeners` allow you to observe things like `inputTokenCount` to calculate cost, or `finishReason` to keep statistics of failed calls.

**Testing non-deterministic apps:** tests with retries come with `Junit Pioneer`, or even better (only in `quarkus-langchain4j` for now) `@QuarkusTest` allows you to give a score to your test output instead of having a clear pass vs. fail scenario. You can use scoring strategies like `AiJudgeStrategy` and `SemanticSimilarityStrategy` or create your own custom implementation.

**Human feedback:** at my company Naboo.ai, we noticed that having all the above in place is still not sufficient to guarantee an excellent user experience. If, like us, you deal with user queries as input ("_ask anything regarding your project and integrated tool_s"), the variety of what users will ask beats anything you could have predicted upfront. It even beats what the overzealous testers could come up with!


<img src="/java-ai-resource/img/10-genai/30-using-llms-in-code/30-frameworks/users_program.png" alt="User Programming Interface" style={{width: '50%', display: 'block', margin: 'auto'}} />

<br />

We solved this by collecting user feedback (thumbs up, or more important for us: thumbs down). If you want to offer a great user experience, consider a pilot phase where you manually review the creative caprices of your customers and extend your system to cover them. Once in production, you can continue gathering this feedback and use embeddings to find the most prevalent negative feedback categories and address those.

Important links
---------------

*   LangChain4j repo: [github.com/langchain4j/langchain4j](https://github.com/langchain4j/langchain4j)
*   The dreaded but beautiful documentation (It doesn’t bite! It’s trying to be likeable with tutorials ♥️): [docs.langchain4j.dev](https://docs.langchain4j.dev/)
*   Community incubator repo for new integrations: [github.com/langchain4j/langchain4j-community](https://github.com/langchain4j/langchain4j-community)
*   Examples repo: [github.com/langchain4j/langchain4j-examples](https://github.com/langchain4j/langchain4j-examples)
*   Awesome LangChain4j examples: [github.com/langchain4j/awesome-langchain4j](https://github.com/langchain4j/awesome-langchain4j)
*   LangChain4j Discord: [discord.com/invite/JzTFvyjG6R](https://discord.com/invite/JzTFvyjG6R)

Thank you and FAQ
-----------------

*   LangChain4j was **created** in 2023 by **Dmytro Liubarskyi**, who is still its relentless lead engineer. Thank you so much for your awesome work!
*   **Immense thanks to our 200+ contributors!** Proudly listing the top 20 here, but everyone that didn’t make it to this list, we see you! Thank you Julien Dubois, Crutcher Dunnavant, Martin7-1, Konstantin Pavlov, jiangsier-xyz, Guillaume Laforge, Antonio Goncalves, Eddú Meléndez Gonzales, omarmahamid, Carlos Zela Bueno, Alexey Titov, Jan Martiska, xermaor, Georgios Andrianakis, kuraleta, bidek, Julien Perrochet, PrimosK, Eric Deandrea, Mario Fusco and all the other contributors ♥️
*   **LangChain4j** is used **in production** in projects like MuleSoft by Salesforce, Advanced Coding Assistant by Deutsche Telekom, Apache Camel, MicroProfile, Wildfly, Micronaut and many more projects. We’re proud ^^
*   _**Where are the chains in LangChain4j?**_ Well erm, just like RAG, names are sticky… we abandoned the chains for the more versatile AiServices 🚀
*   **_How do I contribute?_** You are very welcome to contribute! Bug fixes may not be the most glamorous thing, but they actually help us a ton and we appreciate it tremendously. For more tips and tricks, the contributor guide is linked in the readme.
*   _**Aren’t the swag and the model licenses for testing expensive?**_ Yes they are, so feel free to drop us some coins via [opencollective.com/langchain4j](http://opencollective.com/langchain4j) for a swaggier future ☕🦜
*   _**How much does it cost to use GPT4, or Gemini, or… ?**_ Not that much, especially compared to the value they may bring to your product. Model pricing depends on the model quality (which you can assess using benchmarks, eg. [www.livebench.ai](http://www.livebench.ai/)) and are calculated in function of input tokens (less expensive) and output tokens (more expensive). For a pricing overview, check llm-price.com. Tokens typically are about 3 characters long, so to give an idea, with `GPT4` you get around 12 A4 pages output for 1$, and for `claude-3.5-sonnet` that would be 48 pages for the same price.
*   _**Just how good is a local model?**_ It depends a lot on how much GPU you have available to run it on! For 700GB GPU you can run `deepseek-r1`, which performs in the top 5 of best models at the moment of writing, or `Llama-3.1-405B-Instruct` which performs in the top 30. But you will need specialized, expensive hardware. Models of around 70GB can run reasonably fast on a laptop, for example a Macbook Pro with enough unified memory (GPU+CPU) and still perform reasonably well. If you want to serve multiple users simultaneously, you need to do some research on the latency though. Then there are the really small models like Microsoft’s `phi3`, which is under 4GB. Some of those tiny models still perform very well for just language interaction with humans, but fail on more complex tasks and are very unreliable for tool calling.

---

*Written by Lize Raes*
