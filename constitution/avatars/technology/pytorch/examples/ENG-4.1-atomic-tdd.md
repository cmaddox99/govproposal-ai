---
law_id: ENG-4.1
avatar: pytorch
---

# ENG-4.1: Atomic TDD Examples for PyTorch

## COMPLIANT: Unit Testing Neural Network Layer Forward Pass

```python
import pytest
import torch
import torch.nn as nn
from models.attention import MultiHeadAttention
from models.layers import ResidualBlock, PositionalEncoding


class TestMultiHeadAttention:
    """Atomic tests for multi-head attention layer."""

    @pytest.fixture
    def attention_layer(self):
        """Provide configured attention layer."""
        return MultiHeadAttention(
            embed_dim=512,
            num_heads=8,
            dropout=0.0  # Disable dropout for deterministic tests
        )

    @pytest.fixture
    def sample_input(self):
        """Provide sample input tensors."""
        batch_size = 4
        seq_len = 16
        embed_dim = 512
        return torch.randn(batch_size, seq_len, embed_dim)

    def test_forward_output_shape_matches_input(
        self, attention_layer, sample_input
    ):
        """Test that attention output has same shape as input."""
        output, _ = attention_layer(sample_input, sample_input, sample_input)

        assert output.shape == sample_input.shape

    def test_forward_returns_attention_weights(
        self, attention_layer, sample_input
    ):
        """Test that attention weights are returned correctly."""
        _, attention_weights = attention_layer(
            sample_input, sample_input, sample_input
        )

        batch_size, seq_len, _ = sample_input.shape
        num_heads = attention_layer.num_heads

        assert attention_weights.shape == (batch_size, num_heads, seq_len, seq_len)

    def test_attention_weights_sum_to_one(
        self, attention_layer, sample_input
    ):
        """Test that attention weights are valid probability distributions."""
        _, attention_weights = attention_layer(
            sample_input, sample_input, sample_input
        )

        # Sum over last dimension (key positions) should equal 1
        weight_sums = attention_weights.sum(dim=-1)

        assert torch.allclose(weight_sums, torch.ones_like(weight_sums), atol=1e-5)

    def test_causal_mask_prevents_future_attention(self, attention_layer):
        """Test that causal mask blocks attention to future positions."""
        seq_len = 8
        batch_size = 2
        embed_dim = 512

        x = torch.randn(batch_size, seq_len, embed_dim)
        causal_mask = torch.triu(
            torch.ones(seq_len, seq_len), diagonal=1
        ).bool()

        _, attention_weights = attention_layer(
            x, x, x, attn_mask=causal_mask
        )

        # Upper triangle (future positions) should have zero attention
        for i in range(seq_len):
            for j in range(i + 1, seq_len):
                assert torch.allclose(
                    attention_weights[:, :, i, j],
                    torch.zeros(batch_size, attention_layer.num_heads),
                    atol=1e-6
                )


class TestResidualBlock:
    """Atomic tests for residual connection block."""

    @pytest.fixture
    def residual_block(self):
        """Provide configured residual block."""
        return ResidualBlock(
            in_features=256,
            hidden_features=512,
            dropout=0.0
        )

    def test_residual_connection_adds_input(self, residual_block):
        """Test that residual connection properly adds input to output."""
        torch.manual_seed(42)
        x = torch.randn(4, 256)

        # Zero out the transformation to test pure residual
        with torch.no_grad():
            for param in residual_block.transform.parameters():
                param.zero_()

        output = residual_block(x)

        assert torch.allclose(output, x, atol=1e-5)

    def test_gradient_flows_through_residual_path(self, residual_block):
        """Test that gradients flow through skip connection."""
        x = torch.randn(4, 256, requires_grad=True)

        output = residual_block(x)
        loss = output.sum()
        loss.backward()

        assert x.grad is not None
        assert not torch.all(x.grad == 0)


class TestPositionalEncoding:
    """Atomic tests for positional encoding layer."""

    @pytest.fixture
    def pos_encoder(self):
        """Provide positional encoding layer."""
        return PositionalEncoding(d_model=512, max_len=1000)

    def test_encoding_is_deterministic(self, pos_encoder):
        """Test that positional encoding produces same output for same input."""
        x = torch.randn(2, 50, 512)

        output1 = pos_encoder(x)
        output2 = pos_encoder(x)

        assert torch.equal(output1, output2)

    def test_different_positions_have_unique_encodings(self, pos_encoder):
        """Test that each position has a unique encoding."""
        x = torch.zeros(1, 100, 512)

        output = pos_encoder(x)

        # Each position should have unique encoding
        encodings = output[0]  # Shape: (100, 512)
        for i in range(100):
            for j in range(i + 1, 100):
                assert not torch.allclose(encodings[i], encodings[j])

    def test_encoding_magnitude_is_bounded(self, pos_encoder):
        """Test that positional encoding values are bounded."""
        x = torch.zeros(1, 1000, 512)

        output = pos_encoder(x)

        # Sinusoidal encodings should be in [-1, 1]
        positional_component = output - x
        assert positional_component.min() >= -1.0
        assert positional_component.max() <= 1.0
```

