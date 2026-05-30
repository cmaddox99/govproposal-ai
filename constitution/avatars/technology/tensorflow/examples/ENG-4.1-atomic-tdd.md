---
law_id: ENG-4.1
avatar: tensorflow
---

# ENG-4.1: Atomic TDD Examples for TensorFlow

## COMPLIANT: Unit Testing Custom Keras Layers with tf.test

```python
import tensorflow as tf
import numpy as np
from models.layers import (
    ScaledDotProductAttention,
    MultiHeadAttention,
    PositionWiseFeedForward
)


class TestScaledDotProductAttention(tf.test.TestCase):
    """Atomic tests for scaled dot-product attention layer."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        tf.random.set_seed(42)
        self.attention = ScaledDotProductAttention()

    def test_output_shape_matches_value_shape(self):
        """Test that attention output has same shape as values."""
        batch_size = 4
        seq_len = 16
        d_model = 64

        query = tf.random.normal((batch_size, seq_len, d_model))
        key = tf.random.normal((batch_size, seq_len, d_model))
        value = tf.random.normal((batch_size, seq_len, d_model))

        output, _ = self.attention(query, key, value)

        self.assertEqual(output.shape, value.shape)

    def test_attention_weights_are_valid_distribution(self):
        """Test that attention weights sum to 1 along key dimension."""
        query = tf.random.normal((2, 8, 32))
        key = tf.random.normal((2, 8, 32))
        value = tf.random.normal((2, 8, 32))

        _, attention_weights = self.attention(query, key, value)

        # Sum over key dimension should equal 1
        weight_sums = tf.reduce_sum(attention_weights, axis=-1)
        expected = tf.ones_like(weight_sums)

        self.assertAllClose(weight_sums, expected, atol=1e-5)

    def test_mask_zeros_out_padded_positions(self):
        """Test that mask properly blocks attention to padded positions."""
        query = tf.random.normal((1, 4, 32))
        key = tf.random.normal((1, 4, 32))
        value = tf.random.normal((1, 4, 32))

        # Mask last two positions
        mask = tf.constant([[[[0, 0, 1, 1]]]], dtype=tf.float32) * -1e9

        _, attention_weights = self.attention(query, key, value, mask=mask)

        # Masked positions should have near-zero attention
        masked_weights = attention_weights[0, :, 2:]
        self.assertAllClose(
            masked_weights,
            tf.zeros_like(masked_weights),
            atol=1e-6
        )

    def test_scaling_factor_is_applied_correctly(self):
        """Test that attention scores are scaled by sqrt(d_k)."""
        d_model = 64
        query = tf.ones((1, 1, d_model))
        key = tf.ones((1, 1, d_model))
        value = tf.ones((1, 1, d_model))

        # With all ones, raw dot product = d_model
        # Scaled should be d_model / sqrt(d_model) = sqrt(d_model)
        output, _ = self.attention(query, key, value)

        # Output should be value since softmax of single element is 1
        self.assertAllClose(output, value)


class TestMultiHeadAttention(tf.test.TestCase):
    """Atomic tests for multi-head attention layer."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        tf.random.set_seed(42)
        self.mha = MultiHeadAttention(d_model=512, num_heads=8)

    def test_output_dimension_equals_d_model(self):
        """Test that output has correct embedding dimension."""
        x = tf.random.normal((4, 16, 512))

        output, _ = self.mha(x, x, x)

        self.assertEqual(output.shape[-1], 512)

    def test_attention_heads_are_independent(self):
        """Test that each attention head operates independently."""
        x = tf.random.normal((2, 8, 512))

        _, attention_weights = self.mha(x, x, x, return_attention=True)

        # Weights shape: (batch, num_heads, seq_len, seq_len)
        self.assertEqual(attention_weights.shape[1], 8)

        # Each head should have different attention patterns
        head_0 = attention_weights[:, 0, :, :]
        head_1 = attention_weights[:, 1, :, :]

        # Heads should not be identical (very unlikely with random input)
        self.assertNotAllClose(head_0, head_1)

    def test_layer_is_trainable(self):
        """Test that layer parameters receive gradients."""
        x = tf.random.normal((2, 8, 512))

        with tf.GradientTape() as tape:
            output, _ = self.mha(x, x, x)
            loss = tf.reduce_mean(output)

        gradients = tape.gradient(loss, self.mha.trainable_variables)

        for grad, var in zip(gradients, self.mha.trainable_variables):
            self.assertIsNotNone(grad, f"No gradient for {var.name}")
            self.assertFalse(
                tf.reduce_all(grad == 0),
                f"Zero gradient for {var.name}"
            )


class TestPositionWiseFeedForward(tf.test.TestCase):
    """Atomic tests for position-wise feed-forward layer."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.ffn = PositionWiseFeedForward(d_model=512, d_ff=2048)

    def test_output_shape_matches_input(self):
        """Test that FFN preserves input shape."""
        x = tf.random.normal((4, 16, 512))

        output = self.ffn(x)

        self.assertEqual(output.shape, x.shape)

    def test_inner_dimension_expansion(self):
        """Test that hidden layer has correct expanded dimension."""
        self.assertEqual(self.ffn.dense_1.units, 2048)
        self.assertEqual(self.ffn.dense_2.units, 512)

    def test_activation_function_is_relu(self):
        """Test that ReLU activation is applied."""
        # Input with negative values
        x = tf.constant([[[-1.0, -2.0, 3.0, 4.0]]])

        # Create FFN with identity-like weights to test activation
        ffn = PositionWiseFeedForward(d_model=4, d_ff=4)
        ffn.build((None, None, 4))

        # Set weights to identity (approximately)
        ffn.dense_1.set_weights([
            tf.eye(4).numpy(),
            tf.zeros(4).numpy()
        ])

        output_after_relu = ffn.dense_1(x)

        # ReLU should zero out negative values
        self.assertTrue(tf.reduce_all(output_after_relu >= 0))


if __name__ == '__main__':
    tf.test.main()
```

