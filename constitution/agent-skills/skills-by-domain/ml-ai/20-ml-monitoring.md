---
skill:
  id: skill-20-ml-monitoring
  name: ML Monitoring
  category: mlops
  version: "2.0.0"

laws:
  implements:
    - id: ENG-5.5
      title: Observability Law
    - id: BUS-6.3
      title: Risk Monitoring Law
  references:
    - id: BUS-3.2
      title: Data Quality Law

triggers:
  phrases:
    - "Monitor model"
    - "Detect drift"
    - "Model performance"
    - "Retraining trigger"

followed_by:
  - skill-17-ml-pipeline
  - skill-11-incident-response
---

# Skill: ML Monitoring

> **Purpose:** Detect model degradation, data drift, and performance issues in production ML systems before they impact business outcomes.

---

## Purpose

ML Monitoring is the practice of continuously observing ML systems in production to ensure they perform as expected. This skill ensures:

1. **Drift Detection** - Catch data and concept drift early
2. **Performance Tracking** - Model accuracy monitored over time
3. **Data Quality** - Input data validated in real-time
4. **Alerting** - Issues detected before users notice
5. **Debugging** - Root cause analysis when things go wrong

**Key principle:** Models degrade silently. Without monitoring, you're flying blind.

---

## When to Invoke

Invoke this skill when:

- Deploying models to production
- Model performance appears to degrade
- Business metrics diverge from model metrics
- Planning retraining schedules
- Investigating prediction quality issues
- Setting up ML observability infrastructure

**Trigger phrases:**
- "Is the model still accurate?"
- "Why are predictions getting worse?"
- "How do we know when to retrain?"
- "The data looks different than training"
- "Set up monitoring for this model"

---

## Constitutional Foundation

### Engineering Constitution
- **Article VI, Section 6.1** - Observability: Model behavior visible
- **Article VI, Section 6.2** - Reliability: SLOs for model quality

### Business Constitution
- **Article IV, Section 4.1** - Continuity: Model degradation detected early
- **Article III, Section 3.3** - Audit Trail: Predictions traceable

---

## Types of ML Monitoring

### Monitoring Taxonomy

```
┌─────────────────────────────────────────────────────────────┐
│                    ML MONITORING                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │   DATA        │  │   MODEL       │  │   SYSTEM      │   │
│  │   MONITORING  │  │   MONITORING  │  │   MONITORING  │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
│                                                              │
│  • Data drift       • Prediction       • Latency            │
│  • Feature drift      distribution     • Throughput         │
│  • Data quality     • Accuracy decay   • Errors             │
│  • Schema changes   • Concept drift    • Resource usage     │
│  • Missing values   • Bias detection   • Dependencies       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Drift Detection

### Statistical Tests for Drift

```python
from scipy import stats
import numpy as np
from typing import Tuple

class DriftDetector:
    """Detect distribution shifts in features."""

    def __init__(self, reference_data: np.ndarray, threshold: float = 0.05):
        self.reference = reference_data
        self.threshold = threshold

    def detect_drift_ks(
        self,
        current_data: np.ndarray
    ) -> Tuple[bool, float]:
        """Kolmogorov-Smirnov test for drift."""
        statistic, p_value = stats.ks_2samp(
            self.reference,
            current_data
        )
        is_drift = p_value < self.threshold
        return is_drift, p_value

    def detect_drift_psi(
        self,
        current_data: np.ndarray,
        bins: int = 10
    ) -> Tuple[bool, float]:
        """Population Stability Index for drift."""
        # Create bins from reference
        min_val = min(self.reference.min(), current_data.min())
        max_val = max(self.reference.max(), current_data.max())
        bin_edges = np.linspace(min_val, max_val, bins + 1)

        # Calculate proportions
        ref_counts, _ = np.histogram(self.reference, bins=bin_edges)
        cur_counts, _ = np.histogram(current_data, bins=bin_edges)

        ref_props = ref_counts / len(self.reference)
        cur_props = cur_counts / len(current_data)

        # Avoid division by zero
        ref_props = np.clip(ref_props, 0.0001, None)
        cur_props = np.clip(cur_props, 0.0001, None)

        # Calculate PSI
        psi = np.sum((cur_props - ref_props) * np.log(cur_props / ref_props))

        # PSI interpretation: <0.1 no drift, 0.1-0.25 moderate, >0.25 significant
        is_drift = psi > 0.25
        return is_drift, psi

    def detect_drift_wasserstein(
        self,
        current_data: np.ndarray
    ) -> Tuple[bool, float]:
        """Wasserstein (Earth Mover's) distance for drift."""
        distance = stats.wasserstein_distance(
            self.reference,
            current_data
        )
        # Normalize by reference std
        normalized_distance = distance / self.reference.std()
        is_drift = normalized_distance > 0.5
        return is_drift, normalized_distance