**Why compliant:** Each test verifies a single behavior of a PyTorch layer. Tests use fixtures for reproducible setup. Dropout is disabled for deterministic testing. Shape assertions verify tensor dimensions. Mathematical properties (sum to one, bounded values) are tested atomically.

---

## VIOLATION: Testing Entire Model Pipeline in One Test

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from models import TransformerModel
from data import TextDataset


def test_transformer_model():
    """Test complete transformer training pipeline."""
    # Load real dataset
    dataset = TextDataset('data/corpus.txt', max_length=512)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Create full model
    model = TransformerModel(
        vocab_size=50000,
        d_model=512,
        n_heads=8,
        n_layers=6,
        d_ff=2048
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    # Train for one epoch
    model.train()
    total_loss = 0
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids']
        labels = batch['labels']

        output = model(input_ids)
        loss = criterion(output.view(-1, 50000), labels.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    # Test inference
    model.eval()
    with torch.no_grad():
        test_input = torch.randint(0, 50000, (1, 100))
        output = model(test_input)

    # Assert multiple unrelated things
    assert output.shape == (1, 100, 50000)
    assert total_loss < 10.0
    assert model.d_model == 512
    assert len(list(model.parameters())) > 0
```

**Why violates ENG-4.1:** The test combines data loading, model construction, training loop, and inference. It depends on external file (`data/corpus.txt`). Training introduces non-determinism through shuffling. Multiple unrelated assertions are bundled together. Test execution time is excessive for a unit test. A single failure point obscures which component failed.

---

## COMPLIANT: Testing Model Training Step in Isolation

```python
import pytest
import torch
import torch.nn as nn


class TestTrainingStep:
    """Atomic tests for model training step logic."""

    @pytest.fixture
    def simple_model(self):
        """Provide simple model for testing training mechanics."""
        return nn.Linear(10, 2)

    @pytest.fixture
    def sample_batch(self):
        """Provide deterministic sample batch."""
        torch.manual_seed(42)
        return {
            'features': torch.randn(8, 10),
            'labels': torch.randint(0, 2, (8,))
        }

    def test_loss_decreases_after_gradient_step(
        self, simple_model, sample_batch
    ):
        """Test that loss decreases after one optimization step."""
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(simple_model.parameters(), lr=0.1)

        # Compute initial loss
        output = simple_model(sample_batch['features'])
        initial_loss = criterion(output, sample_batch['labels'])

        # Perform gradient step
        initial_loss.backward()
        optimizer.step()

        # Compute new loss
        output = simple_model(sample_batch['features'])
        new_loss = criterion(output, sample_batch['labels'])

        assert new_loss < initial_loss

    def test_gradients_are_computed_for_all_parameters(
        self, simple_model, sample_batch
    ):
        """Test that all parameters receive gradients."""
        criterion = nn.CrossEntropyLoss()

        output = simple_model(sample_batch['features'])
        loss = criterion(output, sample_batch['labels'])
        loss.backward()

        for name, param in simple_model.named_parameters():
            assert param.grad is not None, f"No gradient for {name}"
            assert not torch.all(param.grad == 0), f"Zero gradient for {name}"

    def test_optimizer_zero_grad_clears_gradients(
        self, simple_model, sample_batch
    ):
        """Test that zero_grad properly clears accumulated gradients."""
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(simple_model.parameters(), lr=0.1)

        # Compute gradients
        output = simple_model(sample_batch['features'])
        loss = criterion(output, sample_batch['labels'])
        loss.backward()

        # Clear gradients
        optimizer.zero_grad()

        for param in simple_model.parameters():
            if param.grad is not None:
                assert torch.all(param.grad == 0)

    def test_model_parameters_update_after_step(
        self, simple_model, sample_batch
    ):
        """Test that model parameters change after optimization step."""
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(simple_model.parameters(), lr=0.1)

        # Store initial parameters
        initial_params = {
            name: param.clone()
            for name, param in simple_model.named_parameters()
        }

        # Perform gradient step
        output = simple_model(sample_batch['features'])
        loss = criterion(output, sample_batch['labels'])
        loss.backward()
        optimizer.step()

        # Verify parameters changed
        for name, param in simple_model.named_parameters():
            assert not torch.equal(param, initial_params[name])


class TestGradientClipping:
    """Atomic tests for gradient clipping functionality."""

    def test_clip_grad_norm_limits_gradient_magnitude(self):
        """Test that gradient clipping limits norm correctly."""
        model = nn.Linear(10, 10)

        # Create artificially large gradients
        for param in model.parameters():
            param.grad = torch.ones_like(param) * 100

        max_norm = 1.0
        nn.utils.clip_grad_norm_(model.parameters(), max_norm)

        # Compute total norm after clipping
        total_norm = 0
        for param in model.parameters():
            total_norm += param.grad.norm() ** 2
        total_norm = total_norm ** 0.5

        assert total_norm <= max_norm + 1e-5

    def test_clip_grad_value_clips_individual_values(self):
        """Test that value clipping limits individual gradient values."""
        model = nn.Linear(5, 5)

        # Create gradients with extreme values
        for param in model.parameters():
            param.grad = torch.randn_like(param) * 100

        clip_value = 1.0
        nn.utils.clip_grad_value_(model.parameters(), clip_value)

        for param in model.parameters():
            assert param.grad.max() <= clip_value
            assert param.grad.min() >= -clip_value
```

**Why compliant:** Each test focuses on a single aspect of training mechanics. Tests use simple models to isolate training logic from model architecture. Deterministic seeding ensures reproducibility. Gradient behavior, parameter updates, and clipping are tested separately.

---

## VIOLATION: Integration Test Disguised as Unit Test

```python
def test_model_training():
    """Test model trains correctly."""
    from models.transformer import TransformerClassifier
    from data.loader import load_imdb_dataset
    from trainers.classifier import ClassifierTrainer
    from utils.metrics import compute_accuracy

    # Load real data
    train_data, val_data = load_imdb_dataset()

    # Build full model
    model = TransformerClassifier(
        vocab_size=30522,
        hidden_size=768,
        num_layers=12,
        num_heads=12,
        num_classes=2
    )

    # Create trainer
    trainer = ClassifierTrainer(
        model=model,
        train_data=train_data,
        val_data=val_data,
        learning_rate=2e-5,
        epochs=3
    )

    # Train and evaluate
    trainer.train()

    accuracy = compute_accuracy(model, val_data)

    assert accuracy > 0.85
    assert trainer.best_loss < 0.5
    assert trainer.epochs_completed == 3
```

**Why violates ENG-4.1:** Test depends on external data source. Full model and trainer are instantiated. Training for multiple epochs makes test slow and non-deterministic. Accuracy threshold tests model performance, not correctness of code. Multiple concerns (data loading, model construction, training, evaluation) are combined.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/models/test_attention.py::TestMultiHeadAttention::test_output_shape -v

# GREEN: Write code, run test again
pytest tests/models/test_attention.py::TestMultiHeadAttention::test_output_shape -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add MultiHeadAttention layer"
```
