---
law_id: ENG-4.1
avatar: vector-databases
---

# ENG-4.1: Atomic TDD Examples for Vector Databases

## COMPLIANT: Unit Testing Embedding Generation and Storage

```python
import pytest
import numpy as np
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from vector_store import VectorStore, Document, SearchResult
from embeddings import EmbeddingGenerator, EmbeddingConfig


class TestEmbeddingGenerator:
    """Atomic tests for embedding generation."""

    @pytest.fixture
    def mock_model(self):
        """Provide mock embedding model."""
        mock = Mock()
        # Return deterministic embeddings
        mock.encode.return_value = np.array([
            [0.1, 0.2, 0.3, 0.4],
            [0.5, 0.6, 0.7, 0.8]
        ])
        return mock

    @pytest.fixture
    def generator(self, mock_model):
        """Provide embedding generator with mock model."""
        return EmbeddingGenerator(model=mock_model, dimension=4)

    def test_generate_embedding_returns_correct_dimension(
        self, generator, mock_model
    ):
        """Test that embeddings have expected dimensions."""
        text = "Sample text for embedding"

        embedding = generator.generate(text)

        assert embedding.shape == (4,)

    def test_generate_batch_returns_array_per_text(
        self, generator, mock_model
    ):
        """Test batch embedding generation."""
        texts = ["First text", "Second text"]

        embeddings = generator.generate_batch(texts)

        assert len(embeddings) == 2
        assert all(e.shape == (4,) for e in embeddings)

    def test_embeddings_are_normalized(self, generator, mock_model):
        """Test that embeddings are L2 normalized."""
        mock_model.encode.return_value = np.array([[3.0, 4.0, 0.0, 0.0]])

        embedding = generator.generate("test")

        norm = np.linalg.norm(embedding)
        assert np.isclose(norm, 1.0, atol=1e-6)

    def test_empty_text_returns_zero_vector(self, generator):
        """Test handling of empty text input."""
        embedding = generator.generate("")

        assert embedding.shape == (4,)
        # Implementation should handle empty gracefully

    def test_truncation_for_long_text(self, generator, mock_model):
        """Test that long text is truncated appropriately."""
        long_text = "word " * 10000

        generator.generate(long_text)

        # Should have called encode with truncated text
        call_args = mock_model.encode.call_args[0][0]
        assert len(call_args) <= generator.max_length


class TestVectorStore:
    """Atomic tests for vector store operations."""

    @pytest.fixture
    def vector_store(self, tmp_path):
        """Provide vector store with in-memory backend."""
        return VectorStore(
            backend="memory",
            dimension=4,
            metric="cosine"
        )

    @pytest.fixture
    def sample_documents(self):
        """Provide sample documents for testing."""
        return [
            Document(
                id="doc1",
                content="Python programming language",
                embedding=np.array([0.9, 0.1, 0.1, 0.1]),
                metadata={"category": "programming"}
            ),
            Document(
                id="doc2",
                content="Machine learning with Python",
                embedding=np.array([0.7, 0.5, 0.3, 0.1]),
                metadata={"category": "ml"}
            ),
            Document(
                id="doc3",
                content="Database design patterns",
                embedding=np.array([0.1, 0.1, 0.9, 0.2]),
                metadata={"category": "databases"}
            )
        ]

    def test_add_document_increases_count(
        self, vector_store, sample_documents
    ):
        """Test that adding documents increases store count."""
        initial_count = vector_store.count()

        vector_store.add(sample_documents[0])

        assert vector_store.count() == initial_count + 1

    def test_add_batch_adds_all_documents(
        self, vector_store, sample_documents
    ):
        """Test batch document addition."""
        vector_store.add_batch(sample_documents)

        assert vector_store.count() == len(sample_documents)

    def test_get_by_id_returns_correct_document(
        self, vector_store, sample_documents
    ):
        """Test document retrieval by ID."""
        vector_store.add(sample_documents[0])

        retrieved = vector_store.get("doc1")

        assert retrieved is not None
        assert retrieved.id == "doc1"
        assert retrieved.content == "Python programming language"

    def test_get_by_id_returns_none_for_missing(self, vector_store):
        """Test retrieval of non-existent document."""
        result = vector_store.get("nonexistent")

        assert result is None

    def test_delete_removes_document(
        self, vector_store, sample_documents
    ):
        """Test document deletion."""
        vector_store.add(sample_documents[0])

        vector_store.delete("doc1")

        assert vector_store.get("doc1") is None
        assert vector_store.count() == 0

    def test_update_replaces_document(
        self, vector_store, sample_documents
    ):
        """Test document update."""
        vector_store.add(sample_documents[0])

        updated_doc = Document(
            id="doc1",
            content="Updated Python content",
            embedding=np.array([0.5, 0.5, 0.5, 0.5]),
            metadata={"category": "updated"}
        )
        vector_store.update(updated_doc)

        retrieved = vector_store.get("doc1")
        assert retrieved.content == "Updated Python content"
        assert retrieved.metadata["category"] == "updated"


class TestVectorSearch:
    """Atomic tests for vector similarity search."""

    @pytest.fixture
    def populated_store(self, tmp_path):
        """Provide vector store with test data."""
        store = VectorStore(backend="memory", dimension=4, metric="cosine")

        documents = [
            Document(
                id="python",
                content="Python programming",
                embedding=np.array([1.0, 0.0, 0.0, 0.0]),
                metadata={}
            ),
            Document(
                id="java",
                content="Java programming",
                embedding=np.array([0.9, 0.1, 0.0, 0.0]),
                metadata={}
            ),
            Document(
                id="databases",
                content="Database systems",
                embedding=np.array([0.0, 0.0, 1.0, 0.0]),
                metadata={}
            )
        ]
        store.add_batch(documents)
        return store

    def test_search_returns_k_results(self, populated_store):
        """Test that search returns requested number of results."""
        query_embedding = np.array([0.9, 0.1, 0.0, 0.0])

        results = populated_store.search(query_embedding, k=2)

        assert len(results) == 2

    def test_search_returns_results_in_similarity_order(
        self, populated_store
    ):
        """Test that results are ordered by similarity."""
        query_embedding = np.array([1.0, 0.0, 0.0, 0.0])

        results = populated_store.search(query_embedding, k=3)

        # First result should be most similar (python)
        assert results[0].document.id == "python"
        # Scores should be descending
        assert all(
            results[i].score >= results[i + 1].score
            for i in range(len(results) - 1)
        )

    def test_search_scores_are_in_valid_range(self, populated_store):
        """Test that similarity scores are valid for cosine metric."""
        query_embedding = np.array([0.5, 0.5, 0.5, 0.5])

        results = populated_store.search(query_embedding, k=3)

        # Cosine similarity should be in [-1, 1]
        for result in results:
            assert -1.0 <= result.score <= 1.0

    def test_search_with_filter_returns_matching_documents(
        self, populated_store
    ):
        """Test metadata filtering in search."""
        # Add documents with metadata
        populated_store.add(Document(
            id="ml_python",
            content="ML with Python",
            embedding=np.array([0.8, 0.2, 0.0, 0.0]),
            metadata={"topic": "ml"}
        ))

        query_embedding = np.array([1.0, 0.0, 0.0, 0.0])
        results = populated_store.search(
            query_embedding,
            k=10,
            filter={"topic": "ml"}
        )

        assert all(r.document.metadata.get("topic") == "ml" for r in results)

    def test_search_with_threshold_filters_low_scores(
        self, populated_store
    ):
        """Test score threshold filtering."""
        query_embedding = np.array([1.0, 0.0, 0.0, 0.0])

        results = populated_store.search(
            query_embedding,
            k=10,
            score_threshold=0.8
        )

        assert all(r.score >= 0.8 for r in results)


class TestEmbeddingIndexOperations:
    """Atomic tests for index management operations."""

    @pytest.fixture
    def vector_store(self):
        """Provide vector store for index testing."""
        return VectorStore(backend="memory", dimension=4, metric="cosine")

    def test_create_index_succeeds(self, vector_store):
        """Test index creation."""
        result = vector_store.create_index(index_type="hnsw", m=16, ef=100)

        assert result.success is True

    def test_index_improves_search_after_bulk_add(self, vector_store):
        """Test that indexing works after bulk document addition."""
        # Add many documents
        documents = [
            Document(
                id=f"doc_{i}",
                content=f"Document {i}",
                embedding=np.random.rand(4),
                metadata={}
            )
            for i in range(100)
        ]
        vector_store.add_batch(documents)

        # Create index
        vector_store.create_index(index_type="hnsw")

        # Search should still work
        query = np.random.rand(4)
        results = vector_store.search(query, k=5)

        assert len(results) == 5

    def test_index_stats_returns_correct_information(self, vector_store):
        """Test index statistics retrieval."""
        vector_store.add(Document(
            id="test",
            content="test",
            embedding=np.array([0.1, 0.2, 0.3, 0.4]),
            metadata={}
        ))
        vector_store.create_index(index_type="flat")

        stats = vector_store.get_index_stats()

        assert "index_type" in stats
        assert "vector_count" in stats
        assert stats["vector_count"] == 1
```

