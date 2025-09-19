# StreamTabs

**StreamTabs** is a Python package that provides a modular tab system for Streamlit applications. It allows you to organize your Streamlit apps into reusable, interconnected tabs with automatic data flow between them.

## Features

- 🏗️ **Modular Architecture**: Organize your Streamlit app into separate tab modules
- 🔄 **Inter-Tab Data Flow**: Pass data between tabs using `required_inputs` and `required_outputs`
- 🎯 **Clear Dependencies**: Explicitly declare what data each tab needs and provides
- 📊 **Sidebar Support**: Create reusable sidebar components
- 🎯 **Easy Integration**: Simple import and registration system
- 🐍 **Python 3.10+**: Modern Python support

## Installation

This project uses Poetry for dependency management:

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Quick Start

### 1. Create Your Tab Classes

Create tab files in `apps/tabs/`:

```python
# apps/tabs/my_tab.py
import streamlit as st
from streamtabs.core import STTab

class MyTab(STTab):
    class Meta:
        name = "my_tab"
        title = "My Tab"
        icon = "📊"
        order = 1
        required_inputs = []  # Inputs from other tabs
        required_outputs = ["my_data"]  # Data to pass to other tabs

    def render(self, **kwargs):
        """Render the tab UI and return outputs."""
        st.header("My Tab")
        # Your tab content here
        return {"my_data": "some_data"}
```

### 2. Create Sidebar Components (Optional)

Create sidebar files in `apps/sidebars/`:

```python
# apps/sidebars/my_sidebar.py
import streamlit as st
from streamtabs.core import STSidebar

class MySidebar(STSidebar):
    class Meta:
        name = "my_sidebar"

    def render(self):
        """Render the sidebar UI."""
        st.header("Configuration")
        # Your sidebar content here
        return {"config": "value"}
```

### 3. Register Components in Your App

```python
# app.py
import streamlit as st
from apps.sidebars import *  # noqa
from apps.tabs import *  # noqa
from streamtabs.core import STSidebar, STTab

st.set_page_config(page_title="My App", layout="wide")
st.title("My StreamTabs App")

STSidebar.run_sidebars()
STTab.run_tabs(debug=True)
```

## Example: Student Performance Evaluation

This repository includes a complete example demonstrating inter-tab data flow:

### Tab Structure

1. **📝 Exam 1 Input** (`exam1_input.py`)
   - Enter student names and Exam 1 marks
   - Outputs: `students_data`

2. **📊 Exam 2 Input** (`exam2_input.py`)
   - Displays Exam 1 data from previous tab
   - Add Exam 2 marks for each student
   - Inputs: `students_data`
   - Outputs: `updated_students_data`

3. **🏆 Results Summary** (`results_summary.py`)
   - Shows topper student and statistics
   - Displays performance charts
   - Inputs: `updated_students_data`

### Sidebar

- **⚙️ Exam Configuration** (`exam_config.py`)
  - Configure exam weights
  - App information and quick stats

### Running the Example

```bash
poetry run streamlit run app.py
```

## Tab Meta Configuration

Each tab class requires a `Meta` class with the following attributes:

- `name`: Unique identifier for the tab
- `title`: Display name in the tab header
- `icon`: Emoji or icon for the tab
- `order`: Display order (lower numbers appear first)
- `required_inputs`: List of input keys from other tabs
- `required_outputs`: List of output keys this tab provides

## Data Flow & Dependencies

StreamTabs uses explicit dependency declaration to ensure clear data flow between tabs. This approach provides several benefits:

### Benefits of Explicit Dependencies

- **🔍 Clear Data Contracts**: Know exactly what data each tab expects and provides
- **🚫 Error Prevention**: Automatic validation of data dependencies
- **📖 Self-Documenting**: Code clearly shows the relationship between tabs
- **🔧 Easy Debugging**: Missing dependencies are caught early with clear error messages

### How It Works

Tabs declare their dependencies using `required_inputs` and `required_outputs`:

```python
# Tab A: Data Producer
class DataProducerTab(STTab):
    class Meta:
        name = "producer"
        title = "Data Producer"
        required_inputs = []           # No dependencies
        required_outputs = ["raw_data", "metadata"]  # Provides two outputs

    def render(self, **kwargs):
        """Generate and return data."""
        raw_data = [1, 2, 3, 4, 5]
        metadata = {"count": len(raw_data), "type": "numbers"}
        
        return {
            "raw_data": raw_data,      # Available to other tabs
            "metadata": metadata       # Available to other tabs
        }

# Tab B: Data Consumer
class DataConsumerTab(STTab):
    class Meta:
        name = "consumer"
        title = "Data Consumer"
        required_inputs = ["raw_data"]     # Depends on raw_data from producer
        required_outputs = ["processed"]   # Provides processed data

    def render(self, raw_data, **kwargs):
        """Process data from producer tab."""
        # raw_data is automatically injected from DataProducerTab
        processed = [x * 2 for x in raw_data]
        
        return {"processed": processed}

# Tab C: Final Consumer
class FinalTab(STTab):
    class Meta:
        name = "final"
        title = "Final Results"
        required_inputs = ["raw_data", "processed"]  # Depends on both
        required_outputs = []                        # No outputs

    def render(self, raw_data, processed, **kwargs):
        """Display results from both previous tabs."""
        st.write("Original data:", raw_data)
        st.write("Processed data:", processed)
        # No return needed - this is a final display tab
```

### Dependency Resolution

StreamTabs automatically resolves dependencies by:

1. **📋 Analyzing Requirements**: Scans all tabs for their `required_inputs` and `required_outputs`
2. **🔗 Building Dependency Graph**: Creates a directed graph of data dependencies
3. **⚡ Executing in Order**: Runs tabs in the correct order to satisfy dependencies
4. **✅ Validating Data**: Ensures all required inputs are available before running a tab

### Error Handling

If dependencies can't be satisfied, StreamTabs provides clear error messages:

```python
# This will fail with a clear error message
class BrokenTab(STTab):
    class Meta:
        required_inputs = ["nonexistent_data"]  # This data doesn't exist!
    
    def render(self, nonexistent_data, **kwargs):
        # This will never be called due to missing dependency
        pass
```

### Best Practices

1. **🎯 Be Specific**: Only declare inputs you actually use
2. **📝 Document Outputs**: Use descriptive names for your outputs
3. **🔄 Keep It Simple**: Avoid circular dependencies
4. **🧪 Test Dependencies**: Verify your data flow works as expected

## Development

### Project Structure

```
streamtabs/
├── streamtabs/          # Core package
│   └── core/
│       └── core.py      # STTab and STSidebar classes
├── apps/                # Example applications
│   ├── tabs/            # Tab modules
│   └── sidebars/        # Sidebar modules
├── app.py              # Main Streamlit app
├── pyproject.toml      # Poetry configuration
└── README.md
```

### Adding New Tabs

1. Create a new file in `apps/tabs/`
2. Define your tab class inheriting from `STTab`
3. Import the tab in `apps/tabs/__init__.py`
4. The tab will be automatically registered when you run the app

### Adding New Sidebars

1. Create a new file in `apps/sidebars/`
2. Define your sidebar class inheriting from `STSidebar`
3. Import the sidebar in `apps/sidebars/__init__.py`
4. The sidebar will be automatically registered when you run the app

## Requirements

- Python 3.10+
- Streamlit >= 1.49.1
- Poetry (for dependency management)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For questions or issues, please open an issue on the GitHub repository.
