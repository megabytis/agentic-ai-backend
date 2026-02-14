# Text Edit Tool - AI-Powered File System Assistant

A Python-based chatbot with file system manipulation capabilities. Read, write, edit, and list files through natural language conversations.

## Features

- 📁 **File Operations**:
  - `read_file` - View file contents
  - `write_file` - Create/overwrite files
  - `list_directory` - Browse folders with file sizes
  - `edit_file` - Replace text or edit specific lines
- 🛠️ **Multi-Tool Support**: Date/time functions, reminders, batch operations
- ⚡ **Streaming Responses**: Real-time token-by-token output
- 🔄 **Conversation History**: Maintains context across interactions
- 🛡️ **Safety Features**: Path validation, error handling

## Prerequisites

- Python 3.8+
- OpenRouter API key (free tier available)
- Required packages: `openai`, `python-dotenv`

## Installation

```bash
# Clone repository
git clone <your-repo-url>
cd text-edit-tool

# Install dependencies
pip install openai python-dotenv

# Create .env file with your API key
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

## Usage

```bash
python main.py
```

### Commands:

- `/bye` - Exit chatbot
- No special commands - just ask naturally!

### Example Queries:

```bash
# Read files
You: Show me what's in config.json

# List directory contents
You: What files are in the current folder?

# Create new files
You: Create a file called todo.txt with my tasks: buy milk, call doctor

# Edit files
You: Change "milk" to "eggs" in todo.txt

# Multi-step workflows
You: Read the error log, fix the bug on line 10, then save as fixed.log

# Complex operations
You: Create a Python script that calculates Fibonacci numbers
```

## Tool Schemas

### File Reading

```python
{
    "name": "read_file",
    "description": "Read contents of a file",
    "parameters": {"filepath": "path/to/file.txt"}
}
```

### File Writing

```python
{
    "name": "write_file",
    "description": "Write content to a file (creates or overwrites)",
    "parameters": {
        "filepath": "path/to/file.txt",
        "content": "file contents here"
    }
}
```

### Directory Listing

```python
{
    "name": "list_directory",
    "description": "List files and directories in a path",
    "parameters": {"path": "."}  # optional, defaults to current
}
```

### File Editing

```python
{
    "name": "edit_file",
    "description": "Edit a file: replace text or edit specific lines",
    "parameters": {
        "filepath": "path/to/file.txt",
        "old_text": "text to replace",  # optional
        "new_text": "new text",         # optional
        "line_start": 5,                # optional (1-indexed)
        "line_end": 10                   # optional
    }
}
```

## Supported Tools

| Tool                       | Description                |
| -------------------------- | -------------------------- |
| `read_file`                | View file contents         |
| `write_file`               | Create/overwrite files     |
| `list_directory`           | Browse folder contents     |
| `edit_file`                | Replace text or edit lines |
| `get_current_time`         | Current time               |
| `get_current_date`         | Current date               |
| `get_current_datetime`     | Combined date/time         |
| `add_duration_to_datetime` | Date arithmetic            |
| `set_reminder`             | Set reminders              |
| `run_batch`                | Execute multiple tools     |

## Safety Features

- **Path Validation**: Prevents directory traversal attacks
- **Error Handling**: Graceful failure with user-friendly messages
- **Directory Creation**: Automatically creates parent directories
- **File Size Info**: Shows file sizes in directory listings
- **Edit Validation**: Checks if text exists before replacing

## Project Structure

```
text-edit-tool/
├── main.py              # Main chatbot implementation
├── .env                 # API keys (not in repo)
├── README.md            # This file
└── requirements.txt     # Dependencies
```

## Dependencies

```
openai>=1.0.0
python-dotenv>=1.0.0
```

## How It Works

1. User requests file operation in natural language
2. LLM maps request to appropriate file tool
3. Tool executes with safety checks:
   - Resolves relative paths
   - Validates file existence
   - Handles permissions
4. Results returned to LLM for natural language response
5. All interactions maintain conversation context

## Example Workflow

```bash
User: Create a Python file that prints "Hello World"
→ LLM calls write_file("hello.py", "print('Hello World')")
→ File created successfully
→ LLM responds: "I've created hello.py with a simple print statement"

User: Now read it back
→ LLM calls read_file("hello.py")
→ Shows file contents
→ LLM confirms: "The file contains: print('Hello World')"
```

## Limitations

- No binary file support (text only)
- No undo functionality (use version control)
- No remote file system access (local only)
- File size limits for very large files
- No concurrent file operations

## Future Improvements

- [ ] Add file move/copy operations
- [ ] Implement file search/grep functionality
- [ ] Add file diff/compare tools
- [ ] Support binary files (images, PDFs)
- [ ] Add file backup/versioning
- [ ] Remote file system support (SFTP, S3)

## License

MIT License - Feel free to use and modify!

## Acknowledgments

- OpenRouter for free LLM access
- Anthropic for Text Editor tool inspiration
- Python `os` and `pathlib` for file operations
