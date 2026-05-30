# TensorFlow/Keras Guidance

> **Purpose:** Stack-specific agent behaviors for deep learning projects using TensorFlow and Keras.

---

## Overview

This guidance provides patterns for AI agents working with TensorFlow and Keras for deep learning model development, training, and deployment.

---

## Testing Framework

**Primary Framework:** pytest + tensorflow.test

### Test Structure

```python
import pytest
import tensorflow as tf
import numpy as np
from tensorflow import keras
from myproject.models.classifier import ImageClassifier
from myproject.data.dataset import create_dataset
from myproject.training.trainer import ModelTrainer


class TestImageClassifier:
    """Tests for the image classifier model."""

    @pytest.fixture
    def model(self):
        """Create model instance."""
        return ImageClassifier(num_classes=10)

    @pytest.fixture
    def sample_batch(self):
        """Sample input batch."""
        return tf.random.normal((4, 224, 224, 3))

    def test_model_output_shape(self, model, sample_batch):
        """Model output should have correct shape."""
        # Act
        output = model(sample_batch)

        # Assert
        assert output.shape == (4, 10)

    def test_model_output_dtype(self, model, sample_batch):
        """Model output should be float32."""
        output = model(sample_batch)
        assert output.dtype == tf.float32

    def test_model_is_trainable(self, model, sample_batch):
        """Model should have trainable weights."""
        assert len(model.trainable_weights) > 0

    def test_model_gradient_flow(self, model, sample_batch):
        """Gradients should flow through model."""
        with tf.GradientTape() as tape:
            output = model(sample_batch)
            loss = tf.reduce_sum(output)

        gradients = tape.gradient(loss, model.trainable_weights)

        # All gradients should be non-None
        assert all(g is not None for g in gradients)

    def test_model_save_load(self, model, sample_batch, tmp_path):
        """Model should save and load correctly."""
        # Get original prediction
        original_output = model(sample_batch)

        # Save model
        save_path = str(tmp_path / "model")
        model.save(save_path)

        # Load model
        loaded_model = keras.models.load_model(save_path)

        # Predictions should match
        loaded_output = loaded_model(sample_batch)
        np.testing.assert_allclose(
            original_output.numpy(),
            loaded_output.numpy(),
            rtol=1e-5
        )

    @pytest.mark.parametrize("batch_size", [1, 8, 32])
    def test_model_handles_batch_sizes(self, model, batch_size):
        """Model should handle various batch sizes."""
        x = tf.random.normal((batch_size, 224, 224, 3))
        output = model(x)
        assert output.shape[0] == batch_size


class TestDataset:
    """Tests for data pipeline."""

    @pytest.fixture
    def dataset(self):
        """Create test dataset."""
        return create_dataset(
            data_dir="test_data",
            batch_size=4,
            shuffle=False
        )

    def test_dataset_yields_batches(self, dataset):
        """Dataset should yield image, label batches."""
        batch = next(iter(dataset))
        images, labels = batch

        assert len(images.shape) == 4  # batch, height, width, channels
        assert len(labels.shape) == 1  # batch

    def test_dataset_image_range(self, dataset):
        """Images should be normalized to [0, 1]."""
        images, _ = next(iter(dataset))

        assert tf.reduce_min(images) >= 0
        assert tf.reduce_max(images) <= 1


class TestModelTrainer:
    """Tests for training logic."""

    @pytest.fixture
    def trainer(self, model):
        """Create trainer instance."""
        return ModelTrainer(
            model=model,
            optimizer=keras.optimizers.Adam(1e-3),
            loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        )

    def test_train_step_returns_loss(self, trainer, sample_batch):
        """Training step should return loss value."""
        labels = tf.random.uniform((4,), 0, 10, dtype=tf.int32)

        loss = trainer.train_step(sample_batch, labels)

        assert isinstance(loss.numpy(), float)
        assert loss > 0

    def test_train_step_updates_weights(self, trainer, model, sample_batch):
        """Training step should update model weights."""
        labels = tf.random.uniform((4,), 0, 10, dtype=tf.int32)

        # Get initial weights
        initial_weights = [w.numpy().copy() for w in model.trainable_weights]

        # Train step
        trainer.train_step(sample_batch, labels)

        # Weights should change
        for initial, current in zip(initial_weights, model.trainable_weights):
            assert not np.allclose(initial, current.numpy())
```

