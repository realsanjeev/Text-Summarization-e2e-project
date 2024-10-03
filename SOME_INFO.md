# Developer Guide & Notes

This document contains technical details, troubleshooting tips, and explanations of specific design choices used in this project.

## 📦 Package Installation

The project is structured as a Python package. To install it in editable mode:

```bash
pip install -e .
```

If you encounter issues with the installation, you can try creating a source distribution:

```bash
python setup.py sdist
```

## 🔧 Configuration Management

We use `python-box` to manage configuration dictionaries as objects. This allows for cleaner code access using dot notation.

### Example: `ConfigBox`

```python
from box import ConfigBox

# Standard Dictionary
d = {"key": "value", "key1": "value1"}
# d.key  # Raises AttributeError

# ConfigBox
d_box = ConfigBox({"key": "value", "key1": "value1"})
print(d_box.key)  # Output: value
```

## 🛡️ Type Safety

We use the `@ensure_annotation` decorator to enforce type checking at runtime. This helps catch errors early, especially when dealing with configuration files and pipeline inputs.

### Example: `@ensure_annotation`

```python
from ensure import ensure_annotation

@ensure_annotation
def get_product(x: int, y: int) -> int:
    return x * y

get_product(2, 4)    # Works: 8
get_product(2, "4")  # Raises EnsureError
```

## 📝 Logging

Logs are stored in the `logs/` directory. Each run creates a new log file with a timestamp. This is crucial for debugging pipeline failures and tracking model training progress.

## 🏗️ Project Components

-   **Data Ingestion**: Downloads and extracts data.
-   **Data Validation**: Checks if required files exist.
-   **Data Transformation**: Tokenizes data for the model.
-   **Model Trainer**: Fine-tunes the Pegasus model.
-   **Model Evaluation**: Calculates ROUGE scores.
