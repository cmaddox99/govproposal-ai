---
skill:
  id: skill-19-model-serving
  name: Model Serving
  category: mlops
  version: "2.0.0"

laws:
  implements:
    - id: ENG-7.1
      title: Failure Handling Law
    - id: ENG-7.5
      title: Graceful Degradation Law
  references:
    - id: ENG-5.2
      title: CI/CD Pipeline Law
    - id: ENG-7.2
      title: Circuit Breaker Law

triggers:
  phrases:
    - "Deploy model"
    - "Model serving"
    - "Inference API"
    - "Model versioning"

followed_by:
  - skill-20-ml-monitoring
  - skill-12-api-design
---

# Skill: Model Serving

> **Purpose:** Deploy machine learning models to production with reliability, scalability, and the ability to update without downtime.

---

## Purpose

Model Serving is the practice of making trained ML models available for real-time or batch predictions in production. This skill ensures:

1. **Reliability** - Models serve predictions consistently
2. **Scalability** - Handle varying load gracefully
3. **Latency** - Meet response time requirements
4. **Versioning** - Multiple model versions manageable
5. **Safety** - Updates don't break production

**Key principle:** A model that can't serve predictions is just a file. Serving is where ML delivers value.

---

## When to Invoke

Invoke this skill when:

- Deploying a model to production for the first time
- Updating an existing production model
- Optimizing inference performance
- Scaling model serving infrastructure
- Implementing A/B testing for models
- Designing batch prediction systems

**Trigger phrases:**
- "How do we deploy this model?"
- "Inference is too slow"
- "We need to update the model safely"
- "Set up A/B testing for the new model"
- "Our model can't handle the load"

---

## Constitutional Foundation

### Engineering Constitution
- **Article VI, Section 6.1** - Observability: Serving metrics monitored
- **Article VI, Section 6.2** - Reliability: SLOs defined and met
- **Article II, Section 2.1** - Simplicity: Serving architecture appropriate

### Business Constitution
- **Article IV, Section 4.1** - Continuity: Zero-downtime deployments
- **Article III, Section 3.3** - Audit Trail: Predictions traceable

---

## Serving Patterns

### Pattern Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVING PATTERNS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   Online    │     │   Batch     │     │  Streaming  │   │
│  │  (Real-time)│     │ (Scheduled) │     │  (Events)   │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                              │
│  - REST API          - Spark jobs       - Kafka consumers   │
│  - gRPC              - Airflow DAGs     - Flink             │
│  - <100ms latency    - Daily/hourly     - Near real-time    │
│  - User-facing       - Bulk scoring     - Event-driven      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Online Serving

### REST API with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import numpy as np
from typing import List

app = FastAPI(title="Model Serving API")

# Load model at startup
MODEL = None

@app.on_event("startup")
async def load_model():
    global MODEL
    MODEL = mlflow.pyfunc.load_model("models:/fraud-detection/Production")

# Request/Response schemas
class PredictionRequest(BaseModel):
    features: List[float]
    request_id: str = None

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str
    request_id: str

class BatchRequest(BaseModel):
    instances: List[List[float]]

class BatchResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]

# Single prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = MODEL.predict(features)[0]

        # Get probability if available
        if hasattr(MODEL, "predict_proba"):
            probability = float(MODEL.predict_proba(features)[0].max())
        else:
            probability = 1.0

        return PredictionResponse(
            prediction=int(prediction),
            probability=probability,
            model_version=MODEL.metadata.run_id,
            request_id=request.request_id or "generated"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch prediction endpoint
@app.post("/predict/batch", response_model=BatchResponse)
async def predict_batch(request: BatchRequest):
    features = np.array(request.instances)
    predictions = MODEL.predict(features)

    if hasattr(MODEL, "predict_proba"):
        probabilities = MODEL.predict_proba(features).max(axis=1).tolist()
    else:
        probabilities = [1.0] * len(predictions)

    return BatchResponse(
        predictions=predictions.tolist(),
        probabilities=probabilities
    )

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "model_version": MODEL.metadata.run_id if MODEL else None
    }