```

### Multi-Feature Drift Monitoring

```python
from dataclasses import dataclass
import pandas as pd

@dataclass
class DriftReport:
    feature: str
    is_drift: bool
    method: str
    score: float
    threshold: float

class FeatureDriftMonitor:
    """Monitor drift across multiple features."""

    def __init__(
        self,
        reference_df: pd.DataFrame,
        numerical_features: list[str],
        categorical_features: list[str]
    ):
        self.reference = reference_df
        self.numerical = numerical_features
        self.categorical = categorical_features

        # Create detectors for numerical features
        self.numerical_detectors = {
            feat: DriftDetector(reference_df[feat].values)
            for feat in numerical_features
        }

    def check_drift(self, current_df: pd.DataFrame) -> list[DriftReport]:
        """Check drift for all features."""
        reports = []

        # Numerical features - KS test
        for feat in self.numerical:
            is_drift, p_value = self.numerical_detectors[feat].detect_drift_ks(
                current_df[feat].values
            )
            reports.append(DriftReport(
                feature=feat,
                is_drift=is_drift,
                method="ks_test",
                score=p_value,
                threshold=0.05
            ))

        # Categorical features - Chi-squared test
        for feat in self.categorical:
            is_drift, score = self._chi_squared_test(
                self.reference[feat],
                current_df[feat]
            )
            reports.append(DriftReport(
                feature=feat,
                is_drift=is_drift,
                method="chi_squared",
                score=score,
                threshold=0.05
            ))

        return reports

    def _chi_squared_test(
        self,
        reference: pd.Series,
        current: pd.Series
    ) -> Tuple[bool, float]:
        """Chi-squared test for categorical drift."""
        # Get all categories
        all_cats = set(reference.unique()) | set(current.unique())

        # Count frequencies
        ref_counts = reference.value_counts()
        cur_counts = current.value_counts()

        # Align to same categories
        ref_freq = np.array([ref_counts.get(c, 0) for c in all_cats])
        cur_freq = np.array([cur_counts.get(c, 0) for c in all_cats])

        # Normalize
        ref_freq = ref_freq / ref_freq.sum()
        cur_freq = cur_freq / cur_freq.sum()

        # Chi-squared
        statistic, p_value = stats.chisquare(cur_freq, ref_freq)
        return p_value < 0.05, p_value
```

---

## Model Performance Monitoring

### Tracking Metrics Over Time

```python
from datetime import datetime, timedelta
import pandas as pd
from collections import deque

class PerformanceMonitor:
    """Track model performance metrics over time."""

    def __init__(
        self,
        window_size: int = 1000,
        alert_thresholds: dict = None
    ):
        self.window_size = window_size
        self.predictions = deque(maxlen=window_size)
        self.actuals = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)

        self.alert_thresholds = alert_thresholds or {
            "accuracy": 0.85,
            "precision": 0.80,
            "recall": 0.75,
            "f1": 0.80
        }

        self.baseline_metrics = None

    def log_prediction(
        self,
        prediction: int,
        actual: int = None,
        timestamp: datetime = None
    ):
        """Log a prediction and optional ground truth."""
        self.predictions.append(prediction)
        self.actuals.append(actual)
        self.timestamps.append(timestamp or datetime.utcnow())

    def update_ground_truth(self, index: int, actual: int):
        """Update ground truth when labels become available."""
        if index < len(self.actuals):
            self.actuals[index] = actual

    def calculate_metrics(self) -> dict:
        """Calculate current window metrics."""
        # Filter to labeled examples
        labeled = [
            (p, a) for p, a in zip(self.predictions, self.actuals)
            if a is not None
        ]

        if not labeled:
            return {}

        preds, actuals = zip(*labeled)
        preds = np.array(preds)
        actuals = np.array(actuals)

        return {
            "accuracy": (preds == actuals).mean(),
            "precision": self._precision(preds, actuals),
            "recall": self._recall(preds, actuals),
            "f1": self._f1(preds, actuals),
            "sample_size": len(labeled),
            "window_start": min(self.timestamps),
            "window_end": max(self.timestamps)
        }

    def check_alerts(self) -> list[dict]:
        """Check if metrics breach thresholds."""
        metrics = self.calculate_metrics()
        alerts = []

        for metric, threshold in self.alert_thresholds.items():
            if metric in metrics and metrics[metric] < threshold:
                alerts.append({
                    "metric": metric,
                    "current_value": metrics[metric],
                    "threshold": threshold,
                    "severity": self._severity(metrics[metric], threshold)
                })

        return alerts

    def _severity(self, value: float, threshold: float) -> str:
        """Determine alert severity."""
        degradation = (threshold - value) / threshold
        if degradation > 0.2:
            return "critical"
        elif degradation > 0.1:
            return "warning"
        return "info"
