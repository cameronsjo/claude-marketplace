# AI/LLM Integration Skill

Build production-ready AI/LLM applications including RAG systems, vector search, agent orchestration, and LLM API integrations.

## Overview

This skill provides comprehensive expertise for integrating AI and LLM capabilities into applications with focus on RAG (Retrieval-Augmented Generation), vector databases, prompt management, and agent orchestration.

## When to Use This Skill

Trigger this skill when:
- Building RAG (Retrieval-Augmented Generation) systems
- Implementing vector search and embeddings
- Integrating LLM APIs (OpenAI, Anthropic, etc.)
- Creating AI-powered features
- Building agent orchestration systems
- Managing prompt templates and versioning
- Implementing semantic search
- Optimizing LLM performance and costs
- Handling LLM rate limiting and retries
- Building chatbots or conversational AI

**Keywords:** RAG, retrieval augmented generation, vector search, embeddings, LLM integration, AI features, semantic search, agent orchestration, chatbot, OpenAI, Claude API

## Core Principles

### AI Application Architecture

1. **Retrieval-Augmented Generation (RAG)**: Combine LLMs with external knowledge
2. **Vector Search**: Semantic similarity for intelligent retrieval
3. **Prompt Engineering**: Craft effective prompts (see prompt-engineering skill)
4. **Cost Optimization**: Minimize tokens, cache responses
5. **Error Handling**: Handle rate limits, timeouts, API failures
6. **Observability**: Log prompts, responses, latency, costs
7. **Safety**: Content moderation, PII protection, prompt injection prevention

## RAG System Architecture

### Basic RAG Pipeline

```
User Query → Embedding → Vector Search → Context Retrieval → Prompt Construction → LLM → Response
```

### Complete RAG Implementation

```python
from typing import List, Dict, Any
import openai
from sentence_transformers import SentenceTransformer
import chromadb
from pydantic import BaseModel

class Document(BaseModel):
    """Document with metadata"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float] | None = None

class RAGSystem:
    """Production RAG system"""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "gpt-4",
        collection_name: str = "documents"
    ):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)

        # Initialize vector database
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)

        # Initialize LLM
        self.llm_model = llm_model

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vector database"""
        for doc in documents:
            if doc.embedding is None:
                doc.embedding = self.embed_text(doc.content)

            self.collection.add(
                ids=[doc.id],
                embeddings=[doc.embedding],
                documents=[doc.content],
                metadatas=[doc.metadata]
            )

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        query_embedding = self.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter
        )

        return [
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
            for i in range(len(results["ids"][0]))
        ]

    def generate_response(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: str | None = None
    ) -> str:
        """Generate response using LLM with context"""

        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(context_docs)
        ])

        # Construct prompt
        if system_prompt is None:
            system_prompt = """You are a helpful assistant that answers questions based on the provided context.
If the context doesn't contain relevant information, say so clearly."""

        user_prompt = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        # Call LLM
        response = openai.ChatCompletion.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    async def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Complete RAG query pipeline"""

        # 1. Search for relevant documents
        relevant_docs = self.search(question, top_k=top_k)

        # 2. Generate response with context
        response = self.generate_response(question, relevant_docs)

        # 3. Return response with sources
        return {
            "answer": response,
            "sources": [
                {
                    "content": doc["content"][:200] + "...",
                    "metadata": doc["metadata"],
                    "relevance_score": 1 - doc["distance"]
                }
                for doc in relevant_docs
            ]
        }

# Usage
rag = RAGSystem()

# Add documents
documents = [
    Document(
        id="doc1",
        content="Python is a high-level programming language...",
        metadata={"source": "docs", "category": "programming"}
    ),
    Document(
        id="doc2",
        content="Machine learning is a subset of AI...",
        metadata={"source": "docs", "category": "ai"}
    )
]
rag.add_documents(documents)

# Query
result = await rag.query("What is Python?")
print(result["answer"])
print("Sources:", result["sources"])
```

## Vector Databases

### ChromaDB (Embedded)

```python
import chromadb
from chromadb.config import Settings

# Persistent storage
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

collection = client.get_or_create_collection(
    name="documents",
    metadata={"description": "Document embeddings"}
)

# Add embeddings
collection.add(
    ids=["id1", "id2"],
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
    documents=["This is document 1", "This is document 2"],
    metadatas=[{"source": "web"}, {"source": "pdf"}]
)

# Query
results = collection.query(
    query_embeddings=[[1.1, 2.3, 4.5]],
    n_results=2,
    where={"source": "web"}
)
```

### Pinecone (Cloud)