**Why compliant:** Each test verifies a single vector store operation. Mock embedding models provide deterministic outputs. Tests use in-memory backends for speed and isolation. Search behavior (ordering, filtering, thresholds) is tested separately. Index operations are tested independently from search logic.

---

## VIOLATION: Testing Vector Operations with Real Services

```python
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer


def test_vector_search():
    """Test vector search with real services - not atomic."""
    # Real embedding model - slow to load
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Real Pinecone connection - external dependency
    pc = Pinecone(api_key="real-api-key")
    index = pc.Index("production-index")

    # Generate real embeddings - slow
    query = "What is machine learning?"
    query_embedding = model.encode(query).tolist()

    # Real search against production index
    results = index.query(
        vector=query_embedding,
        top_k=10,
        include_metadata=True
    )

    # Vague assertions
    assert len(results["matches"]) > 0
    assert results["matches"][0]["score"] > 0.5


def test_full_rag_pipeline():
    """Test complete RAG pipeline - too many concerns."""
    # Real embedding model
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Real vector database
    import chromadb
    client = chromadb.Client()
    collection = client.create_collection("test")

    # Load real documents
    with open("documents.json") as f:
        documents = json.load(f)

    # Add documents (slow - generates embeddings)
    collection.add(
        documents=[d["content"] for d in documents],
        ids=[d["id"] for d in documents]
    )

    # Search
    results = collection.query(
        query_texts=["machine learning"],
        n_results=5
    )

    # Multiple assertions
    assert len(results["documents"][0]) == 5
    assert all("machine" in doc.lower() for doc in results["documents"][0])
```

