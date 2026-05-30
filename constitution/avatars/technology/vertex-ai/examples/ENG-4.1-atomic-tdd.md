---
law_id: ENG-4.1
avatar: vertex-ai
---

# ENG-4.1: Atomic TDD Examples for Google Vertex AI

## COMPLIANT: TDD Cycle with pytest for Vertex AI Training

```python
# test_vertex_trainer.py

# Step 1: RED - Write failing test
def test_trainer_creates_custom_job_with_correct_machine_type():
    # GIVEN
    trainer = VertexTrainer(
        project="test-project",
        location="us-central1",
        staging_bucket="gs://test-bucket"
    )
    config = TrainingConfig(
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1
    )

    # WHEN
    job = trainer.create_training_job(
        display_name="test-job",
        script_path="train.py",
        config=config
    )

    # THEN
    assert job.machine_type == "n1-standard-4"
    assert job.accelerator_type == "NVIDIA_TESLA_T4"


# Step 2: GREEN - Write minimum code (in vertex_trainer.py)
@dataclass
class TrainingJob:
    display_name: str
    machine_type: str
    accelerator_type: str
    accelerator_count: int

class VertexTrainer:
    def create_training_job(
        self,
        display_name: str,
        script_path: str,
        config: TrainingConfig
    ) -> TrainingJob:
        return TrainingJob(
            display_name=display_name,
            machine_type=config.machine_type,
            accelerator_type=config.accelerator_type,
            accelerator_count=config.accelerator_count
        )


# Step 3: REFACTOR - Add proper Vertex AI SDK integration
class VertexTrainer:
    def __init__(self, project: str, location: str, staging_bucket: str):
        self._project = project
        self._location = location
        self._staging_bucket = staging_bucket

    def create_training_job(
        self,
        display_name: str,
        script_path: str,
        config: TrainingConfig
    ) -> TrainingJob:
        worker_pool = self._build_worker_pool(config)
        return TrainingJob(
            display_name=display_name,
            worker_pools=[worker_pool]
        )

    def _build_worker_pool(self, config: TrainingConfig) -> dict:
        return {
            "machine_spec": {
                "machine_type": config.machine_type,
                "accelerator_type": config.accelerator_type,
                "accelerator_count": config.accelerator_count
            }
        }


# Step 4: Commit, then write NEXT test
def test_trainer_uploads_training_script_to_gcs():
    # Next TDD cycle for script upload...
    pass
```

**Why compliant:** One test at a time, minimal code to pass, refactor continuously.

---

## VIOLATION: Testing with Live Vertex AI Resources

```python
# BAD: Tests that require actual GCP resources
from google.cloud import aiplatform

def test_full_training_pipeline():
    # VIOLATION: Initializes against real project
    aiplatform.init(project="prod-project", location="us-central1")

    # VIOLATION: Creates real custom job (costs money)
    job = aiplatform.CustomJob(
        display_name="test-job",
        worker_pool_specs=[{
            "machine_spec": {
                "machine_type": "n1-standard-4",
                "accelerator_type": "NVIDIA_TESLA_T4",
                "accelerator_count": 1
            },
            "python_package_spec": {
                "executor_image_uri": "gcr.io/...",
                "package_uris": ["gs://bucket/training.tar.gz"],
                "python_module": "trainer.task"
            }
        }]
    )

    # VIOLATION: Runs actual training (expensive, slow)
    job.run(sync=True)

    # VIOLATION: Tests multiple behaviors
    assert job.state == "SUCCEEDED"
    assert job.end_time is not None


# BAD: Integration test without mocking
def test_model_deployment():
    # VIOLATION: Uploads to real Model Registry
    model = aiplatform.Model.upload(
        display_name="test-model",
        artifact_uri="gs://bucket/model/"
    )

    # VIOLATION: Creates real endpoint (costs money even when idle)
    endpoint = aiplatform.Endpoint.create(display_name="test-endpoint")

    # VIOLATION: Deploys to real infrastructure
    model.deploy(endpoint=endpoint, machine_type="n1-standard-2")

    # Flaky: depends on deployment timing
    assert endpoint.traffic_split is not None
```

**Why violates ENG-4.1:** Tests against real GCP infrastructure, incurs costs, slow to run, tests multiple behaviors, non-deterministic.

---

## TDD Cycle Commands for Vertex AI

```bash
# RED: Run test, see it fail
pytest tests/training/test_vertex_trainer.py::test_trainer_creates_custom_job -v

# GREEN: Write code, run test again
pytest tests/training/test_vertex_trainer.py::test_trainer_creates_custom_job -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration" -v

# Integration tests (separate, with GCP credentials)
pytest tests/integration/ --run-gcp -v

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add custom job creation to VertexTrainer"
```
