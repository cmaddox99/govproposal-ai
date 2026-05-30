# Vector Databases Guidance

> **Purpose:** Stack-specific agent behaviors for building applications with vector databases (Pinecone, Chroma, Weaviate, pgvector, Qdrant).

---

## Overview

This guidance provides patterns for AI agents working with vector databases for similarity search, RAG systems, and semantic retrieval applications.

---

## Testing Framework

**Primary Framework:** pytest + pytest-asyncio

### Test Structure

```python
import pytest
import numpy as np
from unittest.mock import MagicMock, AsyncMock
from myproject.vectordb.client import VectorDBClient
from myproject.vectordb.indexer import DocumentIndexer
from myproject.search.retriever import SemanticRetriever


class TestVectorDBClient:
    """Tests for vector database client."""

    @pytest.fixture
    def mock_pinecone(self):
        """Mock Pinecone client."""
        mock = MagicMock()
        mock.query.return_value = {
            "matches": [
                {"id": "doc1", "score": 0.95, "metadata": {"text": "content"}},
                {"id": "doc2", "score": 0.87, "metadata": {"text": "content2"}},
            ]
        }
        return mock

    @pytest.fixture
    def client(self, mock_pinecone):
        """Vector DB client with mock."""
        return VectorDBClient(backend=mock_pinecone)

    def test_client_upserts_vectors(self, client, mock_pinecone):
        """Client should upsert vectors correctly."""
        # Arrange
        vectors = [
            {"id": "doc1", "values": [0.1] * 1536, "metadata": {"text": "hello"}},
        ]

        # Act
        client.upsert(vectors)

        # Assert
        mock_pinecone.upsert.assert_called_once()

    def test_client_queries_similar(self, client, mock_pinecone):
        """Client should query for similar vectors."""
        # Arrange
        query_vector = [0.1] * 1536

        # Act
        results = client.query(query_vector, top_k=5)

        # Assert
        assert len(results) == 2
        assert results[0]["score"] > results[1]["score"]

    def test_client_filters_by_metadata(self, client, mock_pinecone):
        """Client should support metadata filtering."""
        # Act
        client.query(
            vector=[0.1] * 1536,
            filter={"category": "technical"}
        )

        # Assert
        call_args = mock_pinecone.query.call_args
        assert "filter" in call_args.kwargs


class TestDocumentIndexer:
    """Tests for document indexing."""

    @pytest.fixture
    def mock_embeddings(self):
        """Mock embedding model."""
        mock = MagicMock()
        mock.embed.return_value = np.random.randn(1536).tolist()
        mock.embed_batch.return_value = [
            np.random.randn(1536).tolist() for _ in range(3)
        ]
        return mock

    @pytest.fixture
    def indexer(self, mock_embeddings, client):
        """Document indexer with mocks."""
        return DocumentIndexer(
            embedding_model=mock_embeddings,
            vector_client=client
        )

    def test_indexer_chunks_documents(self, indexer):
        """Indexer should chunk long documents."""
        # Arrange
        long_doc = "word " * 1000

        # Act
        chunks = indexer._chunk_document(long_doc, chunk_size=100)

        # Assert
        assert len(chunks) > 1
        assert all(len(c.split()) <= 100 for c in chunks)

    def test_indexer_generates_embeddings(self, indexer, mock_embeddings):
        """Indexer should generate embeddings for chunks."""
        # Arrange
        documents = ["doc1 content", "doc2 content"]

        # Act
        indexer.index(documents)

        # Assert
        mock_embeddings.embed_batch.assert_called()

    def test_indexer_preserves_metadata(self, indexer):
        """Indexer should preserve document metadata."""
        # Arrange
        documents = [
            {"content": "text", "metadata": {"source": "file.pdf"}}
        ]

        # Act
        indexed = indexer.index(documents)

        # Assert
        assert all("source" in doc["metadata"] for doc in indexed)


class TestSemanticRetriever:
    """Tests for semantic retrieval."""

    @pytest.fixture
    def retriever(self, client, mock_embeddings):
        """Semantic retriever."""
        return SemanticRetriever(
            vector_client=client,
            embedding_model=mock_embeddings
        )

    def test_retriever_returns_documents(self, retriever):
        """Retriever should return relevant documents."""
        # Act
        results = retriever.retrieve("search query", top_k=5)

        # Assert
        assert len(results) > 0
        assert all("text" in r for r in results)

    def test_retriever_scores_above_threshold(self, retriever):
        """Retriever should filter by score threshold."""
        # Act
        results = retriever.retrieve(
            "query",
            top_k=10,
            score_threshold=0.8
        )

        # Assert
        assert all(r["score"] >= 0.8 for r in results)

    def test_retriever_handles_empty_results(self, retriever, mock_pinecone):
        """Retriever should handle no matches."""
        # Arrange
        mock_pinecone.query.return_value = {"matches": []}

        # Act
        results = retriever.retrieve("obscure query")

        # Assert
        assert results == []
```

