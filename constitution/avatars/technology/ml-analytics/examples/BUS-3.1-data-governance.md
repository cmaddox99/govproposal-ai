---
law_id: BUS-3.1
avatar: ml-analytics
---

# BUS-3.1: Data Governance Examples for ML Analytics

## COMPLIANT: Data Lineage Tracking with Metadata

```python
import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import pandas as pd


@dataclass
class DataLineageRecord:
    """Record tracking data transformations and provenance."""

    dataset_id: str
    version: str
    source_datasets: List[str]
    transformation: str
    created_at: str
    created_by: str
    row_count: int
    column_count: int
    schema_hash: str
    parameters: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DataLineageTracker:
    """Track data provenance and transformations for ML pipelines."""

    def __init__(self, lineage_store_path: str):
        self.lineage_store_path = lineage_store_path
        self.lineage_records: List[DataLineageRecord] = []

    def compute_schema_hash(self, df: pd.DataFrame) -> str:
        """Generate deterministic hash of DataFrame schema."""
        schema_str = json.dumps({
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }, sort_keys=True)
        return hashlib.sha256(schema_str.encode()).hexdigest()[:16]

    def register_dataset(
        self,
        df: pd.DataFrame,
        dataset_id: str,
        version: str,
        source_datasets: List[str],
        transformation: str,
        created_by: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> DataLineageRecord:
        """Register a dataset with full lineage information."""
        record = DataLineageRecord(
            dataset_id=dataset_id,
            version=version,
            source_datasets=source_datasets,
            transformation=transformation,
            created_at=datetime.utcnow().isoformat(),
            created_by=created_by,
            row_count=len(df),
            column_count=len(df.columns),
            schema_hash=self.compute_schema_hash(df),
            parameters=parameters or {}
        )

        self.lineage_records.append(record)
        self._persist_record(record)

        return record

    def _persist_record(self, record: DataLineageRecord) -> None:
        """Persist lineage record to storage."""
        with open(self.lineage_store_path, 'a') as f:
            f.write(json.dumps(record.to_dict()) + '\n')

    def get_upstream_lineage(self, dataset_id: str) -> List[DataLineageRecord]:
        """Trace complete upstream lineage for a dataset."""
        lineage = []
        visited = set()
        queue = [dataset_id]

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            for record in self.lineage_records:
                if record.dataset_id == current_id:
                    lineage.append(record)
                    queue.extend(record.source_datasets)

        return lineage


# Usage in ML pipeline
def create_training_dataset(
    raw_df: pd.DataFrame,
    lineage_tracker: DataLineageTracker,
    analyst_id: str
) -> pd.DataFrame:
    """Create training dataset with full lineage tracking."""

    # Step 1: Clean data
    cleaned_df = raw_df.dropna(subset=['target'])
    lineage_tracker.register_dataset(
        df=cleaned_df,
        dataset_id='training_data_cleaned',
        version='1.0.0',
        source_datasets=['raw_sales_data_v2'],
        transformation='dropna_target_column',
        created_by=analyst_id,
        parameters={'subset': ['target']}
    )

    # Step 2: Feature engineering
    features_df = cleaned_df.copy()
    features_df['revenue_per_unit'] = (
        features_df['revenue'] / features_df['units_sold']
    )
    features_df['log_revenue'] = features_df['revenue'].apply(np.log1p)

    lineage_tracker.register_dataset(
        df=features_df,
        dataset_id='training_data_features',
        version='1.0.0',
        source_datasets=['training_data_cleaned'],
        transformation='add_derived_features',
        created_by=analyst_id,
        parameters={
            'new_features': ['revenue_per_unit', 'log_revenue']
        }
    )

    return features_df
```

**Why compliant:** Every dataset transformation is recorded with full provenance metadata. Source datasets are explicitly tracked enabling upstream lineage queries. Schema hashes provide integrity verification. Transformation parameters are captured for reproducibility. The lineage store provides an audit trail for compliance.

---

## VIOLATION: Data Transformation Without Lineage Tracking

```python
import pandas as pd
import numpy as np


def prepare_ml_data(filepath: str) -> pd.DataFrame:
    """Prepare data for ML training without any tracking."""
    # Load data from unknown source
    df = pd.read_csv(filepath)

    # Apply transformations without documentation
    df = df.dropna()
    df = df[df['value'] > 0]
    df['normalized'] = (df['value'] - df['value'].mean()) / df['value'].std()

    # Merge with another dataset
    other_df = pd.read_csv('supplementary_data.csv')
    df = df.merge(other_df, on='id', how='left')

    # Filter based on business rules
    df = df[df['category'].isin(['A', 'B', 'C'])]

    # Save without versioning
    df.to_csv('prepared_data.csv', index=False)

    return df


def train_model(data_path: str):
    """Train model on data with no provenance information."""
    df = pd.read_csv(data_path)

    # No record of which version of data was used
    # No tracking of transformations applied
    # No audit trail for compliance

    X = df.drop('target', axis=1)
    y = df['target']

    model = train_random_forest(X, y)

    # Save model without linking to data version
    save_model(model, 'model.pkl')
```

