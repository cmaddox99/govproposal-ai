---
skill:
  id: skill-22-rag-architecture
  name: RAG Architecture
  category: ai-development
  version: "2.0.0"

laws:
  implements:
    - id: ENG-2.1
      title: Domain-Driven Design Law
    - id: BUS-3.1
      title: Data Classification Law
  references:
    - id: BUS-4.1
      title: GDPR Compliance Law
    - id: ENG-6.4
      title: Data Protection Law

triggers:
  phrases:
    - "Build RAG system"
    - "Knowledge retrieval"
    - "Vector database"
    - "Ground LLM responses"

followed_by:
  - skill-21-prompt-engineering
  - skill-24-ai-safety
---

# Skill: RAG Architecture

> **Purpose:** Design and implement Retrieval-Augmented Generation systems that provide accurate, grounded, and up-to-date AI responses.

---

## Purpose

RAG Architecture is the practice of combining retrieval systems with generative AI to produce responses grounded in specific knowledge. This skill ensures:

1. **Accuracy** - Responses grounded in source documents
2. **Freshness** - Access to up-to-date information
3. **Traceability** - Answers linked to sources
4. **Reliability** - Reduced hallucinations
5. **Scalability** - Handle large knowledge bases efficiently

**Key principle:** The best answer combines retrieved facts with generated fluency.

---

## When to Invoke

Invoke this skill when:

- Building knowledge-based Q&A systems
- Creating documentation assistants
- Implementing enterprise search with AI
- Reducing hallucinations in LLM applications
- Integrating proprietary data with LLMs
- Building chatbots that need factual accuracy

**Trigger phrases:**
- "The model doesn't know our internal docs"
- "How do we ground answers in our data?"
- "We need accurate answers from our knowledge base"
- "The responses need citations"
- "Build a chat interface for our documentation"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: RAG architecture appropriate to needs
- **Article IV, Section 4.1** - Test-First: Retrieval quality tested
- **Article VI, Section 6.1** - Observability: Retrieval metrics tracked

### Product Constitution
- **Article V, Section 5.1** - User Experience: Accurate, helpful responses

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: Sources traceable
- **Article II, Section 2.1** - Business Rules: Responses comply with policy

---

## RAG Architecture Overview

### Basic RAG Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│   │ INGEST  │───▶│  EMBED &    │───▶│     VECTOR STORE        │ │
│   │         │    │   INDEX     │    │                         │ │
│   └─────────┘    └─────────────┘    └───────────┬─────────────┘ │
│                                                   │               │
│                                                   │ retrieve      │
│                                                   ▼               │
│   ┌─────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│   │  USER   │───▶│   EMBED     │───▶│      RETRIEVER          │ │
│   │  QUERY  │    │   QUERY     │    │                         │ │
│   └─────────┘    └─────────────┘    └───────────┬─────────────┘ │
│                                                   │               │
│                                                   │ context       │
│                                                   ▼               │
│                                     ┌─────────────────────────┐ │
│                                     │       GENERATOR         │ │
│                                     │    (LLM + Context)      │ │
│                                     └───────────┬─────────────┘ │
│                                                   │               │
│                                                   ▼               │
│                                     ┌─────────────────────────┐ │
│                                     │       RESPONSE          │ │
│                                     │    (with citations)     │ │
│                                     └─────────────────────────┘ │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Document Processing

### Chunking Strategies

