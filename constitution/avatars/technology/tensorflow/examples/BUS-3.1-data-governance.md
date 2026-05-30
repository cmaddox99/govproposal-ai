---
law_id: BUS-3.1
avatar: tensorflow
---

# BUS-3.1: Data Governance Examples for TensorFlow

## COMPLIANT: Model Registry with TensorFlow Serving Integration

```python
import tensorflow as tf
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class ModelRegistryEntry:
    """Metadata for a registered TensorFlow model."""

    model_name: str
    version: str
    model_hash: str
    created_at: str
    created_by: str
    training_data_version: str
    framework_version: str
    input_signature: Dict[str, Any]
    output_signature: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    metrics: Dict[str, float]
    serving_path: str
    tags: List[str]
    description: str


class TensorFlowModelRegistry:
    """Model registry with versioning and governance for TF Serving."""

    def __init__(self, registry_base_path: str):
        self.registry_base_path = Path(registry_base_path)
        self.registry_base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path = self.registry_base_path / 'metadata'
        self.metadata_path.mkdir(exist_ok=True)

    def compute_model_hash(self, model: tf.keras.Model) -> str:
        """Compute hash of model weights for integrity verification."""
        weight_bytes = b''
        for weight in model.get_weights():
            weight_bytes += weight.tobytes()
        return hashlib.sha256(weight_bytes).hexdigest()[:16]

    def get_signature_info(
        self,
        model: tf.keras.Model
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Extract input and output signature information."""
        input_sig = {}
        for i, input_spec in enumerate(model.input_spec or []):
            if input_spec:
                input_sig[f'input_{i}'] = {
                    'dtype': str(input_spec.dtype),
                    'shape': list(input_spec.shape) if input_spec.shape else None
                }

        output_sig = {
            'dtype': str(model.output.dtype),
            'shape': list(model.output.shape)
        }

        return input_sig, output_sig

    def register_model(
        self,
        model: tf.keras.Model,
        model_name: str,
        version: str,
        training_data_version: str,
        hyperparameters: Dict[str, Any],
        metrics: Dict[str, float],
        created_by: str,
        tags: Optional[List[str]] = None,
        description: str = ''
    ) -> ModelRegistryEntry:
        """Register a model with full governance metadata."""

        # Create versioned serving directory (TF Serving expects numeric versions)
        version_num = self._get_next_version_number(model_name)
        serving_path = self.registry_base_path / model_name / str(version_num)
        serving_path.mkdir(parents=True, exist_ok=True)

        # Save model in SavedModel format for TF Serving
        model.save(serving_path, save_format='tf')

        # Get signature information
        input_sig, output_sig = self.get_signature_info(model)

        # Create registry entry
        entry = ModelRegistryEntry(
            model_name=model_name,
            version=version,
            model_hash=self.compute_model_hash(model),
            created_at=datetime.utcnow().isoformat(),
            created_by=created_by,
            training_data_version=training_data_version,
            framework_version=tf.__version__,
            input_signature=input_sig,
            output_signature=output_sig,
            hyperparameters=hyperparameters,
            metrics=metrics,
            serving_path=str(serving_path),
            tags=tags or [],
            description=description
        )

        # Save metadata
        metadata_file = self.metadata_path / f"{model_name}_{version}.json"
        with open(metadata_file, 'w') as f:
            json.dump(asdict(entry), f, indent=2)

        # Also save metadata alongside model
        model_metadata_file = serving_path / 'metadata.json'
        with open(model_metadata_file, 'w') as f:
            json.dump(asdict(entry), f, indent=2)

        return entry

    def _get_next_version_number(self, model_name: str) -> int:
        """Get next numeric version for TF Serving compatibility."""
        model_dir = self.registry_base_path / model_name
        if not model_dir.exists():
            return 1

        existing_versions = [
            int(d.name) for d in model_dir.iterdir()
            if d.is_dir() and d.name.isdigit()
        ]

        return max(existing_versions, default=0) + 1

    def load_model(
        self,
        model_name: str,
        version: Optional[str] = None
    ) -> tuple[tf.keras.Model, ModelRegistryEntry]:
        """Load a model with metadata and integrity verification."""

        if version:
            metadata_file = self.metadata_path / f"{model_name}_{version}.json"
        else:
            # Get latest version
            metadata_files = list(self.metadata_path.glob(f"{model_name}_*.json"))
            metadata_file = max(metadata_files, key=lambda f: f.stat().st_mtime)

        with open(metadata_file) as f:
            entry_data = json.load(f)

        entry = ModelRegistryEntry(**entry_data)

        # Load model
        model = tf.keras.models.load_model(entry.serving_path)

        # Verify integrity
        current_hash = self.compute_model_hash(model)
        if current_hash != entry.model_hash:
            raise ValueError(
                f"Model integrity check failed. "
                f"Expected {entry.model_hash}, got {current_hash}"
            )

        return model, entry

    def list_models(
        self,
        model_name: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[ModelRegistryEntry]:
        """List registered models with optional filtering."""
        entries = []

        for metadata_file in self.metadata_path.glob('*.json'):
            with open(metadata_file) as f:
                entry_data = json.load(f)

            if model_name and entry_data['model_name'] != model_name:
                continue

            if tags and not all(t in entry_data['tags'] for t in tags):
                continue

            entries.append(ModelRegistryEntry(**entry_data))

        return sorted(entries, key=lambda e: e.created_at, reverse=True)

    def promote_to_production(
        self,
        model_name: str,
        version: str,
        promoted_by: str
    ) -> None:
        """Promote a model version to production with audit trail."""
        metadata_file = self.metadata_path / f"{model_name}_{version}.json"

        with open(metadata_file) as f:
            entry_data = json.load(f)

        # Add promotion metadata
        entry_data['promoted_to_production'] = True
        entry_data['promoted_at'] = datetime.utcnow().isoformat()
        entry_data['promoted_by'] = promoted_by

        with open(metadata_file, 'w') as f:
            json.dump(entry_data, f, indent=2)

        # Create symlink for production serving
        production_link = self.registry_base_path / model_name / 'production'
        if production_link.exists():
            production_link.unlink()

        production_link.symlink_to(entry_data['serving_path'])
```

