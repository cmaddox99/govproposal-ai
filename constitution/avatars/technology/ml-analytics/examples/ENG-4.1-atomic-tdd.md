---
law_id: ENG-4.1
avatar: ml-analytics
---

# ENG-4.1: Atomic TDD Examples for ML Analytics

## COMPLIANT: Unit Testing Data Preprocessing Pipeline

```python
import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from ml_pipeline.preprocessing import (
    handle_missing_values,
    normalize_features,
    encode_categorical,
    validate_data_schema
)


class TestDataPreprocessing:
    """Atomic tests for data preprocessing functions."""

    @pytest.fixture
    def sample_dataframe(self):
        """Provide clean test data fixture."""
        return pd.DataFrame({
            'numeric_feature': [1.0, 2.0, 3.0, 4.0, 5.0],
            'categorical_feature': ['A', 'B', 'A', 'C', 'B'],
            'target': [0, 1, 0, 1, 1]
        })

    @pytest.fixture
    def dataframe_with_nulls(self):
        """Provide test data with missing values."""
        return pd.DataFrame({
            'numeric_feature': [1.0, np.nan, 3.0, np.nan, 5.0],
            'categorical_feature': ['A', None, 'A', 'C', 'B'],
            'target': [0, 1, 0, 1, 1]
        })

    def test_handle_missing_values_fills_numeric_with_median(
        self, dataframe_with_nulls
    ):
        """Test that numeric nulls are filled with median value."""
        result = handle_missing_values(
            dataframe_with_nulls,
            strategy='median'
        )

        assert not result['numeric_feature'].isna().any()
        # Median of [1.0, 3.0, 5.0] is 3.0
        assert result['numeric_feature'].iloc[1] == 3.0
        assert result['numeric_feature'].iloc[3] == 3.0

    def test_handle_missing_values_fills_categorical_with_mode(
        self, dataframe_with_nulls
    ):
        """Test that categorical nulls are filled with mode."""
        result = handle_missing_values(
            dataframe_with_nulls,
            strategy='mode'
        )

        assert not result['categorical_feature'].isna().any()
        # Mode is 'A' (appears twice)
        assert result['categorical_feature'].iloc[1] == 'A'

    def test_normalize_features_produces_zero_mean_unit_variance(
        self, sample_dataframe
    ):
        """Test normalization produces standardized output."""
        result = normalize_features(
            sample_dataframe,
            columns=['numeric_feature']
        )

        assert np.isclose(result['numeric_feature'].mean(), 0, atol=1e-10)
        assert np.isclose(result['numeric_feature'].std(), 1, atol=1e-10)

    def test_encode_categorical_creates_expected_columns(
        self, sample_dataframe
    ):
        """Test one-hot encoding creates correct columns."""
        result = encode_categorical(
            sample_dataframe,
            columns=['categorical_feature']
        )

        expected_columns = [
            'categorical_feature_A',
            'categorical_feature_B',
            'categorical_feature_C'
        ]
        for col in expected_columns:
            assert col in result.columns

    def test_validate_data_schema_raises_on_missing_column(
        self, sample_dataframe
    ):
        """Test schema validation catches missing required columns."""
        required_schema = {
            'numeric_feature': 'float64',
            'missing_column': 'int64'
        }

        with pytest.raises(ValueError, match="Missing required column"):
            validate_data_schema(sample_dataframe, required_schema)


class TestFeatureEngineering:
    """Atomic tests for feature engineering functions."""

    @pytest.fixture
    def time_series_data(self):
        """Provide time series test data."""
        dates = pd.date_range('2024-01-01', periods=10, freq='D')
        return pd.DataFrame({
            'date': dates,
            'value': [100, 102, 98, 105, 103, 107, 110, 108, 112, 115]
        })

    def test_create_lag_features_generates_correct_lags(
        self, time_series_data
    ):
        """Test lag feature generation."""
        from ml_pipeline.features import create_lag_features

        result = create_lag_features(
            time_series_data,
            column='value',
            lags=[1, 2, 3]
        )

        assert 'value_lag_1' in result.columns
        assert 'value_lag_2' in result.columns
        assert 'value_lag_3' in result.columns
        assert result['value_lag_1'].iloc[3] == 105  # value at index 2

    def test_create_rolling_features_computes_correct_statistics(
        self, time_series_data
    ):
        """Test rolling window statistics."""
        from ml_pipeline.features import create_rolling_features

        result = create_rolling_features(
            time_series_data,
            column='value',
            window=3,
            statistics=['mean', 'std']
        )

        assert 'value_rolling_mean_3' in result.columns
        assert 'value_rolling_std_3' in result.columns
        # Mean of [100, 102, 98] = 100
        assert np.isclose(result['value_rolling_mean_3'].iloc[2], 100)
```

**Why compliant:** Each test focuses on a single behavior of the preprocessing pipeline. Tests use descriptive names that explain the expected behavior. Fixtures provide isolated, reproducible test data. Assertions are specific and verify exact expected outcomes.

---

## VIOLATION: Monolithic Test with Multiple Concerns

```python
import pytest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def test_entire_ml_pipeline():
    """Test the complete ML pipeline from data to predictions."""
    # Load and preprocess data
    df = pd.read_csv('data/train.csv')
    df = df.dropna()
    df['category'] = df['category'].astype('category').cat.codes

    # Split data
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate
    accuracy = accuracy_score(y_test, predictions)

    # Assert everything at once
    assert accuracy > 0.8
    assert len(predictions) == len(y_test)
    assert model.n_estimators == 100
    assert df.isna().sum().sum() == 0
    assert 'category' in df.columns
```