```python
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Chunk:
    content: str
    metadata: dict
    chunk_id: str
    source_id: str

class DocumentChunker:
    """Split documents into retrievable chunks."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        strategy: str = "recursive"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy

    def chunk(self, document: str, metadata: dict = None) -> List[Chunk]:
        """Chunk document based on strategy."""
        if self.strategy == "fixed":
            return self._fixed_size_chunk(document, metadata)
        elif self.strategy == "recursive":
            return self._recursive_chunk(document, metadata)
        elif self.strategy == "semantic":
            return self._semantic_chunk(document, metadata)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _fixed_size_chunk(self, document: str, metadata: dict) -> List[Chunk]:
        """Simple fixed-size chunking with overlap."""
        chunks = []
        start = 0

        while start < len(document):
            end = start + self.chunk_size
            chunk_text = document[start:end]

            chunks.append(Chunk(
                content=chunk_text,
                metadata=metadata or {},
                chunk_id=f"chunk_{len(chunks)}",
                source_id=metadata.get("source_id", "unknown")
            ))

            start = end - self.chunk_overlap

        return chunks

    def _recursive_chunk(self, document: str, metadata: dict) -> List[Chunk]:
        """Recursive chunking respecting document structure."""
        # Split hierarchy: paragraphs -> sentences -> words
        separators = ["\n\n", "\n", ". ", " "]
        return self._recursive_split(document, separators, metadata)

    def _recursive_split(
        self,
        text: str,
        separators: List[str],
        metadata: dict
    ) -> List[Chunk]:
        """Recursively split text."""
        if len(text) <= self.chunk_size:
            return [Chunk(
                content=text,
                metadata=metadata or {},
                chunk_id=f"chunk_{hash(text) % 10000}",
                source_id=metadata.get("source_id", "unknown")
            )]

        separator = separators[0] if separators else ""
        remaining_separators = separators[1:] if len(separators) > 1 else []

        splits = text.split(separator)
        chunks = []
        current_chunk = ""

        for split in splits:
            if len(current_chunk) + len(split) + len(separator) <= self.chunk_size:
                current_chunk += (separator if current_chunk else "") + split
            else:
                if current_chunk:
                    chunks.extend(
                        self._recursive_split(current_chunk, remaining_separators, metadata)
                    )
                current_chunk = split

        if current_chunk:
            chunks.extend(
                self._recursive_split(current_chunk, remaining_separators, metadata)
            )

        return chunks

    def _semantic_chunk(self, document: str, metadata: dict) -> List[Chunk]:
        """Chunk based on semantic similarity."""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', document)

        # Get embeddings for each sentence
        embeddings = [get_embedding(s) for s in sentences]

        # Group sentences with similar embeddings
        chunks = []
        current_chunk = []
        current_embedding = None

        for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
            if current_embedding is None:
                current_chunk.append(sentence)
                current_embedding = embedding
            elif cosine_similarity(current_embedding, embedding) > 0.8:
                current_chunk.append(sentence)
                # Update centroid
                current_embedding = average_embeddings([current_embedding, embedding])
            else:
                # Start new chunk
                chunks.append(Chunk(
                    content=" ".join(current_chunk),
                    metadata=metadata or {},
                    chunk_id=f"chunk_{len(chunks)}",
                    source_id=metadata.get("source_id", "unknown")
                ))
                current_chunk = [sentence]
                current_embedding = embedding

        if current_chunk:
            chunks.append(Chunk(
                content=" ".join(current_chunk),
                metadata=metadata or {},
                chunk_id=f"chunk_{len(chunks)}",
                source_id=metadata.get("source_id", "unknown")
            ))

        return chunks
```

### Document Loaders

```python
from abc import ABC, abstractmethod
from pathlib import Path
import json

class DocumentLoader(ABC):
    """Base class for document loaders."""

    @abstractmethod
    def load(self, source: str) -> List[dict]:
        """Load documents from source."""
        pass

class PDFLoader(DocumentLoader):
    """Load PDF documents."""

    def load(self, file_path: str) -> List[dict]:
        import fitz  # PyMuPDF

        documents = []
        pdf = fitz.open(file_path)

        for page_num, page in enumerate(pdf):
            text = page.get_text()
            documents.append({
                "content": text,
                "metadata": {
                    "source": file_path,
                    "page": page_num + 1,
                    "type": "pdf"
                }
            })

        return documents

class MarkdownLoader(DocumentLoader):
    """Load Markdown documents with structure preservation."""

    def load(self, file_path: str) -> List[dict]:
        with open(file_path, 'r') as f:
            content = f.read()

        # Split by headers
        sections = re.split(r'^(#{1,6}\s+.+)$', content, flags=re.MULTILINE)

        documents = []
        current_header = ""

        for i, section in enumerate(sections):
            if section.startswith('#'):
                current_header = section.strip()
            elif section.strip():
                documents.append({
                    "content": section.strip(),
                    "metadata": {
                        "source": file_path,
                        "header": current_header,
                        "type": "markdown"
                    }
                })

        return documents

class WebLoader(DocumentLoader):
    """Load web pages."""

    def load(self, url: str) -> List[dict]:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()

        return [{
            "content": text,
            "metadata": {
                "source": url,
                "type": "web",
                "title": soup.title.string if soup.title else ""
            }
        }]
```