**Why compliant:** Models are saved in TF Serving compatible format with versioning. Comprehensive metadata includes data lineage, hyperparameters, and metrics. Integrity verification through model hash comparison. Production promotion creates audit trail. Input/output signatures are captured for API governance.

---

## VIOLATION: Saving Models Without Registry

```python
import tensorflow as tf


def save_model(model: tf.keras.Model, name: str) -> None:
    """Save model without governance metadata."""
    # Save without versioning
    model.save(f'models/{name}')

    # No record of:
    # - Training data version
    # - Hyperparameters used
    # - Metrics achieved
    # - Who created the model
    # - When it was created


def deploy_model(model_path: str) -> None:
    """Deploy model without governance checks."""
    # Load without verification
    model = tf.keras.models.load_model(model_path)

    # No integrity check
    # No lineage information
    # No approval workflow

    # Copy to serving directory
    shutil.copy(model_path, '/serving/model')


def update_production_model(new_model_path: str) -> None:
    """Update production without audit trail."""
    # Overwrite production model
    shutil.rmtree('/serving/model', ignore_errors=True)
    shutil.copytree(new_model_path, '/serving/model')

    # Previous version is lost
    # No rollback capability
    # No record of change
```

**Why violates BUS-3.1:** Models are saved without any metadata or versioning. No record of training data or hyperparameters. Production updates lack audit trail. Previous versions are overwritten without history. No integrity verification on load.

---

## COMPLIANT: TFX Pipeline with Data Lineage Tracking

