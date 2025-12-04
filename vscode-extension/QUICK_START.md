# Pawa AI VS Code Extension - Quick Start Guide

Get up and running with Pawa AI in VS Code in under 5 minutes!

## Prerequisites

Before you begin, ensure you have:

1. **VS Code** version 1.80.0 or higher
2. **Pawa AI Backend** running on `http://localhost:8000`
3. **Node.js** version 16+ (for building from source)

## Installation Methods

### Method 1: From VSIX File (Recommended)

1. Download `pawa-ai-1.0.0.vsix` file
2. Open VS Code
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Type: `Extensions: Install from VSIX`
5. Select the downloaded `.vsix` file
6. Click "Reload" when prompted

### Method 2: From Source

```bash
# Clone or navigate to extension directory
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Press F5 in VS Code to launch Extension Development Host
```

## First Time Setup

### 1. Start Pawa AI Backend

Make sure your Pawa AI backend is running:

```bash
# In your Pawa AI directory
cd backend
python super_intelligent_endpoint.py
```

The backend should be accessible at `http://localhost:8000`

### 2. Open VS Code

Launch VS Code and open any project or folder.

### 3. Verify Extension is Active

You should see:
- Pawa AI icon in the activity bar (left sidebar)
- Welcome notification: "Pawa AI is ready!"

## Your First Chat

### Opening the Chat Panel

**Option A: Keyboard Shortcut** (Fastest)
```
Windows/Linux: Ctrl+Shift+P
Mac: Cmd+Shift+P
```

**Option B: Activity Bar**
- Click the Pawa AI icon in the left sidebar

**Option C: Command Palette**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P`)
2. Type: "Pawa AI: Open Chat"
3. Press Enter

### Sending Your First Message

1. Type in the chat input at the bottom
2. Example: "Explain what TypeScript interfaces are"
3. Press Enter or click Send button
4. Watch the response stream in real-time!

## Quick Actions

### Generate Code

**Scenario**: You need a function but don't want to write it from scratch

1. Place cursor where you want the code
2. Press `Ctrl+Shift+G` (or `Cmd+Shift+G`)
3. Describe what you want:
   ```
   A function to debounce user input
   ```
4. Code appears at your cursor position!

### Explain Code

**Scenario**: You found complex code and need to understand it

1. Select the code you're confused about
2. Right-click → Pawa AI → Explain Selected Code
3. Explanation appears in chat panel
4. Ask follow-up questions!

### Refactor Code

**Scenario**: Your code works but could be cleaner

1. Select code to refactor
2. Right-click → Pawa AI → Refactor Selected Code
3. Review the diff preview
4. Accept or reject changes

### Fix Bugs

**Scenario**: Something's not working and you're stuck

1. Select the problematic code
2. Right-click → Pawa AI → Fix Bug in Selected Code
3. Optionally describe the issue
4. Review and apply the fix

## Configuration (Optional)

Press `Ctrl+,` to open settings, then search "Pawa AI":

**Essential Settings:**

```json
{
  "pawa-ai.apiUrl": "http://localhost:8000",
  "pawa-ai.model": "llama-3.3-70b-versatile",
  "pawa-ai.maxTokens": 4096,
  "pawa-ai.temperature": 0.7
}
```

**Advanced Settings:**

```json
{
  "pawa-ai.autoContextLines": 50,
  "pawa-ai.showDiffBeforeApply": true
}
```

## Keyboard Shortcuts Reference

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Open Chat | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Generate Code | `Ctrl+Shift+G` | `Cmd+Shift+G` |
| Send Message | `Enter` | `Enter` |
| New Line in Chat | `Shift+Enter` | `Shift+Enter` |

## Common Use Cases

### 1. Learning a New Framework

**You**: "Show me a basic Next.js 14 page with server components"

**Result**: Complete example with explanations

### 2. Code Review

**Action**: Select your function → Right-click → Pawa AI → Explain Code

**Result**: Analysis of what your code does and suggestions

### 3. Writing Tests

**Action**: Select function → Right-click → Pawa AI → Generate Unit Tests

**Result**: Complete test file opens in new tab

### 4. Debugging

**You**: "Why is this useState not updating?"

**Result**: Explanation of closure issues in React and how to fix

### 5. Documentation

**Action**: Select code → Right-click → Pawa AI → Add Comments

**Result**: Clear, helpful comments added to your code

## Tips for Best Results

### 1. Be Specific

❌ **Vague**: "Make this better"
✅ **Specific**: "Refactor this to use async/await instead of promises"

### 2. Provide Context

Include what you're trying to achieve:
```
I'm building a user authentication system.
Generate a function to validate password strength.
Requirements: 8+ chars, uppercase, lowercase, number, special char
```

### 3. Use Code Selection

Always select relevant code when using context menu actions. The AI gets better context!

### 4. Ask Follow-Up Questions

The chat remembers your conversation:
```
You: "Create a React component for a modal"
AI: [generates modal]
You: "Add animations and close on backdrop click"
AI: [enhances the modal]
```

### 5. Review Before Applying

Always review AI-generated code before applying:
- Check for security issues
- Verify logic is correct
- Ensure it fits your patterns

## Troubleshooting

### Extension Not Showing Up

**Solution**:
1. Check Extensions panel: `Ctrl+Shift+X`
2. Search "Pawa AI"
3. Ensure it's enabled
4. Reload window: `Ctrl+Shift+P` → "Reload Window"

### "Failed to Connect" Error

**Solution**:
1. Verify backend is running: Open `http://localhost:8000` in browser
2. Check the API URL in settings
3. Check firewall/antivirus settings

### Responses Not Streaming

**Solution**:
1. Update to latest extension version
2. Check backend logs for errors
3. Try non-streaming mode in settings

### No Context Being Sent

**Solution**:
1. Make sure a file is open in editor
2. Try selecting code explicitly
3. Check `autoContextLines` setting

## Next Steps

Now that you're set up:

1. **Explore Commands**: Press `Ctrl+Shift+P` and type "Pawa AI" to see all available commands

2. **Customize Settings**: Adjust temperature, context lines, and other settings to your preference

3. **Try Different Use Cases**: Experiment with code generation, explanations, refactoring, and testing

4. **Read Full Documentation**: Check out [README.md](README.md) for comprehensive guide

5. **Join Community**: Share your experience and get help (link to community)

## Example Workflow

Here's a complete workflow example:

```
1. Open your project in VS Code
2. Press Ctrl+Shift+P to open Pawa AI chat
3. Ask: "Review my authentication middleware"
4. Select your middleware code
5. Right-click → Pawa AI → Explain Code
6. Review the explanation
7. Ask: "Are there any security issues?"
8. Review recommendations
9. Select code to fix
10. Right-click → Pawa AI → Refactor Code
11. Review diff, apply changes
12. Right-click → Pawa AI → Generate Tests
13. Save tests, run them
14. Done! 🎉
```

## Getting Help

- **Documentation**: [README.md](README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Issues**: GitHub Issues
- **Backend Docs**: See Pawa AI backend documentation

---

**You're all set!** Start coding with AI assistance. Press `Ctrl+Shift+P` now to open the chat!

**Questions?** Check the full [README.md](README.md) or ask Pawa AI directly in the chat!

---

Version: 1.0.0
Last Updated: 2025-01-04