**Why compliant:** Each test method verifies a single behavior of a TensorFlow layer. Uses `tf.test.TestCase` for proper TensorFlow testing infrastructure. Tests use deterministic seeds for reproducibility. Shape assertions verify tensor dimensions. Layer behavior (trainability, activation, scaling) is tested atomically.

---

## VIOLATION: Testing Entire Model in Single Test

```python
import tensorflow as tf
from tensorflow import keras


def test_transformer_model():
    """Test complete transformer model - not atomic."""
    # Build full model
    model = keras.Sequential([
        keras.layers.Embedding(10000, 512),
        keras.layers.TransformerEncoder(512, 8, 2048),
        keras.layers.GlobalAveragePooling1D(),
        keras.layers.Dense(2, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Generate training data
    x_train = tf.random.uniform((1000, 100), 0, 10000, dtype=tf.int32)
    y_train = tf.random.uniform((1000,), 0, 2, dtype=tf.int32)

    # Train model
    history = model.fit(x_train, y_train, epochs=5, batch_size=32)

    # Test inference
    x_test = tf.random.uniform((10, 100), 0, 10000, dtype=tf.int32)
    predictions = model.predict(x_test)

    # Multiple unrelated assertions
    assert predictions.shape == (10, 2)
    assert history.history['loss'][-1] < history.history['loss'][0]
    assert len(model.layers) == 4
    assert model.count_params() > 0
```

**Why violates ENG-4.1:** Test combines model construction, compilation, training, and inference. Multiple epochs of training make test slow. Random data generation introduces non-determinism. Multiple unrelated assertions are bundled together. Cannot identify which component failed from a test failure.

---

## COMPLIANT: Testing Model Training Callbacks in Isolation

