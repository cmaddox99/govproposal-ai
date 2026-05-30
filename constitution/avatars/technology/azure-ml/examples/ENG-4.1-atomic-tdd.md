---
law_id: ENG-4.1
avatar: azure-ml
---

# ENG-4.1: Atomic TDD Examples for Azure Machine Learning

## COMPLIANT: TDD Cycle with pytest for Azure ML Training

```python
# test_azure_trainer.py

# Step 1: RED - Write failing test
def test_trainer_submits_job_with_correct_compute_target():
    # GIVEN
    trainer = AzureMLTrainer(
        workspace=MockWorkspace(),
        experiment_name="test-experiment"
    )
    config = TrainingConfig(
        compute_target="gpu-cluster",
        environment_name="pytorch-env"
    )

    # WHEN
    job = trainer.submit_training(
        script_path="train.py",
        config=config
    )

    # THEN
    assert job.compute_target == "gpu-cluster"
    assert job.status == JobStatus.SUBMITTED


# Step 2: GREEN - Write minimum code (in azure_trainer.py)
class AzureMLTrainer:
    def submit_training(self, script_path: str, config: TrainingConfig) -> Job:
        command = command(
            code="./src",
            command=f"python {script_path}",
            compute=config.compute_target,
            environment=config.environment_name
        )
        return Job(
            compute_target=config.compute_target,
            status=JobStatus.SUBMITTED
        )


# Step 3: REFACTOR - Extract environment resolution
class AzureMLTrainer:
    def submit_training(self, script_path: str, config: TrainingConfig) -> Job:
        environment = self._resolve_environment(config.environment_name)
        command_job = self._build_command_job(script_path, config, environment)
        return self._submit_job(command_job)

    def _resolve_environment(self, name: str) -> Environment:
        return self._ml_client.environments.get(name, label="latest")


# Step 4: Commit, then write NEXT test
def test_trainer_registers_model_after_successful_run():
    # Next TDD cycle for model registration...
    pass
```

**Why compliant:** One test at a time, minimal code to pass, refactor continuously.

---

## VIOLATION: Testing Azure ML Components Without Isolation

```python
# BAD: Tests that depend on actual Azure resources
def test_training_pipeline():
    # VIOLATION: Requires actual Azure workspace
    ml_client = MLClient.from_config()

    # VIOLATION: Uses real compute that costs money
    job = ml_client.jobs.create_or_update(
        command(
            code="./src",
            command="python train.py",
            compute="expensive-gpu-cluster",
            environment="pytorch-curated:latest"
        )
    )

    # VIOLATION: Waits for actual job completion
    ml_client.jobs.stream(job.name)

    # VIOLATION: Tests multiple things at once
    assert job.status == "Completed"
    assert job.outputs["model"] is not None
    assert job.metrics["accuracy"] > 0.9

# BAD: No mocking of Azure ML SDK
def test_model_deployment():
    ml_client = MLClient.from_config()

    # VIOLATION: Deploys to real endpoint
    endpoint = ml_client.online_endpoints.begin_create_or_update(
        OnlineEndpoint(name="prod-endpoint")
    ).result()

    # Tests production infrastructure in unit tests
    assert endpoint.provisioning_state == "Succeeded"
```

**Why violates ENG-4.1:** Tests multiple behaviors at once, depends on real infrastructure, no isolation, expensive to run, and non-deterministic results.

---

## TDD Cycle Commands for Azure ML

```bash
# RED: Run test, see it fail
pytest tests/training/test_trainer.py::test_trainer_submits_job -v

# GREEN: Write code, run test again
pytest tests/training/test_trainer.py::test_trainer_submits_job -v

# REFACTOR: Run all tests after refactoring
pytest tests/ -m "not integration"

# Integration tests (separate from TDD cycle)
pytest tests/integration/ --run-azure -v

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add job submission to AzureMLTrainer"
```