---

## Vector Store

### Embedding and Indexing

```python
from typing import List, Optional
import numpy as np

class VectorStore:
    """Store and retrieve document embeddings."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        similarity_metric: str = "cosine"
    ):
        self.embedding_model = embedding_model
        self.similarity_metric = similarity_metric
        self.documents = []
        self.embeddings = []

    def add_documents(self, chunks: List[Chunk]):
        """Add documents to the store."""
        for chunk in chunks:
            embedding = self._embed(chunk.content)
            self.documents.append(chunk)
            self.embeddings.append(embedding)

    def _embed(self, text: str) -> np.ndarray:
        """Generate embedding for text."""
        # Using OpenAI embeddings
        from openai import OpenAI
        client = OpenAI()

        response = client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return np.array(response.data[0].embedding)

    def search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: dict = None
    ) -> List[tuple[Chunk, float]]:
        """Search for similar documents."""
        query_embedding = self._embed(query)

        # Calculate similarities
        similarities = []
        for i, (doc, emb) in enumerate(zip(self.documents, self.embeddings)):
            # Apply metadata filter
            if filter_metadata:
                if not all(doc.metadata.get(k) == v for k, v in filter_metadata.items()):
                    continue

            similarity = self._similarity(query_embedding, emb)
            similarities.append((doc, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:k]

    def _similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate similarity between embeddings."""
        if self.similarity_metric == "cosine":
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        elif self.similarity_metric == "euclidean":
            return -np.linalg.norm(a - b)  # Negative because lower is more similar
        else:
            raise ValueError(f"Unknown metric: {self.similarity_metric}")
```

### Production Vector Stores

```python
# Pinecone integration
import pinecone

class PineconeStore:
    """Production vector store using Pinecone."""

    def __init__(self, index_name: str, api_key: str, environment: str):
        pinecone.init(api_key=api_key, environment=environment)

        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric="cosine"
            )

        self.index = pinecone.Index(index_name)

    def upsert(self, chunks: List[Chunk], embeddings: List[np.ndarray]):
        """Upsert vectors to Pinecone."""
        vectors = [
            (chunk.chunk_id, emb.tolist(), chunk.metadata)
            for chunk, emb in zip(chunks, embeddings)
        ]
        self.index.upsert(vectors=vectors)

    def query(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        filter: dict = None
    ) -> List[dict]:
        """Query similar vectors."""
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            filter=filter,
            include_metadata=True
        )
        return results.matches


# Chroma integration
import chromadb

class ChromaStore:
    """Local vector store using Chroma."""

    def __init__(self, collection_name: str, persist_directory: str = None):
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, chunks: List[Chunk], embeddings: List[np.ndarray]):
        """Add documents to collection."""
        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            embeddings=[e.tolist() for e in embeddings],
            documents=[c.content for c in chunks],
            metadatas=[c.metadata for c in chunks]
        )

    def query(
        self,
        query_embedding: np.ndarray,
        n_results: int = 5,
        where: dict = None
    ) -> dict:
        """Query collection."""
        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
```

---

## Retrieval Strategies

### Hybrid Search