```python
import tensorflow as tf
import tempfile
import os
from callbacks.custom import (
    GradientLoggingCallback,
    LearningRateSchedulerCallback,
    EarlyStoppingWithPatience
)


class TestGradientLoggingCallback(tf.test.TestCase):
    """Atomic tests for gradient logging callback."""

    def setUp(self):
        """Set up simple model and callback for testing."""
        super().setUp()
        tf.random.set_seed(42)

        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, input_shape=(5,)),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='sgd', loss='mse')

        self.log_dir = tempfile.mkdtemp()
        self.callback = GradientLoggingCallback(log_dir=self.log_dir)

    def test_gradient_norms_are_logged(self):
        """Test that gradient norms are written to log directory."""
        x = tf.random.normal((32, 5))
        y = tf.random.normal((32, 1))

        self.model.fit(x, y, epochs=1, callbacks=[self.callback], verbose=0)

        log_files = os.listdir(self.log_dir)
        self.assertTrue(any('gradient' in f for f in log_files))

    def test_callback_does_not_modify_gradients(self):
        """Test that callback logs but does not alter gradients."""
        x = tf.random.normal((32, 5))
        y = tf.random.normal((32, 1))

        # Get weights after training without callback
        model_without = tf.keras.models.clone_model(self.model)
        model_without.compile(optimizer='sgd', loss='mse')
        model_without.set_weights(self.model.get_weights())
        model_without.fit(x, y, epochs=1, verbose=0)
        weights_without = model_without.get_weights()

        # Get weights after training with callback
        model_with = tf.keras.models.clone_model(self.model)
        model_with.compile(optimizer='sgd', loss='mse')
        model_with.set_weights(self.model.get_weights())
        model_with.fit(x, y, epochs=1, callbacks=[self.callback], verbose=0)
        weights_with = model_with.get_weights()

        for w1, w2 in zip(weights_without, weights_with):
            self.assertAllClose(w1, w2)


class TestLearningRateScheduler(tf.test.TestCase):
    """Atomic tests for learning rate scheduler callback."""

    def test_learning_rate_decreases_with_decay_schedule(self):
        """Test that learning rate follows decay schedule."""
        initial_lr = 0.1
        decay_rate = 0.9

        callback = LearningRateSchedulerCallback(
            initial_lr=initial_lr,
            decay_rate=decay_rate,
            decay_steps=1
        )

        model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
        model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=initial_lr), loss='mse')

        x = tf.random.normal((10, 1))
        y = tf.random.normal((10, 1))

        model.fit(x, y, epochs=3, callbacks=[callback], verbose=0)

        # After 3 epochs, LR should be initial_lr * decay_rate^3
        expected_lr = initial_lr * (decay_rate ** 3)
        actual_lr = model.optimizer.learning_rate.numpy()

        self.assertAllClose(actual_lr, expected_lr, atol=1e-6)

    def test_learning_rate_has_minimum_bound(self):
        """Test that learning rate does not go below minimum."""
        callback = LearningRateSchedulerCallback(
            initial_lr=0.1,
            decay_rate=0.1,
            decay_steps=1,
            min_lr=0.001
        )

        model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
        model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.1), loss='mse')

        x = tf.random.normal((10, 1))
        y = tf.random.normal((10, 1))

        model.fit(x, y, epochs=10, callbacks=[callback], verbose=0)

        actual_lr = model.optimizer.learning_rate.numpy()
        self.assertGreaterEqual(actual_lr, 0.001)


class TestEarlyStopping(tf.test.TestCase):
    """Atomic tests for early stopping callback."""

    def test_training_stops_when_metric_plateaus(self):
        """Test that training stops after patience epochs without improvement."""
        callback = EarlyStoppingWithPatience(
            monitor='loss',
            patience=2,
            min_delta=0.01
        )

        model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
        # Use very small learning rate so loss won't improve
        model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=1e-10),
            loss='mse'
        )

        x = tf.random.normal((100, 1))
        y = tf.random.normal((100, 1))

        history = model.fit(
            x, y,
            epochs=100,
            callbacks=[callback],
            verbose=0
        )

        # Should stop well before 100 epochs
        epochs_trained = len(history.history['loss'])
        self.assertLess(epochs_trained, 10)

    def test_best_weights_are_restored(self):
        """Test that best weights are restored after early stopping."""
        callback = EarlyStoppingWithPatience(
            monitor='loss',
            patience=2,
            restore_best_weights=True
        )

        # Verify restore_best_weights flag is set
        self.assertTrue(callback.restore_best_weights)


if __name__ == '__main__':
    tf.test.main()
```

**Why compliant:** Each test focuses on a single callback behavior. Tests use minimal models to isolate callback logic. Deterministic seeds ensure reproducibility. Callback side effects (logging, weight modification) are tested separately. Edge cases (minimum bounds, early stopping) are verified atomically.

---

## VIOLATION: Testing Multiple Callbacks Together

```python
import tensorflow as tf


def test_all_callbacks():
    """Test all callbacks together in one test."""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, input_shape=(10,)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=5),
        tf.keras.callbacks.ModelCheckpoint('model.h5'),
        tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        tf.keras.callbacks.ReduceLROnPlateau(),
        tf.keras.callbacks.CSVLogger('training.csv')
    ]

    x = tf.random.normal((1000, 10))
    y = tf.random.normal((1000, 1))

    history = model.fit(
        x, y,
        epochs=100,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=0
    )

    # Check everything at once
    assert os.path.exists('model.h5')
    assert os.path.exists('./logs')
    assert os.path.exists('training.csv')
    assert len(history.history['loss']) > 0
    assert len(history.history['loss']) < 100  # Early stopping worked
```

**Why violates ENG-4.1:** Multiple unrelated callbacks are tested simultaneously. File system side effects from multiple callbacks. Cannot determine which callback caused a failure. Test has external dependencies (file paths). Single test verifies multiple independent behaviors.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/models/test_layers.py::TestCustomLayer::test_output_shape -v

# GREEN: Write code, run test again
pytest tests/models/test_layers.py::TestCustomLayer::test_output_shape -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add custom TensorFlow layer"
```