```

### gRPC Serving

```python
# prediction_service.proto
"""
syntax = "proto3";

service PredictionService {
    rpc Predict (PredictRequest) returns (PredictResponse);
    rpc PredictBatch (PredictBatchRequest) returns (PredictBatchResponse);
}

message PredictRequest {
    repeated float features = 1;
    string request_id = 2;
}

message PredictResponse {
    int32 prediction = 1;
    float probability = 2;
    string model_version = 3;
}
"""

import grpc
from concurrent import futures
import prediction_pb2
import prediction_pb2_grpc

class PredictionServicer(prediction_pb2_grpc.PredictionServiceServicer):

    def __init__(self, model):
        self.model = model

    def Predict(self, request, context):
        features = np.array(request.features).reshape(1, -1)
        prediction = self.model.predict(features)[0]

        return prediction_pb2.PredictResponse(
            prediction=int(prediction),
            probability=float(self.model.predict_proba(features)[0].max()),
            model_version=self.model.metadata.run_id
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServicer(model), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

---

## Model Optimization

### Latency Optimization

```python
import onnxruntime as ort
import numpy as np

class OptimizedModelServer:
    """Serve models with ONNX Runtime for better performance."""

    def __init__(self, onnx_model_path: str):
        # Configure for performance
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = 4

        self.session = ort.InferenceSession(
            onnx_model_path,
            sess_options,
            providers=['CPUExecutionProvider']  # or 'CUDAExecutionProvider'
        )

        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Fast prediction with ONNX Runtime."""
        return self.session.run(
            None,
            {self.input_name: features.astype(np.float32)}
        )[0]


# Converting sklearn model to ONNX
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

def export_to_onnx(model, n_features: int, output_path: str):
    """Export sklearn model to ONNX format."""
    initial_type = [('float_input', FloatTensorType([None, n_features]))]

    onnx_model = convert_sklearn(model, initial_types=initial_type)

    with open(output_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
```

### Batching for Throughput

```python
import asyncio
from collections import deque
import time

class DynamicBatcher:
    """Batch requests for improved throughput."""

    def __init__(
        self,
        model,
        max_batch_size: int = 32,
        max_wait_ms: float = 10.0
    ):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms

        self.queue = deque()
        self.lock = asyncio.Lock()

    async def predict(self, features: np.ndarray) -> np.ndarray:
        """Add request to batch and wait for result."""
        future = asyncio.Future()

        async with self.lock:
            self.queue.append((features, future))

            # If batch is full, process immediately
            if len(self.queue) >= self.max_batch_size:
                await self._process_batch()

        # Start timer for max wait
        asyncio.create_task(self._wait_and_process())

        return await future

    async def _wait_and_process(self):
        """Wait for max_wait_ms then process."""
        await asyncio.sleep(self.max_wait_ms / 1000)

        async with self.lock:
            if self.queue:
                await self._process_batch()

    async def _process_batch(self):
        """Process all queued requests as a batch."""
        if not self.queue:
            return

        # Collect batch
        batch_items = []
        while self.queue and len(batch_items) < self.max_batch_size:
            batch_items.append(self.queue.popleft())

        # Stack features
        features = np.vstack([item[0] for item in batch_items])

        # Batch predict
        predictions = self.model.predict(features)

        # Distribute results
        for i, (_, future) in enumerate(batch_items):
            future.set_result(predictions[i])
```

---

## Deployment Strategies

### Canary Deployment

```python
import random
from dataclasses import dataclass

@dataclass
class ModelVersion:
    model: any
    version: str
    weight: float  # Traffic percentage (0.0 - 1.0)

class CanaryRouter:
    """Route traffic between model versions."""

    def __init__(self):
        self.versions: List[ModelVersion] = []

    def add_version(self, model, version: str, weight: float):
        """Add a model version with traffic weight."""
        self.versions.append(ModelVersion(model, version, weight))
        self._normalize_weights()

    def _normalize_weights(self):
        """Ensure weights sum to 1.0."""
        total = sum(v.weight for v in self.versions)
        for v in self.versions:
            v.weight = v.weight / total

    def route(self) -> ModelVersion:
        """Select model based on weights."""
        r = random.random()
        cumulative = 0.0

        for version in self.versions:
            cumulative += version.weight
            if r <= cumulative:
                return version

        return self.versions[-1]

    def predict(self, features):
        """Route and predict."""
        selected = self.route()
        prediction = selected.model.predict(features)

        return {
            "prediction": prediction,
            "model_version": selected.version
        }

# Usage
router = CanaryRouter()
router.add_version(old_model, "v1.0", weight=0.9)  # 90% traffic
router.add_version(new_model, "v2.0", weight=0.1)  # 10% canary
```

### Blue-Green Deployment

```python
from enum import Enum

class Slot(Enum):
    BLUE = "blue"
    GREEN = "green"

class BlueGreenDeployer:
    """Blue-green deployment for zero-downtime updates."""

    def __init__(self):
        self.slots = {
            Slot.BLUE: None,
            Slot.GREEN: None
        }
        self.active_slot = Slot.BLUE

    def deploy(self, model, version: str) -> Slot:
        """Deploy to inactive slot."""
        inactive_slot = self._get_inactive_slot()
        self.slots[inactive_slot] = {
            "model": model,
            "version": version,
            "deployed_at": datetime.utcnow()
        }
        return inactive_slot

    def _get_inactive_slot(self) -> Slot:
        """Get the slot not currently serving traffic."""
        return Slot.GREEN if self.active_slot == Slot.BLUE else Slot.BLUE

    def switch(self):
        """Switch traffic to the other slot."""
        inactive = self._get_inactive_slot()
        if self.slots[inactive] is None:
            raise ValueError("Cannot switch to empty slot")

        self.active_slot = inactive

    def rollback(self):
        """Switch back to previous slot."""
        self.switch()

    def get_active_model(self):
        """Get the currently active model."""
        return self.slots[self.active_slot]["model"]

    def predict(self, features):
        """Predict using active model."""
        model = self.get_active_model()
        return model.predict(features)
```

### Shadow Deployment

```python
import asyncio
from dataclasses import dataclass

@dataclass
class ShadowResult:
    primary_prediction: any
    shadow_prediction: any
    primary_latency_ms: float
    shadow_latency_ms: float
    predictions_match: bool

class ShadowDeployer:
    """Run shadow model alongside primary for comparison."""

    def __init__(self, primary_model, shadow_model):
        self.primary = primary_model
        self.shadow = shadow_model

    async def predict(self, features) -> ShadowResult:
        """Run both models, return primary result."""

        # Run both concurrently
        primary_task = asyncio.create_task(
            self._timed_predict(self.primary, features)
        )
        shadow_task = asyncio.create_task(
            self._timed_predict(self.shadow, features)
        )

        primary_result, primary_latency = await primary_task

        # Don't wait for shadow to complete - fire and forget logging
        asyncio.create_task(
            self._log_shadow_result(shadow_task, primary_result)
        )

        return primary_result

    async def _timed_predict(self, model, features):
        """Predict with timing."""
        start = time.time()
        result = model.predict(features)
        latency = (time.time() - start) * 1000
        return result, latency

    async def _log_shadow_result(self, shadow_task, primary_result):
        """Log shadow comparison (async, non-blocking)."""
        try:
            shadow_result, shadow_latency = await shadow_task
            match = np.array_equal(primary_result, shadow_result)

            # Log for analysis
            logger.info("shadow_comparison",
                predictions_match=match,
                primary=primary_result.tolist(),
                shadow=shadow_result.tolist()
            )
        except Exception as e:
            logger.warning("shadow_prediction_failed", error=str(e))
```

---

## Kubernetes Deployment

### Model Serving Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-serving
  labels:
    app: model-serving
spec:
  replicas: 3
  selector:
    matchLabels:
      app: model-serving
  template:
    metadata:
      labels:
        app: model-serving
    spec:
      containers:
      - name: model-server
        image: model-serving:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        env:
        - name: MODEL_URI
          value: "s3://models/fraud-detection/v2.0"
        - name: MAX_BATCH_SIZE
          value: "32"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: model-serving
spec:
  selector:
    app: model-serving
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-serving-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-serving
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

---

## Batch Serving

### Spark Batch Inference

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf
import mlflow

def batch_inference(
    input_path: str,
    output_path: str,
    model_uri: str,
    date: str
):
    """Run batch inference on Spark."""

    spark = SparkSession.builder.appName("BatchInference").getOrCreate()

    # Load data
    df = spark.read.parquet(f"{input_path}/date={date}")

    # Load model as Spark UDF
    model = mlflow.pyfunc.spark_udf(spark, model_uri)

    # Define feature columns
    feature_cols = ["feature_1", "feature_2", "feature_3"]

    # Run predictions
    predictions_df = df.withColumn(
        "prediction",
        model(*[df[col] for col in feature_cols])
    )

    # Write results
    predictions_df.write.parquet(
        f"{output_path}/date={date}",
        mode="overwrite"
    )

    return predictions_df.count()
```

---

## Good Examples

### Example 1: Production-Ready Serving

```python
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram
import structlog

logger = structlog.get_logger()

# Metrics
PREDICTIONS = Counter(
    'predictions_total',
    'Total predictions',
    ['model_version', 'status']
)
LATENCY = Histogram(
    'prediction_latency_seconds',
    'Prediction latency',
    ['model_version']
)

app = FastAPI()

@app.post("/predict")
async def predict(request: PredictionRequest):
    start = time.time()

    try:
        result = model.predict(request.features)

        # Metrics
        PREDICTIONS.labels(model_version=VERSION, status="success").inc()
        LATENCY.labels(model_version=VERSION).observe(time.time() - start)

        # Logging
        logger.info("prediction_success",
            request_id=request.request_id,
            latency_ms=(time.time() - start) * 1000,
            model_version=VERSION
        )

        return {"prediction": result}

    except Exception as e:
        PREDICTIONS.labels(model_version=VERSION, status="error").inc()
        logger.error("prediction_failed",
            request_id=request.request_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Prediction failed")
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: No Health Checks

```python
# BAD - No way to know if model is loaded/healthy
@app.post("/predict")
def predict(data):
    return model.predict(data)  # May crash if model not loaded
```

**Correct approach:** Health and readiness endpoints.

---

### Anti-Pattern 2: Blocking Model Load

```python
# BAD - Loads model on every request
@app.post("/predict")
def predict(data):
    model = load_model("s3://models/latest")  # Slow!
    return model.predict(data)
```

**Correct approach:** Load model at startup, cache in memory.

---

## Quality Checklist

Before considering model serving complete:

### Reliability
- [ ] Health/readiness endpoints implemented
- [ ] Graceful shutdown handling
- [ ] Error handling with meaningful responses
- [ ] Circuit breakers for dependencies

### Performance
- [ ] Latency meets SLO (p99)
- [ ] Model optimized (ONNX, quantization if needed)
- [ ] Batching implemented if beneficial
- [ ] Load testing completed

### Observability
- [ ] Metrics exported (latency, throughput, errors)
- [ ] Structured logging with request IDs
- [ ] Model version tracked in responses
- [ ] Alerting configured

### Deployment
- [ ] Zero-downtime deployment possible
- [ ] Rollback procedure tested
- [ ] Canary/shadow deployment supported
- [ ] Auto-scaling configured

---

## Skill Interactions

### Preceded By
- **17-ML Pipeline** - Pipeline produces models to serve
- **18-Experiment Tracking** - Best experiments become serving models

### Followed By
- **20-ML Monitoring** - Monitor served model performance

### Related Skills
- **12-API Design** - Serving API design patterns
- **13-Observability** - Serving metrics and logging