```python
import pinecone

# Initialize
pinecone.init(
    api_key="your-api-key",
    environment="us-west1-gcp"
)

# Create index
index_name = "documents"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        index_name,
        dimension=384,  # Embedding dimension
        metric="cosine"
    )

index = pinecone.Index(index_name)

# Upsert vectors
index.upsert(vectors=[
    ("id1", [0.1, 0.2, ...], {"text": "Document 1"}),
    ("id2", [0.3, 0.4, ...], {"text": "Document 2"})
])

# Query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    include_metadata=True
)
```

### Weaviate (Graph + Vector)

```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "class": "Document",
    "vectorizer": "text2vec-openai",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "title", "dataType": ["string"]},
        {"name": "category", "dataType": ["string"]}
    ]
}
client.schema.create_class(schema)

# Add data
client.data_object.create(
    data_object={
        "content": "Document content here...",
        "title": "My Document",
        "category": "technical"
    },
    class_name="Document"
)

# Semantic search
result = client.query.get("Document", ["content", "title"]) \
    .with_near_text({"concepts": ["python programming"]}) \
    .with_limit(5) \
    .do()
```

## LLM API Integration

### Anthropic Claude

```python
import anthropic
from typing import AsyncIterator

class ClaudeClient:
    """Production Claude API client"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    async def complete(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0
    ) -> str:
        """Complete prompt with Claude"""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    async def stream_complete(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 1024
    ) -> AsyncIterator[str]:
        """Stream completion from Claude"""

        with self.client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system or "",
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text

# Usage
client = ClaudeClient(api_key="your-key")
response = await client.complete("Explain RAG systems")

# Streaming
async for chunk in client.stream_complete("Write a story"):
    print(chunk, end="", flush=True)
```

### OpenAI GPT

```python
import openai
from openai import AsyncOpenAI

class GPTClient:
    """Production OpenAI API client"""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int | None = None
    ) -> str:
        """Complete with GPT"""

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    async def complete_with_functions(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, Any]],
        model: str = "gpt-4-turbo-preview"
    ) -> Dict[str, Any]:
        """Complete with function calling"""

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto"
        )

        choice = response.choices[0]

        if choice.finish_reason == "function_call":
            return {
                "type": "function_call",
                "function": choice.message.function_call.name,
                "arguments": choice.message.function_call.arguments
            }
        else:
            return {
                "type": "text",
                "content": choice.message.content
            }

# Usage
client = GPTClient(api_key="your-key")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is RAG?"}
]

response = await client.complete(messages)
```

## Embeddings

### Generating Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    """Embedding generation service"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts"""
        return self.model.encode(texts, show_progress_bar=False)

    def embed_single(self, text: str) -> List[float]:
        """Embed single text"""
        return self.model.encode(text).tolist()

    def similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity"""
        emb1 = self.embed_single(text1)
        emb2 = self.embed_single(text2)

        # Cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        return dot_product / (norm1 * norm2)

# Usage
embedder = EmbeddingService()

# Batch embedding
texts = ["Document 1", "Document 2", "Document 3"]
embeddings = embedder.embed(texts)

# Similarity
similarity = embedder.similarity("Python programming", "Coding in Python")
print(f"Similarity: {similarity:.3f}")
```

### OpenAI Embeddings

```python
import openai

async def get_openai_embedding(text: str) -> List[float]:
    """Get embedding from OpenAI"""
    response = await openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

## Agent Orchestration

### Simple Agent Framework

```python
from typing import List, Callable, Any
from dataclasses import dataclass

@dataclass
class Tool:
    """Agent tool definition"""
    name: str
    description: str
    function: Callable

class Agent:
    """Simple LLM agent with tools"""

    def __init__(
        self,
        llm_client: Any,
        tools: List[Tool],
        system_prompt: str
    ):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = system_prompt

    def get_tool_descriptions(self) -> str:
        """Format tools for LLM"""
        return "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.tools.values()
        ])

    async def run(self, task: str, max_iterations: int = 5) -> str:
        """Run agent on task"""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Task: {task}

Available tools:
{self.get_tool_descriptions()}

Think step by step and use tools as needed."""}
        ]

        for iteration in range(max_iterations):
            # Get LLM response
            response = await self.llm.complete(messages)

            # Check if agent wants to use a tool
            if "USE_TOOL:" in response:
                # Parse tool call
                tool_line = [l for l in response.split("\n") if "USE_TOOL:" in l][0]
                tool_name = tool_line.split("USE_TOOL:")[1].strip()

                if tool_name in self.tools:
                    # Execute tool
                    result = await self.tools[tool_name].function()

                    # Add tool result to conversation
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": f"Tool result: {result}"
                    })
                else:
                    return f"Error: Unknown tool {tool_name}"
            else:
                # Agent is done
                return response

        return "Max iterations reached"