**Why violates ENG-4.1:** Tests use real embedding models which are slow to load. Connection to production Pinecone index creates external dependency. Real embedding generation is computationally expensive. Tests depend on current state of external vector database. File system dependency for documents. Multiple operations combined in single test.

---

## COMPLIANT: Testing Retrieval Quality Metrics

```python
import pytest
import numpy as np
from typing import List, Tuple

from retrieval_metrics import (
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_mrr,
    calculate_ndcg,
    RetrievalEvaluator
)


class TestPrecisionAtK:
    """Atomic tests for precision@k metric."""

    def test_precision_at_k_with_all_relevant(self):
        """Test precision when all retrieved are relevant."""
        retrieved_ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        relevant_ids = {"doc1", "doc2", "doc3", "doc4", "doc5"}

        precision = calculate_precision_at_k(retrieved_ids, relevant_ids, k=5)

        assert precision == 1.0

    def test_precision_at_k_with_none_relevant(self):
        """Test precision when no retrieved are relevant."""
        retrieved_ids = ["doc1", "doc2", "doc3"]
        relevant_ids = {"doc4", "doc5", "doc6"}

        precision = calculate_precision_at_k(retrieved_ids, relevant_ids, k=3)

        assert precision == 0.0

    def test_precision_at_k_with_partial_relevant(self):
        """Test precision with mix of relevant and irrelevant."""
        retrieved_ids = ["doc1", "doc2", "doc3", "doc4"]
        relevant_ids = {"doc1", "doc3"}

        precision = calculate_precision_at_k(retrieved_ids, relevant_ids, k=4)

        assert precision == 0.5  # 2 relevant out of 4

    def test_precision_at_k_considers_only_top_k(self):
        """Test that only top k results are considered."""
        retrieved_ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        relevant_ids = {"doc1", "doc5"}

        precision = calculate_precision_at_k(retrieved_ids, relevant_ids, k=3)

        # Only doc1 is relevant in top 3
        assert precision == pytest.approx(1/3)


class TestRecallAtK:
    """Atomic tests for recall@k metric."""

    def test_recall_at_k_with_all_retrieved(self):
        """Test recall when all relevant are retrieved."""
        retrieved_ids = ["doc1", "doc2", "doc3"]
        relevant_ids = {"doc1", "doc2", "doc3"}

        recall = calculate_recall_at_k(retrieved_ids, relevant_ids, k=3)

        assert recall == 1.0

    def test_recall_at_k_with_partial_retrieval(self):
        """Test recall when some relevant are retrieved."""
        retrieved_ids = ["doc1", "doc2"]
        relevant_ids = {"doc1", "doc2", "doc3", "doc4"}

        recall = calculate_recall_at_k(retrieved_ids, relevant_ids, k=2)

        assert recall == 0.5  # 2 retrieved out of 4 relevant

    def test_recall_at_k_handles_empty_relevant(self):
        """Test recall when no relevant documents exist."""
        retrieved_ids = ["doc1", "doc2"]
        relevant_ids = set()

        recall = calculate_recall_at_k(retrieved_ids, relevant_ids, k=2)

        # Edge case: defined as 0 or 1 depending on implementation
        assert recall in [0.0, 1.0]


class TestMRR:
    """Atomic tests for Mean Reciprocal Rank."""

    def test_mrr_with_first_position_relevant(self):
        """Test MRR when first result is relevant."""
        retrieved_ids = ["doc1", "doc2", "doc3"]
        relevant_ids = {"doc1"}

        mrr = calculate_mrr(retrieved_ids, relevant_ids)

        assert mrr == 1.0  # 1/1

    def test_mrr_with_second_position_relevant(self):
        """Test MRR when second result is first relevant."""
        retrieved_ids = ["doc1", "doc2", "doc3"]
        relevant_ids = {"doc2"}

        mrr = calculate_mrr(retrieved_ids, relevant_ids)

        assert mrr == 0.5  # 1/2

    def test_mrr_with_no_relevant_in_results(self):
        """Test MRR when no relevant results."""
        retrieved_ids = ["doc1", "doc2", "doc3"]
        relevant_ids = {"doc4"}

        mrr = calculate_mrr(retrieved_ids, relevant_ids)

        assert mrr == 0.0


class TestNDCG:
    """Atomic tests for Normalized Discounted Cumulative Gain."""

    def test_ndcg_with_perfect_ranking(self):
        """Test NDCG with ideal ranking."""
        # Relevance scores in ideal order
        relevance_scores = [3, 2, 1, 0]

        ndcg = calculate_ndcg(relevance_scores, k=4)

        assert ndcg == 1.0

    def test_ndcg_with_reversed_ranking(self):
        """Test NDCG with worst ranking."""
        # Relevance scores in reverse order
        relevance_scores = [0, 1, 2, 3]

        ndcg = calculate_ndcg(relevance_scores, k=4)

        assert ndcg < 1.0

    def test_ndcg_considers_position_discount(self):
        """Test that NDCG discounts by position."""
        # Same relevance but different positions
        scores_high_first = [3, 0, 0, 0]
        scores_high_last = [0, 0, 0, 3]

        ndcg_first = calculate_ndcg(scores_high_first, k=4)
        ndcg_last = calculate_ndcg(scores_high_last, k=4)

        assert ndcg_first > ndcg_last


class TestRetrievalEvaluator:
    """Atomic tests for retrieval evaluation pipeline."""

    @pytest.fixture
    def evaluator(self):
        """Provide retrieval evaluator."""
        return RetrievalEvaluator()

    @pytest.fixture
    def sample_queries(self):
        """Provide sample queries with ground truth."""
        return [
            {
                "query_id": "q1",
                "retrieved": ["doc1", "doc2", "doc3"],
                "relevant": {"doc1", "doc3"}
            },
            {
                "query_id": "q2",
                "retrieved": ["doc4", "doc5", "doc6"],
                "relevant": {"doc4", "doc5", "doc6"}
            }
        ]

    def test_evaluate_batch_returns_metrics_per_query(
        self, evaluator, sample_queries
    ):
        """Test batch evaluation returns per-query metrics."""
        results = evaluator.evaluate_batch(sample_queries)

        assert len(results) == len(sample_queries)
        assert all("precision@3" in r for r in results)
        assert all("recall@3" in r for r in results)

    def test_compute_aggregate_metrics(
        self, evaluator, sample_queries
    ):
        """Test aggregate metric computation."""
        results = evaluator.evaluate_batch(sample_queries)
        aggregates = evaluator.compute_aggregates(results)

        assert "mean_precision@3" in aggregates
        assert "mean_recall@3" in aggregates
        assert "mean_mrr" in aggregates
```