```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """Combine semantic and keyword search."""

    def __init__(
        self,
        vector_store: VectorStore,
        semantic_weight: float = 0.7
    ):
        self.vector_store = vector_store
        self.semantic_weight = semantic_weight
        self.keyword_weight = 1 - semantic_weight

        # Build BM25 index
        tokenized_docs = [
            doc.content.lower().split()
            for doc in vector_store.documents
        ]
        self.bm25 = BM25Okapi(tokenized_docs)

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        """Hybrid retrieval combining semantic and keyword search."""

        # Semantic search
        semantic_results = self.vector_store.search(query, k=k*2)
        semantic_scores = {
            chunk.chunk_id: score
            for chunk, score in semantic_results
        }

        # Keyword search (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Normalize BM25 scores
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        bm25_normalized = bm25_scores / max_bm25

        # Combine scores
        combined_scores = []
        for i, doc in enumerate(self.vector_store.documents):
            semantic_score = semantic_scores.get(doc.chunk_id, 0)
            keyword_score = bm25_normalized[i]

            combined = (
                self.semantic_weight * semantic_score +
                self.keyword_weight * keyword_score
            )
            combined_scores.append((doc, combined))

        # Sort and return top k
        combined_scores.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in combined_scores[:k]]
```

### Re-Ranking

```python
class ReRanker:
    """Re-rank retrieved documents for better relevance."""

    def __init__(self, model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model)

    def rerank(
        self,
        query: str,
        documents: List[Chunk],
        top_k: int = 5
    ) -> List[Chunk]:
        """Re-rank documents using cross-encoder."""

        # Score each document
        pairs = [(query, doc.content) for doc in documents]
        scores = self.model.predict(pairs)

        # Sort by score
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in scored_docs[:top_k]]
```

### Multi-Query Retrieval

```python
class MultiQueryRetriever:
    """Generate multiple query variations for better recall."""

    def __init__(self, vector_store: VectorStore, llm_client):
        self.vector_store = vector_store
        self.llm = llm_client

    async def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        """Retrieve using multiple query variations."""

        # Generate query variations
        variations = await self._generate_variations(query)

        # Retrieve for each variation
        all_results = set()

        for variation in [query] + variations:
            results = self.vector_store.search(variation, k=k)
            for doc, _ in results:
                all_results.add(doc)

        # Re-rank combined results
        reranker = ReRanker()
        return reranker.rerank(query, list(all_results), top_k=k)

    async def _generate_variations(self, query: str) -> List[str]:
        """Generate query variations using LLM."""

        prompt = f"""Generate 3 alternative phrasings of this search query.
Each variation should capture the same intent but use different words.

Original query: {query}

Return only the 3 variations, one per line:"""

        response = await self.llm.complete(prompt)
        return response.strip().split('\n')[:3]
```

---

## Generation with Context

### RAG Prompt Template

```python
RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.

Guidelines:
- Only answer based on the provided context
- If the context doesn't contain the answer, say "I don't have enough information to answer that"
- Cite your sources using [Source: X] format
- Be concise and direct"""

RAG_USER_TEMPLATE = """Context:
{context}

Question: {question}

Answer based on the context above. Include citations."""

class RAGGenerator:
    """Generate responses using retrieved context."""

    def __init__(self, llm_client, system_prompt: str = None):
        self.llm = llm_client
        self.system_prompt = system_prompt or RAG_SYSTEM_PROMPT

    async def generate(
        self,
        question: str,
        retrieved_docs: List[Chunk],
        max_context_tokens: int = 3000
    ) -> dict:
        """Generate answer with citations."""

        # Format context with source identifiers
        context_parts = []
        sources = []

        for i, doc in enumerate(retrieved_docs):
            source_id = f"Source {i+1}"
            context_parts.append(f"[{source_id}]\n{doc.content}")
            sources.append({
                "id": source_id,
                "content": doc.content[:200] + "...",
                "metadata": doc.metadata
            })

        context = "\n\n".join(context_parts)

        # Truncate if needed
        context = self._truncate_context(context, max_context_tokens)

        # Generate response
        response = await self.llm.chat([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": RAG_USER_TEMPLATE.format(
                context=context,
                question=question
            )}
        ])

        return {
            "answer": response,
            "sources": sources,
            "context_used": context
        }

    def _truncate_context(self, context: str, max_tokens: int) -> str:
        """Truncate context to fit token budget."""
        # Rough estimation: 4 chars per token
        max_chars = max_tokens * 4

        if len(context) <= max_chars:
            return context

        return context[:max_chars] + "\n\n[Context truncated...]"
```