# Example tools
async def search_web(query: str) -> str:
    """Search the web"""
    # Implementation...
    return f"Search results for: {query}"

async def calculate(expression: str) -> str:
    """Calculate math expression"""
    return str(eval(expression))

# Create agent
tools = [
    Tool("search_web", "Search the web for information", search_web),
    Tool("calculate", "Calculate mathematical expressions", calculate)
]

agent = Agent(
    llm_client=claude_client,
    tools=tools,
    system_prompt="You are a helpful assistant with access to tools."
)

# Run
result = await agent.run("What is 25 * 47?")
```

## Cost Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens for text"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(
    prompt: str,
    completion: str,
    model: str = "gpt-4"
) -> float:
    """Estimate cost for request"""

    # Token counts
    prompt_tokens = count_tokens(prompt, model)
    completion_tokens = count_tokens(completion, model)

    # Pricing (as of 2024)
    if model == "gpt-4":
        prompt_cost = prompt_tokens * 0.03 / 1000
        completion_cost = completion_tokens * 0.06 / 1000
    elif model == "gpt-3.5-turbo":
        prompt_cost = prompt_tokens * 0.0015 / 1000
        completion_cost = completion_tokens * 0.002 / 1000
    else:
        return 0.0

    return prompt_cost + completion_cost
```

### Response Caching

```python
import hashlib
import json
from functools import wraps

class LLMCache:
    """Cache for LLM responses"""

    def __init__(self):
        self.cache: Dict[str, str] = {}

    def get_cache_key(
        self,
        prompt: str,
        model: str,
        temperature: float
    ) -> str:
        """Generate cache key"""
        key_data = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature
        }
        return hashlib.sha256(
            json.dumps(key_data, sort_keys=True).encode()
        ).hexdigest()

    def get(self, key: str) -> str | None:
        """Get cached response"""
        return self.cache.get(key)

    def set(self, key: str, value: str) -> None:
        """Cache response"""
        self.cache[key] = value

cache = LLMCache()

def cached_llm_call(func):
    """Decorator for caching LLM calls"""
    @wraps(func)
    async def wrapper(prompt: str, model: str, temperature: float = 0.0, **kwargs):
        # Only cache when temperature = 0 (deterministic)
        if temperature == 0:
            cache_key = cache.get_cache_key(prompt, model, temperature)
            cached_response = cache.get(cache_key)

            if cached_response:
                return cached_response

        # Make actual API call
        response = await func(prompt, model, temperature, **kwargs)

        # Cache if deterministic
        if temperature == 0:
            cache_key = cache.get_cache_key(prompt, model, temperature)
            cache.set(cache_key, response)

        return response

    return wrapper

@cached_llm_call
async def call_llm(prompt: str, model: str, temperature: float) -> str:
    # Actual LLM call
    ...
```

## Error Handling and Rate Limiting

### Retry Logic

```python
import asyncio
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import openai

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(openai.RateLimitError)
)
async def call_llm_with_retry(prompt: str) -> str:
    """Call LLM with automatic retry on rate limit"""
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## Resources

### Templates
- `resources/rag-architecture-patterns.md` - RAG system designs
- `resources/vector-db-configs.json` - Vector DB configurations
- `resources/llm-provider-templates.py` - LLM client templates
- `resources/agent-patterns.md` - Agent orchestration patterns

### Scripts
- `scripts/benchmark-embeddings.py` - Compare embedding models
- `scripts/test-rag-quality.py` - RAG system evaluation
- `scripts/estimate-costs.py` - Cost estimation tool

## Related Skills

- **prompt-engineering**: Crafting effective LLM prompts
- **mcp-development**: MCP servers for AI tools
- **python-development**: Python best practices

## Best Practices Summary

1. **RAG Quality**: Chunk documents properly, tune retrieval
2. **Vector Search**: Choose appropriate embedding model
3. **Prompt Engineering**: Use prompt-engineering skill
4. **Cost Control**: Cache responses, count tokens
5. **Error Handling**: Retry with backoff, handle rate limits
6. **Observability**: Log prompts, responses, costs, latency
7. **Safety**: PII protection, content moderation, injection prevention
8. **Performance**: Batch embeddings, parallel requests
9. **Testing**: Evaluate RAG quality metrics
10. **Caching**: Cache deterministic responses (temperature=0)