---

## Common Patterns

### Good Patterns

**Unified Vector DB Client:**

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Standardized search result."""
    id: str
    score: float
    metadata: Dict
    vector: Optional[List[float]] = None

class VectorDBBackend(ABC):
    """Abstract vector database backend."""

    @abstractmethod
    def upsert(self, vectors: List[Dict]) -> int:
        """Upsert vectors. Returns count."""
        pass

    @abstractmethod
    def query(
        self,
        vector: List[float],
        top_k: int = 10,
        filter: Dict = None
    ) -> List[SearchResult]:
        """Query similar vectors."""
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> int:
        """Delete vectors by ID."""
        pass


class PineconeBackend(VectorDBBackend):
    """Pinecone implementation."""

    def __init__(self, api_key: str, index_name: str, environment: str):
        import pinecone
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)

    def upsert(self, vectors: List[Dict]) -> int:
        formatted = [
            (v["id"], v["values"], v.get("metadata", {}))
            for v in vectors
        ]
        response = self.index.upsert(vectors=formatted)
        return response.upserted_count

    def query(
        self,
        vector: List[float],
        top_k: int = 10,
        filter: Dict = None
    ) -> List[SearchResult]:
        response = self.index.query(
            vector=vector,
            top_k=top_k,
            filter=filter,
            include_metadata=True
        )
        return [
            SearchResult(
                id=m["id"],
                score=m["score"],
                metadata=m.get("metadata", {})
            )
            for m in response["matches"]
        ]

    def delete(self, ids: List[str]) -> int:
        self.index.delete(ids=ids)
        return len(ids)


class ChromaBackend(VectorDBBackend):
    """Chroma implementation."""

    def __init__(self, collection_name: str, persist_dir: str = None):
        import chromadb
        if persist_dir:
            self.client = chromadb.PersistentClient(path=persist_dir)
        else:
            self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)

    def upsert(self, vectors: List[Dict]) -> int:
        self.collection.upsert(
            ids=[v["id"] for v in vectors],
            embeddings=[v["values"] for v in vectors],
            metadatas=[v.get("metadata", {}) for v in vectors]
        )
        return len(vectors)

    def query(
        self,
        vector: List[float],
        top_k: int = 10,
        filter: Dict = None
    ) -> List[SearchResult]:
        results = self.collection.query(
            query_embeddings=[vector],
            n_results=top_k,
            where=filter
        )
        return [
            SearchResult(
                id=results["ids"][0][i],
                score=1 - results["distances"][0][i],  # Convert distance to score
                metadata=results["metadatas"][0][i]
            )
            for i in range(len(results["ids"][0]))
        ]

    def delete(self, ids: List[str]) -> int:
        self.collection.delete(ids=ids)
        return len(ids)
```

**Document Indexer:**

```python
from typing import List, Dict, Optional
import hashlib

class DocumentIndexer:
    """Index documents into vector database."""

    def __init__(
        self,
        embedding_model,
        vector_client: VectorDBBackend,
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        self.embedder = embedding_model
        self.client = vector_client
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def index(
        self,
        documents: List[Dict],
        batch_size: int = 100
    ) -> Dict:
        """Index documents with chunking and batching."""
        all_chunks = []

        # Chunk documents
        for doc in documents:
            content = doc.get("content") or doc.get("text")
            metadata = doc.get("metadata", {})

            chunks = self._chunk_text(content)

            for i, chunk in enumerate(chunks):
                chunk_id = self._generate_id(content, i)
                all_chunks.append({
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })

        # Generate embeddings in batches
        total_indexed = 0
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]

            # Get embeddings
            texts = [c["text"] for c in batch]
            embeddings = self.embedder.embed_batch(texts)

            # Prepare vectors
            vectors = [
                {
                    "id": batch[j]["id"],
                    "values": embeddings[j],
                    "metadata": {
                        **batch[j]["metadata"],
                        "text": batch[j]["text"][:1000]  # Store truncated text
                    }
                }
                for j in range(len(batch))
            ]

            # Upsert
            count = self.client.upsert(vectors)
            total_indexed += count

        return {
            "documents_processed": len(documents),
            "chunks_indexed": total_indexed
        }

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - self.chunk_overlap

        return chunks

    def _generate_id(self, content: str, chunk_index: int) -> str:
        """Generate deterministic chunk ID."""
        hash_input = f"{content[:100]}_{chunk_index}"
        return hashlib.md5(hash_input.encode()).hexdigest()
```

**Hybrid Search:**

```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """Combine semantic and keyword search."""

    def __init__(
        self,
        vector_client: VectorDBBackend,
        embedding_model,
        documents: List[Dict],
        semantic_weight: float = 0.7
    ):
        self.vector_client = vector_client
        self.embedder = embedding_model
        self.semantic_weight = semantic_weight

        # Build BM25 index
        self.documents = documents
        tokenized = [doc["text"].lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Dict]:
        """Hybrid retrieval combining semantic + keyword."""

        # Semantic search
        query_embedding = self.embedder.embed(query)
        semantic_results = self.vector_client.query(
            vector=query_embedding,
            top_k=top_k * 2
        )

        # Keyword search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Normalize scores
        semantic_scores = {r.id: r.score for r in semantic_results}
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1

        # Combine scores
        combined = []
        for i, doc in enumerate(self.documents):
            doc_id = doc.get("id", str(i))

            sem_score = semantic_scores.get(doc_id, 0)
            kw_score = bm25_scores[i] / max_bm25

            combined_score = (
                self.semantic_weight * sem_score +
                (1 - self.semantic_weight) * kw_score
            )

            combined.append({
                "id": doc_id,
                "text": doc["text"],
                "score": combined_score,
                "semantic_score": sem_score,
                "keyword_score": kw_score
            })

        # Sort and return top_k
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:top_k]
```

---

## Anti-Patterns to Avoid

### No Batching

```python
# BAD - One at a time
for doc in documents:
    embedding = embedder.embed(doc)
    client.upsert([{"id": doc.id, "values": embedding}])

# GOOD - Batch operations
embeddings = embedder.embed_batch([d.text for d in documents])
vectors = [{"id": d.id, "values": e} for d, e in zip(documents, embeddings)]
client.upsert(vectors)
```

### Storing Full Text in Metadata

```python
# BAD - Storing huge text in vector metadata
client.upsert([{
    "id": "doc1",
    "values": embedding,
    "metadata": {"full_text": very_long_document}  # May exceed limits
}])

# GOOD - Store reference or truncated
client.upsert([{
    "id": "doc1",
    "values": embedding,
    "metadata": {
        "preview": document[:500],
        "source_path": "s3://bucket/doc1.txt"
    }
}])
```

---

## Tools and Commands

### Development

```bash
# Install clients
pip install pinecone-client chromadb weaviate-client qdrant-client pgvector

# Start local Chroma
chroma run --path ./chroma_data

# Start local Qdrant
docker run -p 6333:6333 qdrant/qdrant
```

### Testing

```bash
# Run unit tests
pytest tests/ -m "not integration"

# Run with real vector DB
pytest tests/integration/ --run-integration
```

---

## Production Checklist

```markdown
## Vector Database Production Checklist

### Index Quality
- [ ] Embedding model validated
- [ ] Chunk size optimized
- [ ] Index populated correctly
- [ ] Metadata schema defined

### Performance
- [ ] Latency meets requirements
- [ ] Batch operations used
- [ ] Caching implemented
- [ ] Connection pooling

### Reliability
- [ ] Index backups configured
- [ ] Failover strategy
- [ ] Rate limiting handled
```
