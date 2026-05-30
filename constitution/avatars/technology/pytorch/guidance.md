# PyTorch Guidance

> **Purpose:** Stack-specific agent behaviors for deep learning projects using PyTorch.

---

## Overview

This guidance provides patterns for AI agents working with PyTorch for deep learning model development, training, and deployment.

---

## Testing Framework

**Primary Framework:** pytest + torch.testing

### Test Structure

```python
import pytest
import torch
import torch.nn as nn
from torch.testing import assert_close
from myproject.models.classifier import ImageClassifier
from myproject.data.dataset import CustomDataset
from myproject.training.trainer import Trainer


class TestImageClassifier:
    """Tests for the image classifier model."""

    @pytest.fixture
    def model(self):
        """Create model instance."""
        return ImageClassifier(num_classes=10, pretrained=False)

    @pytest.fixture
    def sample_batch(self):
        """Sample input batch."""
        return torch.randn(4, 3, 224, 224)  # batch, channels, height, width

    def test_model_forward_shape(self, model, sample_batch):
        """Model output should have correct shape."""
        # Act
        output = model(sample_batch)

        # Assert
        assert output.shape == (4, 10)  # batch_size, num_classes

    def test_model_forward_deterministic(self, model, sample_batch):
        """Model should be deterministic in eval mode."""
        # Arrange
        model.eval()

        # Act
        with torch.no_grad():
            output1 = model(sample_batch)
            output2 = model(sample_batch)

        # Assert
        assert_close(output1, output2)

    def test_model_backward_computes_gradients(self, model, sample_batch):
        """Backward pass should compute gradients."""
        # Arrange
        model.train()
        output = model(sample_batch)
        loss = output.sum()

        # Act
        loss.backward()

        # Assert
        for param in model.parameters():
            if param.requires_grad:
                assert param.grad is not None

    def test_model_handles_different_batch_sizes(self, model):
        """Model should handle various batch sizes."""
        for batch_size in [1, 8, 32]:
            x = torch.randn(batch_size, 3, 224, 224)
            output = model(x)
            assert output.shape[0] == batch_size

    @pytest.mark.parametrize("device", ["cpu", pytest.param("cuda", marks=pytest.mark.skipif(
        not torch.cuda.is_available(), reason="CUDA not available"
    ))])
    def test_model_runs_on_device(self, model, sample_batch, device):
        """Model should run on specified device."""
        model = model.to(device)
        x = sample_batch.to(device)

        output = model(x)

        assert output.device.type == device


class TestCustomDataset:
    """Tests for custom dataset."""

    @pytest.fixture
    def dataset(self, tmp_path):
        """Create dataset with temp data."""
        # Create dummy data files
        for i in range(10):
            torch.save(torch.randn(3, 64, 64), tmp_path / f"img_{i}.pt")
        return CustomDataset(data_dir=tmp_path)

    def test_dataset_length(self, dataset):
        """Dataset should return correct length."""
        assert len(dataset) == 10

    def test_dataset_getitem_returns_tuple(self, dataset):
        """Dataset should return (image, label) tuple."""
        item = dataset[0]
        assert isinstance(item, tuple)
        assert len(item) == 2

    def test_dataset_image_shape(self, dataset):
        """Images should have correct shape."""
        image, _ = dataset[0]
        assert image.shape == (3, 64, 64)

    def test_dataset_is_iterable(self, dataset):
        """Dataset should be iterable via DataLoader."""
        from torch.utils.data import DataLoader
        loader = DataLoader(dataset, batch_size=4)

        batch = next(iter(loader))
        images, labels = batch

        assert images.shape == (4, 3, 64, 64)


class TestTrainer:
    """Tests for the training loop."""

    @pytest.fixture
    def trainer(self, model, tmp_path):
        """Create trainer instance."""
        return Trainer(
            model=model,
            optimizer=torch.optim.Adam(model.parameters()),
            criterion=nn.CrossEntropyLoss(),
            device="cpu",
            checkpoint_dir=tmp_path
        )

    def test_trainer_single_step(self, trainer, sample_batch):
        """Trainer should complete single training step."""
        # Arrange
        labels = torch.randint(0, 10, (4,))

        # Act
        loss = trainer.train_step(sample_batch, labels)

        # Assert
        assert isinstance(loss, float)
        assert loss > 0

    def test_trainer_saves_checkpoint(self, trainer, tmp_path):
        """Trainer should save checkpoints."""
        # Act
        trainer.save_checkpoint(epoch=1, loss=0.5)

        # Assert
        checkpoint_files = list(tmp_path.glob("*.pt"))
        assert len(checkpoint_files) > 0

    def test_trainer_loads_checkpoint(self, trainer, tmp_path):
        """Trainer should load checkpoints."""
        # Arrange
        trainer.save_checkpoint(epoch=5, loss=0.3)

        # Act
        loaded_epoch = trainer.load_checkpoint()

        # Assert
        assert loaded_epoch == 5
```

