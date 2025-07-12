# Authentication Setup

This application now includes a login form with configurable default credentials.

## Default Credentials

By default, the application uses:

- **Username**: `admin`
- **Password**: `admin`

## Custom Credentials

You can set custom default credentials when starting the application:

```bash
streamlit run main.py -- --username YOUR_USERNAME --password YOUR_PASSWORD
```

### Examples

1. Run with custom credentials:

```bash
streamlit run main.py -- --username myuser --password mypass123
```

2. Run with default credentials (admin/admin):

```bash
streamlit run main.py
```

## Features

- **Login Form**: Clean, modern login interface
- **Default Credentials Display**: Shows the current default credentials in an expandable section
- **Quick Login**: "Use Defaults" button for rapid authentication
- **Sidebar Authentication**: Compact login form in the sidebar
- **Session Management**: Proper login/logout functionality

## Security Notes

⚠️ **Important**: This is a demo authentication system. For production use:

1. Use proper password hashing (bcrypt, scrypt, etc.)
2. Implement secure session management
3. Add HTTPS/TLS encryption
4. Consider using OAuth or other enterprise authentication systems
5. Store credentials securely (environment variables, secrets management)

## Usage in Production

For production deployments, consider:

```bash
# Using environment variables
export APP_USERNAME="your_secure_username"
export APP_PASSWORD="your_secure_password"
streamlit run main.py -- --username "$APP_USERNAME" --password "$APP_PASSWORD"
```

Or modify the code to read from environment variables or a secure configuration file.