**Why violates ENG-4.1:** This test combines data loading, preprocessing, model training, prediction, and evaluation into a single test. It depends on external file system state (`data/train.csv`). Multiple unrelated assertions are bundled together. If the test fails, it is unclear which component caused the failure. The test is not atomic and cannot be run in isolation.

---

## COMPLIANT: Testing Model Evaluation Metrics in Isolation

```python
import pytest
import numpy as np
from ml_pipeline.evaluation import (
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_ndcg,
    calculate_confusion_matrix_metrics
)


class TestRankingMetrics:
    """Atomic tests for ranking evaluation metrics."""

    @pytest.fixture
    def binary_predictions(self):
        """Provide binary classification predictions."""
        return {
            'y_true': np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1]),
            'y_pred': np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0]),
            'y_scores': np.array([
                0.9, 0.2, 0.8, 0.4, 0.3, 0.7, 0.6, 0.1, 0.85, 0.35
            ])
        }

    def test_precision_at_k_with_k_equals_5(self, binary_predictions):
        """Test precision@5 calculation."""
        precision = calculate_precision_at_k(
            y_true=binary_predictions['y_true'],
            y_scores=binary_predictions['y_scores'],
            k=5
        )

        # Top 5 by score: indices [0, 8, 2, 5, 6]
        # True labels: [1, 1, 1, 1, 0]
        # Precision@5 = 4/5 = 0.8
        assert np.isclose(precision, 0.8)

    def test_recall_at_k_with_k_equals_3(self, binary_predictions):
        """Test recall@3 calculation."""
        recall = calculate_recall_at_k(
            y_true=binary_predictions['y_true'],
            y_scores=binary_predictions['y_scores'],
            k=3
        )

        # Top 3 by score: indices [0, 8, 2]
        # All are positive, total positives = 6
        # Recall@3 = 3/6 = 0.5
        assert np.isclose(recall, 0.5)

    def test_precision_at_k_returns_zero_when_no_positives_in_top_k(self):
        """Test edge case with no positive predictions in top k."""
        y_true = np.array([0, 0, 0, 1, 1])
        y_scores = np.array([0.9, 0.8, 0.7, 0.2, 0.1])

        precision = calculate_precision_at_k(y_true, y_scores, k=3)

        assert precision == 0.0

    def test_ndcg_returns_one_for_perfect_ranking(self):
        """Test NDCG equals 1 for ideal ranking."""
        y_true = np.array([3, 2, 1, 0])  # Relevance scores
        y_scores = np.array([0.9, 0.7, 0.5, 0.3])  # Perfect ranking

        ndcg = calculate_ndcg(y_true, y_scores)

        assert np.isclose(ndcg, 1.0)


class TestClassificationMetrics:
    """Atomic tests for classification metrics."""

    def test_confusion_matrix_metrics_calculates_correctly(self):
        """Test precision, recall, F1 from confusion matrix."""
        y_true = np.array([1, 1, 1, 0, 0, 0, 1, 0])
        y_pred = np.array([1, 1, 0, 0, 0, 1, 1, 0])

        metrics = calculate_confusion_matrix_metrics(y_true, y_pred)

        # TP=3, FP=1, FN=1, TN=3
        assert np.isclose(metrics['precision'], 3/4)  # 0.75
        assert np.isclose(metrics['recall'], 3/4)     # 0.75
        assert np.isclose(metrics['f1'], 0.75)

    def test_confusion_matrix_handles_edge_case_no_positives(self):
        """Test metrics when no positive predictions exist."""
        y_true = np.array([1, 1, 1, 0])
        y_pred = np.array([0, 0, 0, 0])

        metrics = calculate_confusion_matrix_metrics(y_true, y_pred)

        assert metrics['precision'] == 0.0
        assert metrics['recall'] == 0.0
```

**Why compliant:** Each test method verifies a single metric calculation. Test names clearly describe the scenario being tested. Edge cases are tested separately. Mathematical expectations are documented in comments. Tests are independent and can run in any order.

---

## VIOLATION: Testing Metrics Without Isolation

```python
def test_all_metrics():
    """Test all evaluation metrics together."""
    import pandas as pd
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix
    )

    # Load predictions from file
    results = pd.read_csv('results/model_predictions.csv')
    y_true = results['actual']
    y_pred = results['predicted']
    y_proba = results['probability']

    # Calculate all metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_proba)
    cm = confusion_matrix(y_true, y_pred)

    # Assert all metrics are reasonable
    assert accuracy > 0.7, f"Accuracy too low: {accuracy}"
    assert precision > 0.6, f"Precision too low: {precision}"
    assert recall > 0.6, f"Recall too low: {recall}"
    assert f1 > 0.6, f"F1 too low: {f1}"
    assert auc > 0.75, f"AUC too low: {auc}"
    assert cm.shape == (2, 2)

    # Also test that results file has correct format
    assert 'actual' in results.columns
    assert 'predicted' in results.columns
    assert len(results) > 100
```

**Why violates ENG-4.1:** Multiple unrelated metrics are tested in a single test function. The test depends on external file state. Threshold assertions (`> 0.7`) test model performance rather than metric calculation correctness. File format validation is mixed with metric testing. A failure in any assertion makes it difficult to identify the root cause.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/metrics/test_calculator.py::test_accuracy_with_binary_predictions -v

# GREEN: Write code, run test again
pytest tests/metrics/test_calculator.py::test_accuracy_with_binary_predictions -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add accuracy metric to MetricsCalculator"
```