```

### Delayed Ground Truth Handling

```python
class DelayedLabelMonitor:
    """Handle scenarios where labels arrive after predictions."""

    def __init__(self, label_delay_hours: int = 24):
        self.label_delay = timedelta(hours=label_delay_hours)
        self.pending_predictions = {}  # request_id -> prediction_info
        self.completed_predictions = deque(maxlen=10000)

    def log_prediction(
        self,
        request_id: str,
        prediction: int,
        features: dict,
        timestamp: datetime = None
    ):
        """Store prediction awaiting label."""
        self.pending_predictions[request_id] = {
            "prediction": prediction,
            "features": features,
            "timestamp": timestamp or datetime.utcnow(),
            "actual": None
        }

    def log_label(self, request_id: str, actual: int):
        """Attach label to prediction."""
        if request_id in self.pending_predictions:
            pred_info = self.pending_predictions.pop(request_id)
            pred_info["actual"] = actual
            pred_info["label_timestamp"] = datetime.utcnow()
            self.completed_predictions.append(pred_info)

    def get_metrics_for_period(
        self,
        start: datetime,
        end: datetime
    ) -> dict:
        """Calculate metrics for a time period."""
        relevant = [
            p for p in self.completed_predictions
            if start <= p["timestamp"] <= end
            and p["actual"] is not None
        ]

        if not relevant:
            return {"error": "No labeled data in period"}

        preds = [p["prediction"] for p in relevant]
        actuals = [p["actual"] for p in relevant]

        return {
            "accuracy": np.mean(np.array(preds) == np.array(actuals)),
            "sample_size": len(relevant),
            "period_start": start.isoformat(),
            "period_end": end.isoformat()
        }
```

---

## Prediction Distribution Monitoring

### Output Distribution Tracking

```python
class PredictionDistributionMonitor:
    """Monitor prediction output distributions."""

    def __init__(self, reference_predictions: np.ndarray):
        self.reference = reference_predictions
        self.reference_distribution = self._compute_distribution(reference_predictions)

    def _compute_distribution(self, predictions: np.ndarray) -> dict:
        """Compute distribution statistics."""
        if predictions.dtype in [np.float32, np.float64]:
            # Continuous predictions (probabilities)
            return {
                "mean": predictions.mean(),
                "std": predictions.std(),
                "percentiles": {
                    "p10": np.percentile(predictions, 10),
                    "p25": np.percentile(predictions, 25),
                    "p50": np.percentile(predictions, 50),
                    "p75": np.percentile(predictions, 75),
                    "p90": np.percentile(predictions, 90),
                }
            }
        else:
            # Categorical predictions
            unique, counts = np.unique(predictions, return_counts=True)
            return {
                "class_distribution": dict(zip(unique.tolist(), (counts/len(predictions)).tolist()))
            }

    def check_distribution_shift(
        self,
        current_predictions: np.ndarray
    ) -> dict:
        """Check for shifts in prediction distribution."""
        current_dist = self._compute_distribution(current_predictions)

        alerts = []

        if "mean" in self.reference_distribution:
            # Continuous case
            mean_shift = abs(
                current_dist["mean"] - self.reference_distribution["mean"]
            ) / self.reference_distribution["std"]

            if mean_shift > 2:
                alerts.append({
                    "type": "mean_shift",
                    "reference": self.reference_distribution["mean"],
                    "current": current_dist["mean"],
                    "z_score": mean_shift
                })

        if "class_distribution" in self.reference_distribution:
            # Categorical case
            ref_dist = self.reference_distribution["class_distribution"]
            cur_dist = current_dist["class_distribution"]

            for cls in ref_dist:
                if cls in cur_dist:
                    shift = abs(cur_dist[cls] - ref_dist[cls])
                    if shift > 0.1:  # 10% shift
                        alerts.append({
                            "type": "class_shift",
                            "class": cls,
                            "reference": ref_dist[cls],
                            "current": cur_dist[cls]
                        })

        return {
            "current_distribution": current_dist,
            "alerts": alerts,
            "is_shifted": len(alerts) > 0
        }
