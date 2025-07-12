# Speaker Diarization App - Refactored Architecture

This project has been refactored using SOLID design principles and Python best practices to create a maintainable, scalable, and testable codebase.

## 🏗️ Architecture Overview

The application follows a clean architecture pattern with clear separation of concerns:

```
notta/
├── main.py                     # New main entry point
├── app.py                      # Original monolithic app (kept for reference)
├── config/                     # Configuration management
│   ├── __init__.py
│   └── settings.py
├── src/                        # Source code
│   ├── core/                   # Domain layer (business logic)
│   │   ├── __init__.py
│   │   └── models.py           # Domain models and interfaces
│   ├── services/               # Service layer (business logic implementation)
│   │   ├── __init__.py
│   │   ├── audio_processor.py  # Audio processing service
│   │   ├── auth_service.py     # Authentication service
│   │   ├── file_manager.py     # File management service
│   │   └── transcript_manager.py # Transcript management service
│   ├── ui/                     # Presentation layer
│   │   ├── __init__.py
│   │   ├── components/         # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication components
│   │   │   └── file_components.py # File management components
│   │   └── pages/              # Page-level components
│   │       └── __init__.py
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── helpers.py          # Helper functions
├── requirements.txt            # Dependencies
└── uploads/                    # File storage directory
```

## 🎯 SOLID Principles Applied

### Single Responsibility Principle (SRP)

- Each class has a single, well-defined responsibility
- `FileManagerService` only handles file operations
- `AudioProcessorService` only handles audio processing
- `AuthenticationService` only handles authentication

### Open/Closed Principle (OCP)

- Services implement interfaces, making them easily extendable
- New authentication methods can be added without modifying existing code
- New audio processors can be plugged in via the interface

### Liskov Substitution Principle (LSP)

- All service implementations can be substituted with their interfaces
- Mock implementations can be easily created for testing

### Interface Segregation Principle (ISP)

- Interfaces are focused and contain only necessary methods
- `AudioProcessorInterface` is separate from `FileManagerInterface`

### Dependency Inversion Principle (DIP)

- High-level modules depend on abstractions, not concrete implementations
- Services are injected into the main application class
- Easy to swap implementations for testing or different environments

## 🚀 Key Improvements

### 1. **Separation of Concerns**

- **Domain Layer**: Contains business rules and entities
- **Service Layer**: Implements business logic
- **UI Layer**: Handles presentation and user interaction
- **Configuration**: Centralized settings management

### 2. **Dependency Injection**

- Services are injected into components that need them
- Makes testing easier and reduces coupling
- Follows the Hollywood Principle ("Don't call us, we'll call you")

### 3. **Error Handling**

- Proper exception handling throughout the application
- Service methods return structured results with error information
- User-friendly error messages in the UI

### 4. **Type Safety**

- Full type hints throughout the codebase
- Dataclasses for structured data
- Enums for constants and status values

### 5. **Configuration Management**

- Centralized configuration in `config/settings.py`
- Environment-specific settings
- Easy to modify without changing code

### 6. **Reusable Components**

- UI components can be reused across different pages
- Service components can be used in different contexts
- Utility functions are centralized

## 🔧 Running the Refactored Application

### Using the New Architecture

```bash
# Run the refactored application
streamlit run main.py
```

### Using the Original App (for comparison)

```bash
# Run the original monolithic application
streamlit run app.py
```

## 🧪 Benefits for Testing

The refactored architecture makes testing much easier:

```python
# Example: Testing file manager in isolation
def test_file_manager():
    file_manager = FileManagerService(upload_dir=Path("/tmp/test"))
    # Test file operations without UI dependencies

# Example: Testing audio processor with mock
def test_audio_processor():
    mock_processor = MockAudioProcessor()
    app = SpeakerDiarizationApp()
    app.audio_processor = mock_processor
    # Test processing logic without actual audio processing
```

## 📦 Service Descriptions

### Core Domain Models

- `AudioFile`: Represents an audio file with metadata
- `ProcessingResult`: Contains transcription results
- `ProcessingOptions`: Configuration for audio processing
- Various interfaces defining contracts for services

### Services

- **AudioProcessorService**: Handles audio transcription and diarization
- **FileManagerService**: Manages file upload, storage, and retrieval
- **TranscriptManagerService**: Manages SRT transcript files
- **AuthenticationService**: Handles user authentication (demo implementation)

### UI Components

- **AuthComponent**: Authentication UI elements
- **FileListComponent**: File listing and management UI
- **FileUploadComponent**: File upload interface

## 🔄 Migration Path

1. **Phase 1**: Keep original `app.py` for reference
2. **Phase 2**: Use new `main.py` for new features
3. **Phase 3**: Gradually migrate existing functionality
4. **Phase 4**: Remove old `app.py` when fully migrated

## 🛠️ Future Enhancements

The new architecture makes it easy to add:

- Database integration (replace file-based storage)
- Background job processing
- Real-time processing updates
- Multiple authentication providers
- API endpoints
- Advanced UI components
- Comprehensive test suite

## 📝 Development Guidelines

1. **Adding New Features**: Create new services implementing the appropriate interfaces
2. **UI Changes**: Create reusable components in the `ui/components` directory
3. **Configuration**: Add new settings to `config/settings.py`
4. **Testing**: Mock services using their interfaces for unit testing

This refactored architecture provides a solid foundation for scaling and maintaining the Speaker Diarization application.