**Why violates BUS-3.1:** No lineage tracking for data transformations. Source datasets are not recorded or versioned. Transformation logic is not documented or parameterized. No audit trail exists for compliance requirements. Model training is not linked to specific data versions. Cannot reproduce or trace data provenance.

---

## COMPLIANT: Dataset Versioning with DVC Integration

```python
import subprocess
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd


class DataVersionController:
    """Manage dataset versions with DVC and metadata tracking."""

    def __init__(self, repo_path: str, metadata_path: str):
        self.repo_path = Path(repo_path)
        self.metadata_path = Path(metadata_path)
        self.metadata_path.mkdir(parents=True, exist_ok=True)

    def compute_data_hash(self, df: pd.DataFrame) -> str:
        """Compute deterministic hash of DataFrame contents."""
        # Use pandas hash for content-based versioning
        content_hash = hashlib.sha256(
            pd.util.hash_pandas_object(df).values.tobytes()
        ).hexdigest()
        return content_hash[:16]

    def version_dataset(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        description: str,
        created_by: str,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Version a dataset with full metadata tracking."""

        # Compute content hash for version
        content_hash = self.compute_data_hash(df)
        version_id = f"v_{content_hash}"

        # Save dataset
        data_path = self.repo_path / f"{dataset_name}_{version_id}.parquet"
        df.to_parquet(data_path, index=False)

        # Create metadata record
        metadata = {
            'dataset_name': dataset_name,
            'version_id': version_id,
            'content_hash': content_hash,
            'created_at': datetime.utcnow().isoformat(),
            'created_by': created_by,
            'description': description,
            'row_count': len(df),
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'file_path': str(data_path),
            'tags': tags or {},
            'statistics': self._compute_statistics(df)
        }

        # Save metadata
        metadata_file = self.metadata_path / f"{dataset_name}_{version_id}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        # Track with DVC
        self._dvc_add(data_path)

        return metadata

    def _compute_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute summary statistics for governance reporting."""
        stats = {
            'numeric_columns': {},
            'categorical_columns': {}
        }

        for col in df.select_dtypes(include=[np.number]).columns:
            stats['numeric_columns'][col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'null_count': int(df[col].isna().sum())
            }

        for col in df.select_dtypes(include=['object', 'category']).columns:
            stats['categorical_columns'][col] = {
                'unique_count': int(df[col].nunique()),
                'null_count': int(df[col].isna().sum()),
                'top_values': df[col].value_counts().head(5).to_dict()
            }

        return stats

    def _dvc_add(self, file_path: Path) -> None:
        """Add file to DVC tracking."""
        subprocess.run(
            ['dvc', 'add', str(file_path)],
            cwd=self.repo_path,
            check=True,
            capture_output=True
        )

    def get_dataset_version(
        self,
        dataset_name: str,
        version_id: str
    ) -> pd.DataFrame:
        """Retrieve a specific version of a dataset."""
        metadata_file = self.metadata_path / f"{dataset_name}_{version_id}.json"

        with open(metadata_file) as f:
            metadata = json.load(f)

        return pd.read_parquet(metadata['file_path'])

    def list_versions(self, dataset_name: str) -> List[Dict[str, Any]]:
        """List all versions of a dataset."""
        versions = []
        for metadata_file in self.metadata_path.glob(f"{dataset_name}_v_*.json"):
            with open(metadata_file) as f:
                versions.append(json.load(f))

        return sorted(versions, key=lambda x: x['created_at'], reverse=True)
```

**Why compliant:** Datasets are versioned using content-based hashing for deterministic versioning. Full metadata is captured including schema, statistics, and provenance. DVC integration provides robust version control for large datasets. Historical versions can be retrieved exactly as they were. Audit trail supports compliance and reproducibility requirements.

---

## VIOLATION: Overwriting Data Without Version Control

```python
import pandas as pd


def update_training_data(new_data_path: str) -> None:
    """Update training data by overwriting existing file."""
    # Load new data
    new_df = pd.read_csv(new_data_path)

    # Load and append to existing data
    existing_df = pd.read_csv('training_data.csv')
    combined_df = pd.concat([existing_df, new_df])

    # Remove duplicates
    combined_df = combined_df.drop_duplicates()

    # Overwrite existing file - previous version is lost
    combined_df.to_csv('training_data.csv', index=False)

    print(f"Updated training data with {len(new_df)} new records")


def fix_data_quality_issue() -> None:
    """Fix data quality issue by modifying data in place."""
    df = pd.read_csv('training_data.csv')

    # Apply fix without tracking what changed
    df.loc[df['value'] < 0, 'value'] = 0

    # Overwrite - no history of the change
    df.to_csv('training_data.csv', index=False)


def sample_for_testing() -> pd.DataFrame:
    """Create test sample without versioning."""
    df = pd.read_csv('training_data.csv')

    # Random sample - not reproducible
    sample = df.sample(n=1000)

    # No record of which rows were sampled
    return sample
```

**Why violates BUS-3.1:** Files are overwritten without preserving previous versions. No record of what data changed or why. Changes cannot be audited or rolled back. Random sampling is not reproducible without seed tracking. No metadata captures the state of data at any point in time.
