# Project Structure and Organization Guidelines

This document outlines the organized directory structure for the Speaker Diarization project and provides guidelines for maintaining consistency in future development.

## 📁 Directory Structure

```
WhisprMate/
├── 📄 main.py                           # Main Streamlit application entry point
├── 📄 pyproject.toml                    # Project configuration and dependencies
├── 📄 requirements.txt                  # Python dependencies
├── 📄 README.md                         # Project overview and quick start
├── 📄 LICENSE                           # Project license
├── 📄 .env                              # Environment variables (HuggingFace token, etc.)
├── 📄 .gitignore                        # Git ignore rules
│
├── 📁 config/                           # Application configuration
│   ├── 📄 __init__.py
│   └── 📄 settings.py                   # Configuration classes and constants
│
├── 📁 src/                              # Source code (main application logic)
│   ├── 📄 __init__.py
│   ├── 📁 core/                         # Domain layer (business logic)
│   │   ├── 📄 __init__.py
│   │   └── 📄 models.py                 # Domain models and interfaces
│   ├── 📁 services/                     # Service layer (business logic implementation)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 audio_processor.py        # Audio processing service
│   │   ├── 📄 auth_service.py           # Authentication service
│   │   ├── 📄 file_manager.py           # File management service
│   │   └── 📄 transcript_manager.py     # Transcript management service
│   ├── 📁 ui/                           # Presentation layer
│   │   ├── 📄 __init__.py
│   │   ├── 📁 components/               # Reusable UI components
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py               # Authentication components
│   │   │   └── 📄 file_components.py    # File management components
│   │   └── 📁 pages/                    # Page-level components (future use)
│   │       └── 📄 __init__.py
│   └── 📁 utils/                        # Utility functions
│       ├── 📄 __init__.py
│       └── 📄 helpers.py                # Helper functions
│
├── 📁 tests/                            # Test suite
│   ├── 📄 __init__.py
│   ├── 📁 unit/                         # Unit tests for individual components
│   │   ├── 📄 __init__.py
│   │   └── 📄 test_auth_service.py      # Authentication service tests
│   └── 📁 integration/                  # End-to-end integration tests
│       └── 📄 __init__.py
│
├── 📁 scripts/                          # Utility scripts and tools
│   ├── 📄 diarize_cli_improved.py       # CLI tool for speaker diarization
│   └── 📄 run_with_custom_auth.sh       # Authentication demo script
│
├── 📁 static/                           # Static assets (HTML, CSS, JS)
│   └── 📄 player.html                   # Web player for audio/transcript viewing
│
├── 📁 data/                             # Data files and samples
│   └── 📁 samples/                      # Sample data files
│       └── 📄 real_diarized_output.srt  # Example output file
│
├── 📁 uploads/                          # User uploaded files (runtime)
│   └── 📄 .gitkeep                      # Keep directory in git
│
├── 📁 templates/                        # Template files (if needed)
│   └── 📄 .gitkeep                      # Keep directory in git
│
├── 📁 docs/                             # Project documentation
│   ├── 📄 README.md                     # Documentation index
│   ├── 📄 AUTHENTICATION.md             # Authentication setup guide
│   ├── 📄 PROJECT_STRUCTURE.md          # This file
│   ├── 📁 architecture/                 # Technical architecture docs
│   │   ├── 📄 ARCHITECTURE.md           # Architecture overview
│   │   └── 📄 REFACTORING_SUMMARY.md    # Refactoring changes
│   ├── 📁 development/                  # Development guidelines
│   │   ├── 📄 CONTRIBUTING.md           # Contribution guidelines
│   │   └── 📄 CODE_OF_CONDUCT.md        # Code of conduct
│   └── 📁 project/                      # Project management docs
│       ├── 📄 summary.md                # Project summary
│       ├── 📄 plan.md                   # Development roadmap
│       └── 📄 UI_IMPROVEMENTS.md        # UI/UX improvements
│
└── 📁 venv/                             # Python virtual environment (excluded from git)
```

## 🎯 Organization Principles

### 1. **Separation by Function**

- **`src/`**: All application source code
- **`tests/`**: All test files
- **`scripts/`**: Utility scripts and CLI tools
- **`docs/`**: All documentation
- **`static/`**: Static web assets
- **`data/`**: Data files and samples

### 2. **Layer-Based Architecture**

Following clean architecture principles:

- **`src/core/`**: Domain layer (business entities and interfaces)
- **`src/services/`**: Service layer (business logic implementation)
- **`src/ui/`**: Presentation layer (user interface components)
- **`src/utils/`**: Cross-cutting utilities

### 3. **Test Organization**

- **`tests/unit/`**: Unit tests for individual components
- **`tests/integration/`**: End-to-end integration tests
- Tests mirror the source structure for easy navigation

## 📋 File Naming Conventions

### Python Files

- **Classes**: `PascalCase` (e.g., `AudioProcessorService`)
- **Functions/Variables**: `snake_case` (e.g., `process_audio_file`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE_MB`)
- **Module Names**: `snake_case` (e.g., `audio_processor.py`)

### Test Files

- **Unit Tests**: `test_<module_name>.py` (e.g., `test_auth_service.py`)
- **Integration Tests**: `test_<feature>_integration.py`

### Documentation Files

- **README files**: `README.md`
- **Feature docs**: `FEATURE_NAME.md` (e.g., `AUTHENTICATION.md`)
- **Architecture docs**: Use descriptive names (e.g., `ARCHITECTURE.md`)

## 🔄 Development Workflow Guidelines

### Adding New Features

1. **Create Service Class** in `src/services/`
2. **Define Interface** in `src/core/models.py`
3. **Add UI Components** in `src/ui/components/`
4. **Write Unit Tests** in `tests/unit/`
5. **Update Documentation** in `docs/`

### Adding New Scripts

1. **Place in `scripts/`** directory
2. **Make executable** with `chmod +x`
3. **Add documentation** in script header
4. **Update README** with usage instructions

### Adding Static Assets

1. **Place in `static/`** directory
2. **Organize by type** (css/, js/, images/, etc.)
3. **Reference correctly** from application code

## 🚨 Important Rules

### What Goes Where

- **Never** put business logic in UI components
- **Always** use dependency injection for services
- **Keep** configuration in `config/` directory
- **Place** all tests in `tests/` directory
- **Store** documentation in `docs/` directory

### Git Ignore Guidelines

- **Include** in `.gitignore`:
  - `venv/` (virtual environment)
  - `__pycache__/` (Python cache)
  - `.env` (environment variables)
  - `uploads/` contents (user files)
- **Never ignore** configuration templates or sample files

### Import Guidelines

- **Use absolute imports** from project root
- **Import interfaces** from `src.core.models`
- **Import services** from `src.services`
- **Import utilities** from `src.utils`

## 📈 Future Expansion

When adding new functionality:

1. **Follow the existing structure**
2. **Create new service** if adding business logic
3. **Add corresponding tests**
4. **Update documentation**
5. **Consider configuration** requirements

## 🔧 Maintenance

- **Regularly review** and update this structure
- **Keep documentation** synchronized with code
- **Maintain test coverage** for all services
- **Follow SOLID principles** in all new code

---

This structure supports scalability, maintainability, and clear separation of concerns while following Python and web development best practices.