---

## Common Patterns

### Good Patterns

**Model Architecture:**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple

class ImageClassifier(nn.Module):
    """Image classification model with configurable backbone."""

    def __init__(
        self,
        num_classes: int,
        backbone: str = "resnet50",
        pretrained: bool = True,
        dropout: float = 0.5
    ):
        super().__init__()

        self.backbone = self._create_backbone(backbone, pretrained)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(self._get_backbone_features(), num_classes)

        # Initialize weights
        self._init_weights()

    def _create_backbone(self, name: str, pretrained: bool) -> nn.Module:
        """Create backbone network."""
        import torchvision.models as models

        if name == "resnet50":
            backbone = models.resnet50(pretrained=pretrained)
            # Remove final FC layer
            return nn.Sequential(*list(backbone.children())[:-1])
        else:
            raise ValueError(f"Unknown backbone: {name}")

    def _get_backbone_features(self) -> int:
        """Get number of backbone output features."""
        return 2048  # ResNet50

    def _init_weights(self):
        """Initialize classifier weights."""
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        # Backbone features
        features = self.backbone(x)
        features = features.flatten(1)

        # Classification head
        features = self.dropout(features)
        logits = self.fc(features)

        return logits

    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Predict with probabilities."""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
            preds = torch.argmax(probs, dim=1)
        return preds, probs
```

**Training Loop:**

```python
from typing import Dict, Optional
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

class Trainer:
    """Training loop with best practices."""

    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        device: str = "cuda",
        scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
        gradient_clip: float = 1.0,
        accumulation_steps: int = 1
    ):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.scheduler = scheduler
        self.gradient_clip = gradient_clip
        self.accumulation_steps = accumulation_steps

        self.global_step = 0
        self.best_loss = float('inf')

    def train_epoch(self, dataloader: DataLoader) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0
        num_batches = 0

        self.optimizer.zero_grad()

        pbar = tqdm(dataloader, desc="Training")
        for batch_idx, (inputs, targets) in enumerate(pbar):
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)

            # Forward pass
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            loss = loss / self.accumulation_steps

            # Backward pass
            loss.backward()

            # Gradient accumulation
            if (batch_idx + 1) % self.accumulation_steps == 0:
                # Gradient clipping
                if self.gradient_clip > 0:
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(),
                        self.gradient_clip
                    )

                self.optimizer.step()
                self.optimizer.zero_grad()
                self.global_step += 1

            total_loss += loss.item() * self.accumulation_steps
            num_batches += 1

            pbar.set_postfix({"loss": total_loss / num_batches})

        if self.scheduler:
            self.scheduler.step()

        return {"train_loss": total_loss / num_batches}

    @torch.no_grad()
    def evaluate(self, dataloader: DataLoader) -> Dict[str, float]:
        """Evaluate model."""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0

        for inputs, targets in dataloader:
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)

            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        return {
            "val_loss": total_loss / len(dataloader),
            "val_accuracy": correct / total
        }

    def save_checkpoint(self, path: str, epoch: int, metrics: Dict):
        """Save training checkpoint."""
        torch.save({
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict() if self.scheduler else None,
            "metrics": metrics,
            "global_step": self.global_step
        }, path)

    def load_checkpoint(self, path: str) -> int:
        """Load training checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        if self.scheduler and checkpoint["scheduler_state_dict"]:
            self.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

        self.global_step = checkpoint["global_step"]

        return checkpoint["epoch"]
