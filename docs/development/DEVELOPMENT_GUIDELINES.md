# Development Guidelines

This document provides comprehensive guidelines for maintaining code quality and consistency in the Speaker Diarization project.

## 🏗️ Architecture Guidelines

### SOLID Principles

Our codebase follows SOLID design principles:

1. **Single Responsibility Principle (SRP)**

   - Each class should have only one reason to change
   - ✅ Good: `AuthenticationService` only handles authentication
   - ❌ Bad: A service that handles both file upload and authentication

2. **Open/Closed Principle (OCP)**

   - Classes should be open for extension, closed for modification
   - ✅ Good: Use interfaces and dependency injection
   - ❌ Bad: Modifying existing classes to add new functionality

3. **Liskov Substitution Principle (LSP)**

   - Subtypes must be substitutable for their base types
   - ✅ Good: Any implementation of `AudioProcessorInterface` works
   - ❌ Bad: Implementations that change expected behavior

4. **Interface Segregation Principle (ISP)**

   - Don't force clients to depend on interfaces they don't use
   - ✅ Good: Separate interfaces for different concerns
   - ❌ Bad: One large interface with many unrelated methods

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions, not concretions
   - ✅ Good: Inject services via constructor
   - ❌ Bad: Creating service instances inside classes

### Layer Organization

```
┌─────────────────────┐
│    UI Layer         │  ← Streamlit components
│  (src/ui/)          │
├─────────────────────┤
│   Service Layer     │  ← Business logic
│  (src/services/)    │
├─────────────────────┤
│    Core Layer       │  ← Domain models & interfaces
│  (src/core/)        │
├─────────────────────┤
│   Utils Layer       │  ← Cross-cutting utilities
│  (src/utils/)       │
└─────────────────────┘
```

## 📝 Coding Standards

### Python Style Guide

Follow PEP 8 with these specific rules:

#### Naming Conventions

```python
# Classes: PascalCase
class AudioProcessorService:
    pass

# Functions and variables: snake_case
def process_audio_file(file_path: str) -> bool:
    audio_processor = AudioProcessorService()
    return True

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE_MB = 50
SUPPORTED_FORMATS = ["wav", "mp3"]

# Private methods: _leading_underscore
def _internal_helper(self) -> None:
    pass
```

#### Type Hints

Always use type hints:

```python
from typing import List, Optional, Dict, Any
from pathlib import Path

def process_files(
    file_paths: List[Path],
    options: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Process multiple files and return results."""
    if options is None:
        options = {}
    return []
```

#### Documentation

Use Google-style docstrings:

```python
def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user with username and password.

    Args:
        username: The username to authenticate
        password: The password for authentication

    Returns:
        True if authentication successful, False otherwise

    Raises:
        AuthenticationError: If authentication service is unavailable

    Example:
        >>> auth_service = AuthenticationService()
        >>> auth_service.authenticate_user("admin", "password")
        True
    """
    pass
```

### Error Handling

Use specific exception types and proper error handling:

```python
# Good: Specific exceptions
class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class FileProcessingError(Exception):
    """Raised when file processing fails."""
    pass

# Good: Proper error handling
def process_audio(file_path: Path) -> ProcessingResult:
    """Process audio file with proper error handling."""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Processing logic here
        return ProcessingResult(success=True, message="Processing completed")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return ProcessingResult(success=False, error=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ProcessingResult(success=False, error="Processing failed")
```

## 🧪 Testing Guidelines

### Test Structure

Mirror the source code structure in tests:

```
src/services/auth_service.py  →  tests/unit/test_auth_service.py
src/ui/components/auth.py     →  tests/unit/test_auth_component.py
```

### Test Naming

```python
class TestAuthenticationService:
    """Test suite for AuthenticationService."""

    def test_login_with_valid_credentials_returns_true(self):
        """Test that valid credentials result in successful login."""
        pass

    def test_login_with_invalid_credentials_returns_false(self):
        """Test that invalid credentials result in failed login."""
        pass

    def test_logout_clears_session_state(self):
        """Test that logout properly clears authentication state."""
        pass
```

### Mock Usage

Use mocks for external dependencies:

```python
import unittest.mock as mock

def test_audio_processing_with_mocked_service(self):
    """Test audio processing with mocked external service."""
    with mock.patch('src.services.audio_processor.whisper') as mock_whisper:
        mock_whisper.load_model.return_value = mock.Mock()

        processor = AudioProcessorService()
        result = processor.process_file("test.wav")

        assert result.success is True
        mock_whisper.load_model.assert_called_once()
```

## 📁 File Organization

### Adding New Features

1. **Create Service Interface** (if needed):

```python
# src/core/models.py
class NewFeatureInterface(ABC):
    """Interface for new feature."""

    @abstractmethod
    def execute_feature(self, data: Any) -> FeatureResult:
        """Execute the new feature."""
        pass
```

2. **Implement Service**:

```python
# src/services/new_feature_service.py
class NewFeatureService(NewFeatureInterface):
    """Service implementation for new feature."""

    def execute_feature(self, data: Any) -> FeatureResult:
        """Implementation of the new feature."""
        pass
```

3. **Add UI Component**:

```python
# src/ui/components/new_feature.py
class NewFeatureComponent:
    """UI component for new feature."""

    def __init__(self, service: NewFeatureInterface):
        self.service = service

    def render(self) -> None:
        """Render the new feature UI."""
        pass
```

4. **Write Tests**:

```python
# tests/unit/test_new_feature_service.py
class TestNewFeatureService:
    """Test suite for NewFeatureService."""
    pass
```

### Configuration Management

Add new configuration in `config/settings.py`:

```python
class NewFeatureConfig:
    """Configuration for new feature."""

    FEATURE_ENABLED: bool = True
    FEATURE_TIMEOUT: int = 30
    FEATURE_OPTIONS: Dict[str, Any] = {
        "option1": "value1",
        "option2": "value2"
    }
```

## 🔧 Development Workflow

### Before Starting Development

1. **Pull latest changes**: `git pull origin main`
2. **Activate virtual environment**: `source venv/bin/activate`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run tests**: `python run_tests.py`

### During Development

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Follow TDD**: Write tests first, then implementation
3. **Run tests frequently**: `python run_tests.py`
4. **Check imports**: Ensure all imports work correctly

### Before Committing

1. **Run all tests**: `python run_tests.py`
2. **Check code style**: Use black, flake8, or similar
3. **Update documentation**: If APIs changed
4. **Test main application**: `python main.py --help`

### Code Review Checklist

- [ ] Follows SOLID principles
- [ ] Has appropriate tests
- [ ] Includes proper documentation
- [ ] Uses type hints
- [ ] Handles errors appropriately
- [ ] Follows naming conventions
- [ ] No hard-coded values (use config)

## 📚 Documentation Standards

### README Files

- Clear project overview
- Installation instructions
- Usage examples
- Link to detailed documentation

### Code Documentation

- All public methods documented
- Complex logic explained with comments
- Type hints for all parameters and returns
- Examples for public APIs

### Architecture Documentation

- Update when adding new layers
- Document design decisions
- Include diagrams for complex workflows

## 🚀 Deployment Guidelines

### Environment Variables

Store sensitive data in environment variables:

```bash
# .env
HF_TOKEN=your_huggingface_token
DEBUG=false
LOG_LEVEL=INFO
```

### Configuration

Use different configs for different environments:

```python
# config/settings.py
class Config:
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    HF_TOKEN = os.getenv('HF_TOKEN')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

## 🔍 Performance Guidelines

### File Processing

- Use streaming for large files
- Implement progress indicators
- Add timeout handling
- Cache processed results when appropriate

### Memory Management

- Clean up temporary files
- Use context managers for file operations
- Monitor memory usage for large audio files

### Error Recovery

- Implement retry logic for transient failures
- Provide meaningful error messages
- Log errors for debugging

## 📋 Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and update documentation
- Run security audits
- Monitor performance metrics
- Clean up deprecated code

### Code Reviews

- Focus on architecture adherence
- Check test coverage
- Verify documentation updates
- Ensure error handling is appropriate

---

Following these guidelines ensures consistent, maintainable, and scalable code that aligns with the project's architecture and goals.