```

---

## Data Quality Monitoring

### Real-Time Data Validation

```python
from dataclasses import dataclass
from enum import Enum

class QualityIssue(Enum):
    MISSING_VALUE = "missing_value"
    OUT_OF_RANGE = "out_of_range"
    INVALID_TYPE = "invalid_type"
    SCHEMA_MISMATCH = "schema_mismatch"
    ANOMALY = "anomaly"

@dataclass
class DataQualityAlert:
    feature: str
    issue: QualityIssue
    value: any
    expected: str
    timestamp: datetime

class DataQualityMonitor:
    """Monitor input data quality in real-time."""

    def __init__(self, schema: dict, reference_stats: dict):
        """
        schema: {feature: {"type": str, "nullable": bool, "min": float, "max": float}}
        reference_stats: {feature: {"mean": float, "std": float}}
        """
        self.schema = schema
        self.reference_stats = reference_stats
        self.alerts = []

    def validate(self, data: dict) -> list[DataQualityAlert]:
        """Validate a single input record."""
        alerts = []

        for feature, spec in self.schema.items():
            value = data.get(feature)

            # Missing value check
            if value is None or (isinstance(value, float) and np.isnan(value)):
                if not spec.get("nullable", False):
                    alerts.append(DataQualityAlert(
                        feature=feature,
                        issue=QualityIssue.MISSING_VALUE,
                        value=value,
                        expected="non-null",
                        timestamp=datetime.utcnow()
                    ))
                continue

            # Type check
            expected_type = spec.get("type")
            if expected_type and not isinstance(value, eval(expected_type)):
                alerts.append(DataQualityAlert(
                    feature=feature,
                    issue=QualityIssue.INVALID_TYPE,
                    value=type(value).__name__,
                    expected=expected_type,
                    timestamp=datetime.utcnow()
                ))
                continue

            # Range check
            if "min" in spec and value < spec["min"]:
                alerts.append(DataQualityAlert(
                    feature=feature,
                    issue=QualityIssue.OUT_OF_RANGE,
                    value=value,
                    expected=f">= {spec['min']}",
                    timestamp=datetime.utcnow()
                ))

            if "max" in spec and value > spec["max"]:
                alerts.append(DataQualityAlert(
                    feature=feature,
                    issue=QualityIssue.OUT_OF_RANGE,
                    value=value,
                    expected=f"<= {spec['max']}",
                    timestamp=datetime.utcnow()
                ))

            # Anomaly check (z-score)
            if feature in self.reference_stats:
                stats = self.reference_stats[feature]
                z_score = abs(value - stats["mean"]) / stats["std"]
                if z_score > 4:  # 4 sigma
                    alerts.append(DataQualityAlert(
                        feature=feature,
                        issue=QualityIssue.ANOMALY,
                        value=value,
                        expected=f"within 4σ of {stats['mean']:.2f}",
                        timestamp=datetime.utcnow()
                    ))

        return alerts
```

---

## Alerting System

### ML Alert Manager

```python
from enum import Enum
from dataclasses import dataclass

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class MLAlert:
    name: str
    severity: AlertSeverity
    message: str
    metric_value: float
    threshold: float
    timestamp: datetime
    model_name: str
    model_version: str