```

**Custom Dataset:**

```python
from torch.utils.data import Dataset
from pathlib import Path
from PIL import Image
import torch

class ImageDataset(Dataset):
    """Custom image dataset with transforms."""

    def __init__(
        self,
        data_dir: str,
        split: str = "train",
        transform = None
    ):
        self.data_dir = Path(data_dir)
        self.split = split
        self.transform = transform

        self.samples = self._load_samples()

    def _load_samples(self) -> list:
        """Load sample paths and labels."""
        samples = []
        split_dir = self.data_dir / self.split

        for class_dir in sorted(split_dir.iterdir()):
            if class_dir.is_dir():
                label = int(class_dir.name)
                for img_path in class_dir.glob("*.jpg"):
                    samples.append((img_path, label))

        return samples

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> tuple:
        img_path, label = self.samples[idx]

        # Load image
        image = Image.open(img_path).convert("RGB")

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return image, label
```

**ONNX Export:**

```python
import torch
import onnx

def export_to_onnx(
    model: nn.Module,
    output_path: str,
    input_shape: tuple = (1, 3, 224, 224),
    opset_version: int = 13,
    dynamic_axes: dict = None
):
    """Export PyTorch model to ONNX."""
    model.eval()

    # Create dummy input
    dummy_input = torch.randn(*input_shape)

    # Default dynamic axes for batch size
    if dynamic_axes is None:
        dynamic_axes = {
            "input": {0: "batch_size"},
            "output": {0: "batch_size"}
        }

    # Export
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=opset_version,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes=dynamic_axes
    )

    # Verify
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)

    print(f"Model exported to {output_path}")
```

---

## Anti-Patterns to Avoid

### No Gradient Zeroing

```python
# BAD - Gradients accumulate incorrectly
for batch in dataloader:
    loss = model(batch).sum()
    loss.backward()
    optimizer.step()  # Gradients from previous batches!

# GOOD - Zero gradients
for batch in dataloader:
    optimizer.zero_grad()
    loss = model(batch).sum()
    loss.backward()
    optimizer.step()
```

### Forgetting eval() Mode

```python
# BAD - Dropout/BatchNorm active during inference
predictions = model(test_data)

# GOOD - Set eval mode
model.eval()
with torch.no_grad():
    predictions = model(test_data)
```

### Device Mismatch

```python
# BAD - Data on different device than model
model = model.cuda()
output = model(cpu_tensor)  # Error!

# GOOD - Ensure same device
model = model.to(device)
data = data.to(device)
output = model(data)
```

---

## Tools and Commands

### Development

```bash
# Install PyTorch
pip install torch torchvision torchaudio

# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Start training
python scripts/train.py --config configs/experiment/baseline.yaml
```

### Testing

```bash
# Run all tests
pytest

# Run with GPU
pytest --run-gpu

# Run model tests
pytest tests/models/

# Run with memory profiling
pytest --memray
```

### Profiling

```bash
# Profile training
python -m torch.profiler scripts/train.py

# Memory profiling
python -c "
import torch
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    model(input)
print(prof.key_averages().table())
"
```

---

## PyTorch-Specific Guidance

### Testing Strategy

1. **Unit Tests** - Test components in isolation
   - Model forward/backward
   - Custom layers
   - Loss functions

2. **Integration Tests** - Test training pipeline
   - Full training step
   - Checkpoint save/load
   - Multi-GPU (if applicable)

3. **Performance Tests** - Validate efficiency
   - Memory usage
   - Throughput
   - Latency

### Production Checklist

```markdown
## PyTorch Production Checklist

### Model Quality
- [ ] Validated on held-out test set
- [ ] Performance metrics documented
- [ ] Model architecture documented

### Code Quality
- [ ] All tests pass
- [ ] No memory leaks
- [ ] Deterministic when seeded

### Export
- [ ] ONNX export verified
- [ ] TorchScript export (if needed)
- [ ] Input/output shapes documented

### Deployment
- [ ] Inference optimizations applied
- [ ] Batch inference supported
- [ ] GPU/CPU inference tested
```
