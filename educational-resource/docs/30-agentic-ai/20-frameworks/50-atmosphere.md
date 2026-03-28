---
title: Atmosphere
sidebar_position: 50
hide_title: true

level: intermediate
status: published
visibility: public

# OPTIONAL TAGS:
external-link: https://github.com/Atmosphere/atmosphere
programming-language: "Java"
---

# Atmosphere

**<h2><a href="https://github.com/Atmosphere/atmosphere" target="_blank" rel="noopener noreferrer">👉 Visit Atmosphere on GitHub ↗</a></h2>**

[Documentation](https://atmosphere.github.io/docs/) · [Tutorial](https://atmosphere.github.io/docs/tutorial/01-introduction/) · [Samples](https://github.com/Atmosphere/atmosphere/tree/main/samples)

Atmosphere is a real-time transport abstraction framework for Java. It handles WebSocket, SSE, HTTP long-polling, and gRPC — with automatic transport negotiation, message caching, reconnection, and clustering. Built and maintained over many years.

The AI agent layer was built on top of that foundation. An `@Agent` class defines prompts, commands, and tools. The AI execution engine — tool calling, memory, RAG, retries — is pluggable via the `AgentRuntime` SPI and determined by classpath: Spring AI, LangChain4j, Google ADK, or Embabel. The framework also handles protocol exposure (MCP, A2A, AG-UI) and messaging channels (Slack, Telegram, Discord).

## Architecture

Atmosphere follows the Servlet model: application code is separate from the execution engine.

| Servlet analogy | Atmosphere equivalent |
|-----------------|----------------------|
| `Servlet` / `@Controller` | `@Agent` / `@Prompt` |
| Tomcat, Jetty, Undertow | LangChain4j, Spring AI, ADK, Embabel |
| `AsyncSupport` (container SPI) | `AgentRuntime` (framework SPI) |
| HTTP, WebSocket | MCP, A2A, AG-UI |
| `web.xml` / annotations | Skill files (Markdown + YAML) |

The `@Agent` class declares what the agent does. The `AgentRuntime` on the classpath determines how it executes: tool calling loops, conversation memory, RAG retrieval, retries, and guardrails.

## Supported Runtimes

| Runtime | Module | Capabilities |
|---------|--------|-------------|
| **Built-in** | `atmosphere-ai` | OpenAI-compatible client (Gemini, OpenAI, Ollama) |
| **LangChain4j** | `atmosphere-langchain4j` | ReAct tool loops, `StreamingChatModel`, retries. `@AiTool` methods bridged to LangChain4j tools. |
| **Spring AI** | `atmosphere-spring-ai` | `ChatClient`, function calling, RAG advisors |
| **Google ADK** | `atmosphere-adk` | `LlmAgent`, function tools, session management |
| **Embabel** | `atmosphere-embabel` | Goal-driven GOAP planning |

Switching runtimes requires changing one Maven dependency. Agent code, tools, commands, and skill files remain the same.

## Framework Capabilities

These work regardless of which `AgentRuntime` is active:

- **Real-time streaming** — LLM tokens delivered via WebSocket/SSE
- **Protocol exposure** — MCP, A2A, and AG-UI endpoints auto-register from classpath
- **Multi-agent orchestration** — `@Coordinator` + `@Fleet` for parallel fan-out, sequential pipelines, coordination journal
- **Conversation memory** — multi-turn context persisted to SQLite or Redis
- **Tool portability** — `@AiTool` methods work across all runtimes
- **Skill files** — Markdown with YAML frontmatter for agent persona, tools, guardrails, and channel routing
- **Messaging channels** — Slack, Telegram, Discord, WhatsApp, Messenger via bot token configuration
- **Servlet integration** — runs as a filter in Spring Boot, Quarkus, or any Servlet 6.0+ container

## Quick Start

The Atmosphere CLI scaffolds new projects and runs existing samples directly:

```bash
brew install Atmosphere/tap/atmosphere

# Scaffold a new project
atmosphere new my-agent --template ai-chat
cd my-agent && LLM_API_KEY=your-key ./mvnw spring-boot:run

# Or run any of the 18 built-in samples
atmosphere list
atmosphere run spring-boot-ai-chat
```

```java
@Agent(name = "my-agent", description = "What this agent does")
public class MyAgent {

    @Prompt
    public void onMessage(String message, StreamingSession session) {
        session.stream(message);  // Dispatches to active AgentRuntime
    }

    @Command(value = "/status", description = "Show status")
    public String status() {
        return "All systems operational";
    }

    @AiTool(name = "lookup", description = "Look up data")
    public String lookup(@Param("query") String query) {
        return "Result for: " + query;
    }
}
```

## Protocol Support

| Protocol | Standard |
|----------|----------|
| MCP | Model Context Protocol |
| A2A | Agent-to-Agent Protocol |
| AG-UI | Agent-User Interaction Protocol |

Protocols auto-register based on classpath detection.

## Requirements

Java 21+. Spring Boot 4.0, Quarkus 3.21, or any Servlet 6.0+ container.

## Related Resources

- [A2A Protocol](./40-a2a-protocol.md) — Atmosphere implements A2A for agent-to-agent communication
- [Google ADK](./10-adk.md) — supported as an AgentRuntime backend