class MLAlertManager:
    """Manage ML-specific alerts."""

    def __init__(self, config: dict):
        """
        config = {
            "accuracy_drop": {"threshold": 0.05, "severity": "critical"},
            "latency_spike": {"threshold_ms": 100, "severity": "warning"},
            "drift_detected": {"severity": "warning"},
            ...
        }
        """
        self.config = config
        self.alert_handlers = []

    def register_handler(self, handler):
        """Register alert handler (Slack, PagerDuty, etc.)."""
        self.alert_handlers.append(handler)

    def check_accuracy_drop(
        self,
        current_accuracy: float,
        baseline_accuracy: float,
        model_name: str,
        model_version: str
    ) -> MLAlert | None:
        """Check for accuracy degradation."""
        drop = baseline_accuracy - current_accuracy
        threshold = self.config["accuracy_drop"]["threshold"]

        if drop > threshold:
            alert = MLAlert(
                name="accuracy_drop",
                severity=AlertSeverity(self.config["accuracy_drop"]["severity"]),
                message=f"Model accuracy dropped by {drop:.2%} (threshold: {threshold:.2%})",
                metric_value=current_accuracy,
                threshold=baseline_accuracy - threshold,
                timestamp=datetime.utcnow(),
                model_name=model_name,
                model_version=model_version
            )
            self._dispatch(alert)
            return alert

        return None

    def check_drift(
        self,
        drift_score: float,
        feature: str,
        model_name: str,
        model_version: str
    ) -> MLAlert | None:
        """Check for data drift."""
        if drift_score > 0.25:  # PSI threshold
            severity = AlertSeverity.CRITICAL if drift_score > 0.5 else AlertSeverity.WARNING

            alert = MLAlert(
                name="data_drift",
                severity=severity,
                message=f"Data drift detected in feature '{feature}' (PSI: {drift_score:.3f})",
                metric_value=drift_score,
                threshold=0.25,
                timestamp=datetime.utcnow(),
                model_name=model_name,
                model_version=model_version
            )
            self._dispatch(alert)
            return alert

        return None

    def _dispatch(self, alert: MLAlert):
        """Send alert to all handlers."""
        for handler in self.alert_handlers:
            try:
                handler.send(alert)
            except Exception as e:
                logger.error(f"Failed to dispatch alert: {e}")


# Example handler
class SlackAlertHandler:
    def __init__(self, webhook_url: str, channel: str):
        self.webhook_url = webhook_url
        self.channel = channel

    def send(self, alert: MLAlert):
        """Send alert to Slack."""
        color = {
            AlertSeverity.INFO: "#36a64f",
            AlertSeverity.WARNING: "#ff9800",
            AlertSeverity.CRITICAL: "#f44336"
        }[alert.severity]

        payload = {
            "channel": self.channel,
            "attachments": [{
                "color": color,
                "title": f"🤖 ML Alert: {alert.name}",
                "text": alert.message,
                "fields": [
                    {"title": "Model", "value": f"{alert.model_name} v{alert.model_version}", "short": True},
                    {"title": "Severity", "value": alert.severity.value, "short": True},
                    {"title": "Current Value", "value": f"{alert.metric_value:.4f}", "short": True},
                    {"title": "Threshold", "value": f"{alert.threshold:.4f}", "short": True},
                ],
                "ts": alert.timestamp.timestamp()
            }]
        }

        requests.post(self.webhook_url, json=payload)
```

---

## Monitoring Dashboard Metrics

### Prometheus Metrics for ML

```python
from prometheus_client import Counter, Histogram, Gauge, Summary

# Prediction metrics
PREDICTIONS_TOTAL = Counter(
    'ml_predictions_total',
    'Total predictions made',
    ['model_name', 'model_version', 'prediction_class']
)

PREDICTION_LATENCY = Histogram(
    'ml_prediction_latency_seconds',
    'Prediction latency',
    ['model_name', 'model_version'],
    buckets=[.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0]
)

# Data quality metrics
DATA_QUALITY_ISSUES = Counter(
    'ml_data_quality_issues_total',
    'Data quality issues detected',
    ['model_name', 'feature', 'issue_type']
)

# Drift metrics
FEATURE_DRIFT_SCORE = Gauge(
    'ml_feature_drift_score',
    'Current drift score by feature',
    ['model_name', 'feature', 'method']
)

