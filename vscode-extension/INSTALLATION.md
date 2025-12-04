# Pawa AI VS Code Extension - Installation & Testing Guide

Complete guide for installing, building, testing, and publishing the Pawa AI VS Code extension.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation from VSIX](#installation-from-vsix)
3. [Building from Source](#building-from-source)
4. [Testing the Extension](#testing-the-extension)
5. [Packaging for Distribution](#packaging-for-distribution)
6. [Publishing to Marketplace](#publishing-to-marketplace)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Node.js 16+**
   ```bash
   node --version  # Should be 16.0.0 or higher
   ```

2. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

3. **VS Code 1.80.0+**
   ```bash
   code --version
   ```

4. **Pawa AI Backend**
   - Must be running on `http://localhost:8000`
   - See backend documentation for setup

### Optional Tools

- **vsce** (VS Code Extension Manager)
  ```bash
  npm install -g @vscode/vsce
  ```

- **Git** (for version control)
  ```bash
  git --version
  ```

---

## Installation from VSIX

If you have a pre-built `.vsix` file:

### Method 1: Via Command Palette

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type: `Extensions: Install from VSIX`
4. Browse to your `.vsix` file
5. Select and install
6. Click "Reload" when prompted

### Method 2: Via Command Line

```bash
code --install-extension pawa-ai-1.0.0.vsix
```

### Method 3: Via Extensions Panel

1. Open Extensions panel: `Ctrl+Shift+X`
2. Click the `...` menu (top-right)
3. Select "Install from VSIX..."
4. Browse and select your `.vsix` file

---

## Building from Source

### Step 1: Clone or Navigate to Extension Directory

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension
```

### Step 2: Install Dependencies

```bash
npm install
```

This installs:
- TypeScript compiler
- VS Code types
- Axios for HTTP
- ESLint for linting
- Testing utilities

### Step 3: Compile TypeScript

```bash
npm run compile
```

Or watch mode for development:
```bash
npm run watch
```

This compiles `src/**/*.ts` → `out/**/*.js`

### Step 4: Verify Build

Check that the `out/` directory was created:
```bash
ls out/
# Should see: extension.js, chat/, ai/, commands/
```

---

## Testing the Extension

### Method 1: Extension Development Host (Recommended)

1. Open the extension directory in VS Code:
   ```bash
   code C:\Users\Jorams\genius-ai\vscode-extension
   ```

2. Press `F5` (or Run → Start Debugging)

3. A new VS Code window opens (Extension Development Host)

4. The extension is now active in this window

5. Test all features:
   - Open chat: `Ctrl+Shift+P`
   - Generate code: `Ctrl+Shift+G`
   - Right-click menu actions
   - Configuration settings

### Method 2: Manual Installation for Testing

1. Build the extension:
   ```bash
   npm run compile
   ```

2. Package it:
   ```bash
   vsce package
   ```

3. Install the `.vsix` file (see [Installation from VSIX](#installation-from-vsix))

### Testing Checklist

Test each feature systematically:

#### Basic Functionality
- [ ] Extension activates on VS Code startup
- [ ] Pawa AI icon appears in activity bar
- [ ] Welcome message appears

#### Chat Panel
- [ ] Chat panel opens with `Ctrl+Shift+P`
- [ ] Can send messages
- [ ] Responses stream correctly
- [ ] Code blocks are syntax highlighted
- [ ] Copy code button works
- [ ] Apply code button works
- [ ] Clear history button works

#### Code Generation
- [ ] `Ctrl+Shift+G` opens input dialog
- [ ] Generated code appears at cursor
- [ ] Works in new untitled files
- [ ] Works in existing files

#### Context Menu Actions
- [ ] "Pawa AI" submenu appears on right-click
- [ ] Explain code works
- [ ] Refactor code works
- [ ] Fix bug works
- [ ] Add comments works
- [ ] Generate tests works

#### Context Awareness
- [ ] Current file is detected
- [ ] Code selection is included
- [ ] Language is detected correctly
- [ ] Workspace info is included

#### Configuration
- [ ] Settings page shows Pawa AI options
- [ ] Changing API URL works
- [ ] Changing model works
- [ ] Changing temperature works
- [ ] Changes take effect without restart

#### Error Handling
- [ ] Shows error if backend is down
- [ ] Shows error for invalid responses
- [ ] Gracefully handles network issues
- [ ] Doesn't crash on malformed data

---

## Packaging for Distribution

### Step 1: Install VSCE

```bash
npm install -g @vscode/vsce
```

### Step 2: Verify package.json

Ensure these fields are set:
- `name`
- `displayName`
- `description`
- `version`
- `publisher`
- `repository` (optional)

### Step 3: Package the Extension

```bash
cd vscode-extension
vsce package
```

This creates: `pawa-ai-1.0.0.vsix`

### Step 4: Test the Package

Install and test the `.vsix` file before distributing:

```bash
code --install-extension pawa-ai-1.0.0.vsix
```

### Package Options

**Include specific files only:**
```bash
vsce package --baseContentUrl https://your-cdn.com
```

**Pre-release version:**
```bash
vsce package --pre-release
```

**Target specific platform:**
```bash
vsce package --target win32-x64
```

---

## Publishing to Marketplace

### Option 1: Manual Upload

1. Go to [Visual Studio Marketplace](https://marketplace.visualstudio.com/)
2. Sign in with Microsoft account
3. Create a publisher if you don't have one
4. Click "Publish extension"
5. Upload your `.vsix` file
6. Fill in marketplace details
7. Submit for review

### Option 2: Command Line Publishing

1. Create a Personal Access Token (PAT):
   - Go to Azure DevOps
   - User Settings → Personal Access Tokens
   - Create token with "Marketplace (Publish)" scope

2. Login with VSCE:
   ```bash
   vsce login <publisher-name>
   # Paste your PAT when prompted
   ```

3. Publish:
   ```bash
   vsce publish
   ```

### Versioning

Semantic versioning is used: `MAJOR.MINOR.PATCH`

**Bump version and publish:**
```bash
# Patch version (1.0.0 → 1.0.1)
vsce publish patch

# Minor version (1.0.0 → 1.1.0)
vsce publish minor

# Major version (1.0.0 → 2.0.0)
vsce publish major

# Specific version
vsce publish 1.2.3
```

---

## Troubleshooting

### Build Issues

**Problem**: `tsc: command not found`

**Solution**:
```bash
npm install -g typescript
# Or use local version
npx tsc -p ./
```

**Problem**: Type errors during compilation

**Solution**:
```bash
# Clean and rebuild
rm -rf out node_modules
npm install
npm run compile
```

### Packaging Issues

**Problem**: `vsce: command not found`

**Solution**:
```bash
npm install -g @vscode/vsce
```

**Problem**: Missing files in package

**Solution**:
Check `.vscodeignore` - make sure you're including necessary files

### Extension Not Activating

**Problem**: Extension doesn't activate in VS Code

**Solutions**:
1. Check `activationEvents` in package.json
2. Look for errors in "Developer: Toggle Developer Tools" (Help menu)
3. Check extension host logs
4. Verify extension is enabled in Extensions panel

### Backend Connection Issues

**Problem**: "Failed to connect to Pawa AI"

**Solutions**:
1. Verify backend is running: `http://localhost:8000`
2. Check API URL in settings
3. Test with curl:
   ```bash
   curl http://localhost:8000/health
   ```
4. Check firewall/antivirus settings

### Development Host Issues

**Problem**: Extension Development Host won't start

**Solutions**:
1. Close all VS Code windows
2. Delete `.vscode-test` directory
3. Rebuild:
   ```bash
   npm run compile
   ```
4. Try again with `F5`

---

## Directory Structure Verification

After building, your directory should look like:

```
vscode-extension/
├── out/                    # Compiled JavaScript
│   ├── extension.js
│   ├── chat/
│   │   └── ChatProvider.js
│   ├── ai/
│   │   └── PawaAI.js
│   └── commands/
│       └── index.js
├── media/                  # UI assets
│   ├── chat.css
│   ├── chat.js
│   └── icon.svg
├── node_modules/           # Dependencies
├── src/                    # TypeScript source
│   ├── extension.ts
│   ├── chat/
│   ├── ai/
│   └── commands/
├── package.json
├── tsconfig.json
├── README.md
├── CHANGELOG.md
├── QUICK_START.md
└── INSTALLATION.md (this file)
```

---

## Next Steps

After successful installation:

1. Read [QUICK_START.md](QUICK_START.md) for usage guide
2. Check [README.md](README.md) for full documentation
3. Review [CHANGELOG.md](CHANGELOG.md) for version history
4. Configure settings to your preference
5. Start using Pawa AI in VS Code!

---

## Getting Help

- **Build Issues**: Check VS Code output panel
- **Runtime Issues**: Check Developer Tools console
- **Backend Issues**: Check Pawa AI backend logs
- **GitHub Issues**: Report bugs and request features

---

Version: 1.0.0
Last Updated: 2025-01-04