---

## Common Patterns

### Good Patterns

**Keras Model Subclassing:**

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class ImageClassifier(keras.Model):
    """Image classification model using Keras subclassing."""

    def __init__(
        self,
        num_classes: int,
        backbone: str = "resnet50",
        dropout_rate: float = 0.5,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.backbone = self._create_backbone(backbone)
        self.global_pool = layers.GlobalAveragePooling2D()
        self.dropout = layers.Dropout(dropout_rate)
        self.classifier = layers.Dense(num_classes)

    def _create_backbone(self, name: str) -> keras.Model:
        """Create backbone network."""
        if name == "resnet50":
            backbone = keras.applications.ResNet50(
                include_top=False,
                weights="imagenet",
                input_shape=(224, 224, 3)
            )
            backbone.trainable = False
            return backbone
        else:
            raise ValueError(f"Unknown backbone: {name}")

    def call(self, inputs, training=False):
        """Forward pass."""
        x = self.backbone(inputs, training=training)
        x = self.global_pool(x)
        x = self.dropout(x, training=training)
        return self.classifier(x)

    def get_config(self):
        """Return model configuration."""
        return {
            "num_classes": self.classifier.units,
        }
```

**tf.data Pipeline:**

```python
import tensorflow as tf
from typing import Tuple

def create_dataset(
    data_dir: str,
    batch_size: int = 32,
    image_size: Tuple[int, int] = (224, 224),
    shuffle: bool = True,
    augment: bool = False,
    cache: bool = True
) -> tf.data.Dataset:
    """Create optimized tf.data pipeline."""

    # Load dataset
    dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        image_size=image_size,
        batch_size=None,  # Batch later for better shuffling
        label_mode="int"
    )

    # Normalize images
    normalization = tf.keras.layers.Rescaling(1./255)
    dataset = dataset.map(
        lambda x, y: (normalization(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )

    # Cache before augmentation
    if cache:
        dataset = dataset.cache()

    # Shuffle
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)

    # Augmentation (only for training)
    if augment:
        augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ])
        dataset = dataset.map(
            lambda x, y: (augmentation(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE
        )

    # Batch and prefetch
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    return dataset
```

**Custom Training Loop:**

```python
import tensorflow as tf
from tensorflow import keras
from typing import Dict

class ModelTrainer:
    """Custom training loop with flexibility."""

    def __init__(
        self,
        model: keras.Model,
        optimizer: keras.optimizers.Optimizer,
        loss_fn: keras.losses.Loss,
        metrics: list = None
    ):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.metrics = metrics or []

        # Compile metrics
        self.train_loss = keras.metrics.Mean(name="train_loss")
        self.train_accuracy = keras.metrics.SparseCategoricalAccuracy()

    @tf.function
    def train_step(self, images, labels) -> tf.Tensor:
        """Single training step."""
        with tf.GradientTape() as tape:
            predictions = self.model(images, training=True)
            loss = self.loss_fn(labels, predictions)

        gradients = tape.gradient(loss, self.model.trainable_weights)
        self.optimizer.apply_gradients(
            zip(gradients, self.model.trainable_weights)
        )

        # Update metrics
        self.train_loss.update_state(loss)
        self.train_accuracy.update_state(labels, predictions)

        return loss

    @tf.function
    def test_step(self, images, labels) -> Dict[str, tf.Tensor]:
        """Single evaluation step."""
        predictions = self.model(images, training=False)
        loss = self.loss_fn(labels, predictions)

        return {
            "loss": loss,
            "predictions": predictions
        }

    def fit(
        self,
        train_dataset: tf.data.Dataset,
        val_dataset: tf.data.Dataset = None,
        epochs: int = 10,
        callbacks: list = None
    ) -> Dict:
        """Train the model."""
        history = {"train_loss": [], "train_accuracy": []}
        if val_dataset:
            history["val_loss"] = []
            history["val_accuracy"] = []

        for epoch in range(epochs):
            # Reset metrics
            self.train_loss.reset_states()
            self.train_accuracy.reset_states()

            # Training
            for images, labels in train_dataset:
                self.train_step(images, labels)

            # Record metrics
            history["train_loss"].append(self.train_loss.result().numpy())
            history["train_accuracy"].append(self.train_accuracy.result().numpy())

            # Validation
            if val_dataset:
                val_loss, val_acc = self.evaluate(val_dataset)
                history["val_loss"].append(val_loss)
                history["val_accuracy"].append(val_acc)

            print(f"Epoch {epoch+1}/{epochs} - "
                  f"loss: {history['train_loss'][-1]:.4f} - "
                  f"accuracy: {history['train_accuracy'][-1]:.4f}")

        return history

    def evaluate(self, dataset: tf.data.Dataset) -> Tuple[float, float]:
        """Evaluate on dataset."""
        total_loss = 0
        total_correct = 0
        total_samples = 0

        for images, labels in dataset:
            result = self.test_step(images, labels)
            total_loss += result["loss"].numpy() * len(labels)
            predictions = tf.argmax(result["predictions"], axis=1)
            total_correct += tf.reduce_sum(
                tf.cast(predictions == labels, tf.float32)
            ).numpy()
            total_samples += len(labels)

        return total_loss / total_samples, total_correct / total_samples
```

**Model Export:**

```python
import tensorflow as tf

def export_saved_model(
    model: tf.keras.Model,
    export_path: str,
    input_signature: tf.TensorSpec = None
):
    """Export model as SavedModel."""
    if input_signature is None:
        input_signature = tf.TensorSpec(
            shape=(None, 224, 224, 3),
            dtype=tf.float32
        )

    @tf.function(input_signature=[input_signature])
    def serving_fn(inputs):
        return model(inputs, training=False)

    # Save with signature
    tf.saved_model.save(
        model,
        export_path,
        signatures={"serving_default": serving_fn}
    )


def convert_to_tflite(
    model: tf.keras.Model,
    output_path: str,
    quantize: bool = False
) -> bytes:
    """Convert model to TFLite."""
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]

    tflite_model = converter.convert()

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    return tflite_model
```

---

## Anti-Patterns to Avoid

### Not Using tf.function

```python
# BAD - Python overhead in training loop
def train_step(self, x, y):
    with tf.GradientTape() as tape:
        pred = self.model(x)
        loss = self.loss_fn(y, pred)
    grads = tape.gradient(loss, self.model.trainable_weights)
    self.optimizer.apply_gradients(zip(grads, self.model.trainable_weights))

# GOOD - Compiled graph execution
@tf.function
def train_step(self, x, y):
    # Same code, but faster
```

### Inefficient Data Pipeline

```python
# BAD - No prefetching, no parallelism
dataset = tf.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.batch(32)

# GOOD - Optimized pipeline
dataset = tf.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.cache()
dataset = dataset.shuffle(1000)
dataset = dataset.batch(32)
dataset = dataset.prefetch(tf.data.AUTOTUNE)
```

---

## Tools and Commands

### Development

```bash
# Install TensorFlow
pip install tensorflow

# Check GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Start TensorBoard
tensorboard --logdir logs/
```

### Testing

```bash
# Run tests
pytest

# Run with GPU
pytest --run-gpu

# Model tests
pytest tests/models/
```

### Profiling

```bash
# Profile with TensorBoard
python scripts/train.py --profile

# View profile
tensorboard --logdir logs/
```

---

## TensorFlow-Specific Guidance

### Production Checklist

```markdown
## TensorFlow Production Checklist

### Model Quality
- [ ] Validated on test set
- [ ] Metrics documented
- [ ] No training/inference mismatch

### Code Quality
- [ ] All tests pass
- [ ] tf.function used appropriately
- [ ] Data pipeline optimized

### Export
- [ ] SavedModel exported
- [ ] TFLite converted (if mobile)
- [ ] Signatures documented

### Deployment
- [ ] TF Serving tested
- [ ] Batch inference supported
- [ ] Version tagged
```