---

## Complete RAG Pipeline

```python
class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(self, config: dict):
        self.chunker = DocumentChunker(
            chunk_size=config.get("chunk_size", 512),
            chunk_overlap=config.get("chunk_overlap", 50)
        )
        self.vector_store = VectorStore(
            embedding_model=config.get("embedding_model", "text-embedding-3-small")
        )
        self.retriever = HybridRetriever(self.vector_store)
        self.reranker = ReRanker()
        self.generator = RAGGenerator(config["llm_client"])

    def ingest(self, documents: List[dict]):
        """Ingest documents into the pipeline."""
        all_chunks = []

        for doc in documents:
            chunks = self.chunker.chunk(doc["content"], doc.get("metadata"))
            all_chunks.extend(chunks)

        self.vector_store.add_documents(all_chunks)

        return len(all_chunks)

    async def query(
        self,
        question: str,
        k: int = 5,
        rerank: bool = True
    ) -> dict:
        """Query the RAG pipeline."""

        # Retrieve
        retrieved = self.retriever.retrieve(question, k=k*2 if rerank else k)

        # Re-rank
        if rerank:
            retrieved = self.reranker.rerank(question, retrieved, top_k=k)

        # Generate
        result = await self.generator.generate(question, retrieved)

        return result
```

---

## Good Examples

### Example 1: Production RAG Configuration

```python
RAG_CONFIG = {
    # Chunking
    "chunk_size": 512,
    "chunk_overlap": 50,
    "chunking_strategy": "recursive",

    # Embedding
    "embedding_model": "text-embedding-3-small",
    "embedding_batch_size": 100,

    # Retrieval
    "retrieval_k": 10,
    "rerank_k": 5,
    "hybrid_semantic_weight": 0.7,

    # Generation
    "max_context_tokens": 4000,
    "temperature": 0.1,  # Low for factual responses
    "model": "gpt-4",

    # Quality
    "min_relevance_score": 0.7,
    "require_citations": True
}
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Chunking Strategy

```python
# BAD - Entire documents as single chunks
chunks = [Chunk(content=entire_document, ...)]
# Results in poor retrieval and context overflow
```

**Correct approach:** Appropriate chunking with overlap.

---

### Anti-Pattern 2: No Source Attribution

```python
# BAD - No way to verify answers
def generate(question, context):
    return llm.complete(f"Answer: {question}\nContext: {context}")
    # User can't verify where info came from
```

**Correct approach:** Include citations and return sources.

---

## Quality Checklist

Before deploying RAG system:

### Ingestion
- [ ] Documents properly chunked
- [ ] Metadata preserved
- [ ] Embeddings generated and indexed
- [ ] Incremental updates supported

### Retrieval
- [ ] Relevance tested on sample queries
- [ ] Hybrid search implemented (if needed)
- [ ] Re-ranking improves results
- [ ] Latency acceptable

### Generation
- [ ] Responses grounded in context
- [ ] Citations included
- [ ] Hallucinations minimized
- [ ] "Don't know" responses when appropriate

### Operations
- [ ] Metrics tracked (retrieval quality, latency)
- [ ] Index updates automated
- [ ] Error handling robust

---

## Skill Interactions

### Preceded By
- **21-Prompt Engineering** - Prompts for RAG generation
- **15-Data Modeling** - Document metadata schema

### Followed By
- **23-AI Agents** - RAG as agent tool
- **24-AI Safety** - Safe RAG responses

### Related Skills
- **13-Observability** - RAG metrics and logging
- **19-Model Serving** - Serving RAG endpoints