**Why compliant:** Each test verifies a single retrieval metric. Test data is deterministic with known expected values. Edge cases (empty sets, perfect/worst rankings) are tested separately. Metrics are tested independently from vector search implementation. Aggregate statistics are tested separately from individual metrics.

---

## VIOLATION: Testing Metrics with Real Retrieval

```python
def test_retrieval_quality():
    """Test retrieval quality with real system - not atomic."""
    from sentence_transformers import SentenceTransformer
    import chromadb

    # Real model and database
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.Client()
    collection = client.create_collection("test")

    # Load real test dataset
    with open("test_queries.json") as f:
        test_data = json.load(f)

    # Index documents
    for doc in test_data["documents"]:
        collection.add(
            documents=[doc["content"]],
            ids=[doc["id"]]
        )

    # Run queries and compute metrics
    all_precisions = []
    for query in test_data["queries"]:
        results = collection.query(
            query_texts=[query["text"]],
            n_results=10
        )

        # Calculate precision
        retrieved = results["ids"][0]
        relevant = set(query["relevant_ids"])
        precision = len(set(retrieved) & relevant) / len(retrieved)
        all_precisions.append(precision)

    mean_precision = sum(all_precisions) / len(all_precisions)

    # Vague threshold
    assert mean_precision > 0.5
```

**Why violates ENG-4.1:** Uses real embedding model and vector database. Depends on external test data file. Combines indexing, retrieval, and metric calculation. Performance threshold doesn't test metric calculation correctness. Single test covers multiple concerns (indexing, search, metrics).

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/vectordb/test_client.py::test_search_returns_nearest_neighbors -v

# GREEN: Write code, run test again
pytest tests/vectordb/test_client.py::test_search_returns_nearest_neighbors -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add vector search to VectorDBClient"
```