# Performance metrics
MODEL_ACCURACY = Gauge(
    'ml_model_accuracy',
    'Current model accuracy',
    ['model_name', 'model_version', 'window']
)

PREDICTION_DISTRIBUTION = Histogram(
    'ml_prediction_probability',
    'Distribution of prediction probabilities',
    ['model_name', 'model_version'],
    buckets=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
)
```

---

## Good Examples

### Example 1: Comprehensive Monitoring Setup

```python
class MLMonitoringPipeline:
    """Complete ML monitoring pipeline."""

    def __init__(self, model_name: str, model_version: str, config: dict):
        self.model_name = model_name
        self.model_version = model_version

        # Initialize monitors
        self.drift_monitor = FeatureDriftMonitor(
            reference_df=config["reference_data"],
            numerical_features=config["numerical_features"],
            categorical_features=config["categorical_features"]
        )

        self.performance_monitor = PerformanceMonitor(
            window_size=config.get("window_size", 1000),
            alert_thresholds=config.get("alert_thresholds")
        )

        self.data_quality_monitor = DataQualityMonitor(
            schema=config["schema"],
            reference_stats=config["reference_stats"]
        )

        self.alert_manager = MLAlertManager(config["alert_config"])

    def process_prediction(
        self,
        features: dict,
        prediction: int,
        probability: float,
        actual: int = None
    ):
        """Process a prediction through all monitors."""

        # 1. Data quality check
        quality_alerts = self.data_quality_monitor.validate(features)
        for alert in quality_alerts:
            DATA_QUALITY_ISSUES.labels(
                model_name=self.model_name,
                feature=alert.feature,
                issue_type=alert.issue.value
            ).inc()

        # 2. Log prediction
        PREDICTIONS_TOTAL.labels(
            model_name=self.model_name,
            model_version=self.model_version,
            prediction_class=str(prediction)
        ).inc()

        PREDICTION_DISTRIBUTION.labels(
            model_name=self.model_name,
            model_version=self.model_version
        ).observe(probability)

        # 3. Performance tracking (if label available)
        if actual is not None:
            self.performance_monitor.log_prediction(prediction, actual)

            metrics = self.performance_monitor.calculate_metrics()
            MODEL_ACCURACY.labels(
                model_name=self.model_name,
                model_version=self.model_version,
                window="rolling_1000"
            ).set(metrics.get("accuracy", 0))

        # 4. Check alerts
        for alert in self.performance_monitor.check_alerts():
            self.alert_manager.check_accuracy_drop(
                current_accuracy=alert["current_value"],
                baseline_accuracy=alert["threshold"] * 1.1,
                model_name=self.model_name,
                model_version=self.model_version
            )
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Monitoring

```python
# BAD - Deploy and forget
def predict(features):
    return model.predict(features)
    # No tracking, no alerts, no visibility
```

**Correct approach:** Instrument all predictions with metrics.

---

### Anti-Pattern 2: Only System Metrics

```python
# BAD - Only monitor infrastructure
metrics = {
    "cpu": get_cpu(),
    "memory": get_memory(),
    "latency": get_latency()
}
# Model could be returning garbage with perfect latency!
```

**Correct approach:** Monitor model-specific metrics (drift, accuracy, distribution).

---

## Quality Checklist

Before considering ML monitoring complete:

### Data Monitoring
- [ ] Feature drift detection configured
- [ ] Data quality validation in place
- [ ] Schema validation enforced
- [ ] Anomaly detection for inputs

### Model Monitoring
- [ ] Prediction distribution tracked
- [ ] Performance metrics calculated (when labels available)
- [ ] Baseline metrics established
- [ ] A/B test metrics tracked

### Alerting
- [ ] Drift alerts configured
- [ ] Performance degradation alerts set
- [ ] Data quality alerts enabled
- [ ] Escalation paths defined

### Observability
- [ ] Prometheus/Grafana dashboards created
- [ ] Logging includes model version
- [ ] Prediction audit trail maintained

---

## Skill Interactions

### Preceded By
- **19-Model Serving** - Serving generates data to monitor
- **18-Experiment Tracking** - Baseline metrics from experiments

### Followed By
- **17-ML Pipeline** - Triggers retraining when drift detected

### Related Skills
- **13-Observability** - General observability patterns
- **11-Incident Response** - Respond to ML incidents