```python
import tensorflow as tf
import tensorflow_data_validation as tfdv
import tensorflow_transform as tft
from tfx import v1 as tfx
from tfx.types import standard_artifacts
from typing import Dict, Any, List
import json
from datetime import datetime


class DataLineageTracker:
    """Track data transformations in TFX pipeline."""

    def __init__(self, metadata_store_path: str):
        self.metadata_store_path = metadata_store_path
        self.lineage_records = []

    def record_transformation(
        self,
        input_artifact: standard_artifacts.Examples,
        output_artifact: standard_artifacts.Examples,
        transformation_name: str,
        transformation_config: Dict[str, Any],
        executed_by: str
    ) -> Dict[str, Any]:
        """Record a data transformation with full lineage."""

        record = {
            'transformation_id': f"{transformation_name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'transformation_name': transformation_name,
            'input_uri': input_artifact.uri,
            'output_uri': output_artifact.uri,
            'transformation_config': transformation_config,
            'executed_at': datetime.utcnow().isoformat(),
            'executed_by': executed_by,
            'input_statistics': self._compute_statistics(input_artifact),
            'output_statistics': self._compute_statistics(output_artifact)
        }

        self.lineage_records.append(record)
        self._persist_record(record)

        return record

    def _compute_statistics(
        self,
        artifact: standard_artifacts.Examples
    ) -> Dict[str, Any]:
        """Compute statistics for data governance."""
        stats = tfdv.generate_statistics_from_tfrecord(artifact.uri)

        return {
            'num_examples': stats.datasets[0].num_examples,
            'features': [
                {
                    'name': f.path.step[0],
                    'type': str(f.type),
                    'num_missing': f.num_missing
                }
                for f in stats.datasets[0].features
            ]
        }

    def _persist_record(self, record: Dict[str, Any]) -> None:
        """Persist lineage record."""
        record_file = f"{self.metadata_store_path}/lineage_{record['transformation_id']}.json"
        with open(record_file, 'w') as f:
            json.dump(record, f, indent=2)


class GovernedTFXPipeline:
    """TFX pipeline with data governance integration."""

    def __init__(
        self,
        pipeline_name: str,
        pipeline_root: str,
        data_version: str,
        owner: str
    ):
        self.pipeline_name = pipeline_name
        self.pipeline_root = pipeline_root
        self.data_version = data_version
        self.owner = owner
        self.lineage_tracker = DataLineageTracker(
            f"{pipeline_root}/metadata"
        )

    def create_pipeline(self) -> tfx.dsl.Pipeline:
        """Create TFX pipeline with governance tracking."""

        # Data ingestion with version tracking
        example_gen = tfx.components.CsvExampleGen(
            input_base=f"data/{self.data_version}"
        )

        # Statistics generation for data governance
        statistics_gen = tfx.components.StatisticsGen(
            examples=example_gen.outputs['examples']
        )

        # Schema inference with versioning
        schema_gen = tfx.components.SchemaGen(
            statistics=statistics_gen.outputs['statistics']
        )

        # Data validation for governance
        example_validator = tfx.components.ExampleValidator(
            statistics=statistics_gen.outputs['statistics'],
            schema=schema_gen.outputs['schema']
        )

        # Transform with lineage tracking
        transform = tfx.components.Transform(
            examples=example_gen.outputs['examples'],
            schema=schema_gen.outputs['schema'],
            module_file='transform_module.py'
        )

        # Trainer with hyperparameter tracking
        trainer = tfx.components.Trainer(
            module_file='trainer_module.py',
            examples=transform.outputs['transformed_examples'],
            transform_graph=transform.outputs['transform_graph'],
            schema=schema_gen.outputs['schema'],
            train_args=tfx.proto.TrainArgs(num_steps=10000),
            eval_args=tfx.proto.EvalArgs(num_steps=1000)
        )

        # Model evaluation with metrics tracking
        evaluator = tfx.components.Evaluator(
            examples=example_gen.outputs['examples'],
            model=trainer.outputs['model'],
            eval_config=self._get_eval_config()
        )

        # Model pusher with approval gate
        pusher = tfx.components.Pusher(
            model=trainer.outputs['model'],
            model_blessing=evaluator.outputs['blessing'],
            push_destination=tfx.proto.PushDestination(
                filesystem=tfx.proto.PushDestination.Filesystem(
                    base_directory=f"{self.pipeline_root}/serving"
                )
            )
        )

        # Record pipeline metadata
        self._record_pipeline_run(
            components=[
                example_gen, statistics_gen, schema_gen,
                example_validator, transform, trainer,
                evaluator, pusher
            ]
        )

        return tfx.dsl.Pipeline(
            pipeline_name=self.pipeline_name,
            pipeline_root=self.pipeline_root,
            components=[
                example_gen, statistics_gen, schema_gen,
                example_validator, transform, trainer,
                evaluator, pusher
            ],
            metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(
                f"{self.pipeline_root}/metadata.db"
            )
        )

    def _get_eval_config(self):
        """Get evaluation config with governance thresholds."""
        return tfx.proto.EvalConfig(
            model_specs=[
                tfx.proto.ModelSpec(label_key='label')
            ],
            slicing_specs=[
                tfx.proto.SlicingSpec()
            ],
            metrics_specs=[
                tfx.proto.MetricsSpec(
                    metrics=[
                        tfx.proto.MetricConfig(
                            class_name='BinaryAccuracy',
                            threshold=tfx.proto.MetricThreshold(
                                value_threshold=tfx.proto.GenericValueThreshold(
                                    lower_bound={'value': 0.8}
                                )
                            )
                        )
                    ]
                )
            ]
        )

    def _record_pipeline_run(self, components: List) -> None:
        """Record pipeline run metadata for governance."""
        run_record = {
            'pipeline_name': self.pipeline_name,
            'data_version': self.data_version,
            'owner': self.owner,
            'run_timestamp': datetime.utcnow().isoformat(),
            'components': [c.__class__.__name__ for c in components],
            'tensorflow_version': tf.__version__
        }

        with open(f"{self.pipeline_root}/run_metadata.json", 'w') as f:
            json.dump(run_record, f, indent=2)
```

**Why compliant:** TFX pipeline provides built-in lineage tracking through ML Metadata. Data validation ensures data quality governance. Schema versioning tracks data structure changes. Model evaluation gates prevent poor models from deployment. Full audit trail of pipeline runs with metadata.

---

## VIOLATION: Ad-hoc Pipeline Without Lineage

```python
import tensorflow as tf
import pandas as pd


def train_model_pipeline():
    """Training pipeline without governance."""
    # Load data without version tracking
    df = pd.read_csv('data/train.csv')

    # Transform without recording
    df = df.dropna()
    df['feature_normalized'] = (df['feature'] - df['feature'].mean()) / df['feature'].std()

    # Build dataset without schema tracking
    dataset = tf.data.Dataset.from_tensor_slices(
        (df[['feature_normalized']].values, df['label'].values)
    )

    # Create model without hyperparameter tracking
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy')

    # Train without metrics logging
    model.fit(dataset.batch(32), epochs=10)

    # Save without lineage
    model.save('model')

    # No record of:
    # - Data transformations applied
    # - Schema of input data
    # - Hyperparameters used
    # - Training metrics
    # - Data version


def update_model():
    """Update model without governance."""
    # Previous model is just overwritten
    train_model_pipeline()
```

**Why violates BUS-3.1:** No data version tracking or schema management. Transformations are not recorded for reproducibility. No lineage between data, transformations, and model. Training metrics are not persisted. Previous models are overwritten without history.
