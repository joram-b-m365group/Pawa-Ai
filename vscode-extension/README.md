# Pawa AI - VS Code Extension

Production-grade AI coding assistant with Claude Code-like integration directly in VS Code.

## Features

### AI Chat Panel
- Real-time streaming responses from Pawa AI
- Context-aware: automatically includes current file and selection
- Beautiful, intuitive interface in VS Code sidebar
- Persistent conversation history
- Code syntax highlighting in responses

### Smart Code Actions
- **Generate Code**: Describe what you need and let AI generate it
- **Explain Code**: Get detailed explanations of selected code
- **Refactor Code**: Improve code quality and readability
- **Fix Bugs**: Automatically detect and fix bugs
- **Add Comments**: Generate helpful code comments
- **Generate Tests**: Create unit tests for your code

### Context Awareness
- Automatically includes current file information
- Reads your code selection for targeted assistance
- Provides surrounding code context for better understanding
- Workspace-aware responses

### Diff Preview
- See changes before applying them
- Review AI-generated code modifications
- Accept or reject changes with confidence

### Right-Click Integration
- Quick access from context menu
- "Pawa AI" submenu with all actions
- Works on any selected code

### Keyboard Shortcuts
- `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) - Open Chat
- `Ctrl+Shift+G` (Mac: `Cmd+Shift+G`) - Generate Code

## Installation

### From VSIX File

1. Download the `.vsix` file
2. Open VS Code
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Type "Install from VSIX"
5. Select the downloaded `.vsix` file
6. Reload VS Code when prompted

### From Source

1. Clone this repository
2. Open terminal in the extension directory
3. Run:
   ```bash
   npm install
   npm run compile
   ```
4. Press `F5` to open Extension Development Host

## Requirements

- **VS Code**: Version 1.80.0 or higher
- **Pawa AI Backend**: Must be running on `http://localhost:8000` (or configured URL)
- **Node.js**: Version 16+ for development

## Configuration

Open VS Code settings and search for "Pawa AI":

| Setting | Description | Default |
|---------|-------------|---------|
| `pawa-ai.apiUrl` | Pawa AI backend URL | `http://localhost:8000` |
| `pawa-ai.model` | AI model to use | `llama-3.3-70b-versatile` |
| `pawa-ai.maxTokens` | Max tokens in response | `4096` |
| `pawa-ai.temperature` | Response creativity (0-2) | `0.7` |
| `pawa-ai.autoContextLines` | Context lines around cursor | `50` |
| `pawa-ai.showDiffBeforeApply` | Show diff preview | `true` |

## Usage

### Opening the Chat

**Method 1: Keyboard Shortcut**
- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)

**Method 2: Activity Bar**
- Click the Pawa AI icon in the activity bar

**Method 3: Command Palette**
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P`)
- Type "Pawa AI: Open Chat"

### Generating Code

1. Place cursor where you want code
2. Press `Ctrl+Shift+G` (or use Command Palette: "Pawa AI: Generate Code")
3. Describe what you want
4. Code is inserted at cursor position

### Explaining Code

1. Select the code you want explained
2. Right-click → Pawa AI → Explain Selected Code
3. Explanation appears in chat panel

### Refactoring Code

1. Select code to refactor
2. Right-click → Pawa AI → Refactor Selected Code
3. Review diff preview
4. Accept or reject changes

### Fixing Bugs

1. Select problematic code
2. Right-click → Pawa AI → Fix Bug in Selected Code
3. Optionally describe the bug
4. Fixed code replaces selection

### Adding Comments

1. Select code that needs comments
2. Right-click → Pawa AI → Add Comments to Code
3. Commented code replaces selection

### Generating Tests

1. Select code to test
2. Right-click → Pawa AI → Generate Unit Tests
3. Tests open in new file
4. Save where appropriate

## Examples

### Example 1: Generate a Function

**You**: Generate a TypeScript function to validate email addresses

**Pawa AI**:
```typescript
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Example 2: Explain Complex Code

**Selected Code**:
```typescript
const result = items.reduce((acc, item) =>
  ({ ...acc, [item.id]: item }), {});
```

**Pawa AI**: This code transforms an array of items into an object where each item's `id` is a key and the item itself is the value. It uses `reduce` to iterate through the array, creating a new object that spreads the accumulator and adds each item with its `id` as the key.

### Example 3: Refactor for Better Performance

**Before**:
```typescript
function findUser(id: number) {
  for (let i = 0; i < users.length; i++) {
    if (users[i].id === id) {
      return users[i];
    }
  }
}
```

**After** (Pawa AI refactored):
```typescript
function findUser(id: number): User | undefined {
  return users.find(user => user.id === id);
}
```

## Troubleshooting

### Extension Not Working

**Problem**: Commands don't appear or extension doesn't activate

**Solutions**:
1. Check VS Code version (must be 1.80.0+)
2. Reload VS Code: `Ctrl+Shift+P` → "Reload Window"
3. Check extension is enabled: Extensions panel → search "Pawa AI"

### Can't Connect to Pawa AI

**Problem**: "Failed to connect to Pawa AI" error

**Solutions**:
1. Ensure Pawa AI backend is running: `http://localhost:8000`
2. Check the backend URL in settings
3. Test backend: Open `http://localhost:8000` in browser
4. Check firewall/antivirus settings

### Streaming Not Working

**Problem**: Responses don't stream, appear all at once

**Solutions**:
1. Check backend logs for errors
2. Verify `stream: true` is supported by your backend
3. Update to latest extension version

### Context Not Being Sent

**Problem**: AI doesn't seem aware of current file

**Solutions**:
1. Ensure a file is open and active in editor
2. Try selecting code explicitly
3. Check `autoContextLines` setting

## Development

### Building from Source

```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch mode for development
npm run watch

# Run tests
npm test

# Package extension
npm run package
```

### Project Structure

```
vscode-extension/
├── src/
│   ├── extension.ts          # Entry point
│   ├── chat/
│   │   └── ChatProvider.ts   # Chat webview provider
│   ├── ai/
│   │   └── PawaAI.ts        # AI client
│   └── commands/
│       └── index.ts          # Command handlers
├── media/
│   ├── chat.html            # Chat UI (embedded)
│   ├── chat.css             # Chat styles
│   └── chat.js              # Chat logic
├── package.json
├── tsconfig.json
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Comparison with Claude Code

| Feature | Pawa AI Extension | Claude Code |
|---------|------------------|-------------|
| Chat Panel | ✅ | ✅ |
| Streaming Responses | ✅ | ✅ |
| Context Awareness | ✅ | ✅ |
| Code Generation | ✅ | ✅ |
| Diff Preview | ✅ | ✅ |
| Right-Click Menu | ✅ | ✅ |
| Keyboard Shortcuts | ✅ | ✅ |
| Custom Backend | ✅ | ❌ |
| Self-Hosted | ✅ | ❌ |
| Free to Use | ✅ | 💰 |

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: Report issues in your repository
- **Documentation**: See QUICK_START.md and INSTALLATION.md
- **Backend Setup**: See Pawa AI backend documentation

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Made with ❤️ by the Pawa AI Team**

Version: 1.0.0
