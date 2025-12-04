# Pawa AI VS Code Extension - Troubleshooting Guide

## Quick Diagnostics

### 1. Is the Extension Installed?

**Check:**
1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions panel)
3. Search for "Pawa AI"
4. Should show as installed

**If not showing:**
```bash
# Reinstall the extension
code --install-extension "C:\Users\Jorams\genius-ai\vscode-extension\pawa-ai-1.0.0.vsix"
```

### 2. Is the Extension Activated?

**Check:**
1. Open VS Code
2. Help → Toggle Developer Tools
3. Go to Console tab
4. Look for: `🚀 Pawa AI Extension activated!`

**If not activated:**
1. Check Extensions panel - make sure it's enabled
2. Press `Ctrl+Shift+P` → "Reload Window"

### 3. Is the Backend Running?

**Test:**
```bash
curl http://localhost:8000/health
```

**Should return:**
```json
{"status":"healthy","intelligence_mode":"SUPER","reasoning_engine":"chain-of-thought"}
```

**If not running:**
```bash
cd C:\Users\Jorams\genius-ai\backend
python super_intelligent_endpoint.py
```

### 4. Can You See the Activity Bar Icon?

**Look for:** Pawa AI icon in the left sidebar (activity bar)

**If not visible:**
- The icon uses the SVG in `media/icon.svg`
- Check if other activity bar icons are visible
- Try View → Appearance → Activity Bar Position

### 5. Can You Open the Chat?

**Try:**
1. Press `Ctrl+Shift+P`
2. Should open chat panel in sidebar

**Or:**
1. View → Command Palette
2. Type: "Pawa AI: Open Chat"
3. Press Enter

## Common Issues and Fixes

### Issue 1: Extension Not Showing in Activity Bar

**Symptom:** No Pawa AI icon in left sidebar

**Fix:**
1. Check if extension is installed: `Ctrl+Shift+X`
2. Make sure it's enabled (not disabled)
3. Reload window: `Ctrl+Shift+P` → "Reload Window"
4. Check VS Code version: Help → About (must be 1.80.0+)

### Issue 2: Chat Panel Won't Open

**Symptom:** Pressing `Ctrl+Shift+P` does nothing

**Fix:**
1. Check Developer Tools for errors:
   - Help → Toggle Developer Tools
   - Look in Console tab
2. Try command palette:
   - `Ctrl+Shift+P` (Command Palette)
   - Type: "Pawa AI: Open Chat"
3. Check keybinding conflicts:
   - File → Preferences → Keyboard Shortcuts
   - Search: "Pawa AI"

### Issue 3: "Failed to Connect" Error

**Symptom:** Error message about connection failure

**Fix:**
1. Check backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. If not running, start it:
   ```bash
   cd C:\Users\Jorams\genius-ai\backend
   python super_intelligent_endpoint.py
   ```
3. Check settings:
   - `Ctrl+,` → Search "Pawa AI"
   - Verify API URL: `http://localhost:8000`
4. Test in browser: Open `http://localhost:8000` in Chrome

### Issue 4: Commands Not Appearing

**Symptom:** Right-click menu doesn't show "Pawa AI" option

**Fix:**
1. Make sure you have code selected
2. Check extension is activated (see Developer Tools)
3. Try reloading: `Ctrl+Shift+P` → "Reload Window"
4. Check package.json has correct commands

### Issue 5: Streaming Not Working

**Symptom:** Responses appear all at once, not streaming

**Fix:**
1. Check backend logs for errors
2. Verify backend supports streaming
3. Check network tab in Developer Tools
4. Try non-streaming mode in settings

### Issue 6: Icon Not Showing

**Symptom:** Extension works but no icon visible

**Fix:**
1. The icon is SVG format in `media/icon.svg`
2. Check file exists:
   ```bash
   ls vscode-extension/media/icon.svg
   ```
3. VS Code activity bar uses SVG icons
4. Try repackaging with PNG icon (128x128) instead

## Detailed Diagnostics

### Step 1: Check Extension Files

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension
ls -la out/
ls -la media/
```

**Should show:**
- `out/extension.js`
- `out/ai/PawaAI.js`
- `out/chat/ChatProvider.js`
- `out/commands/index.js`
- `media/chat.css`
- `media/chat.js`
- `media/icon.svg`

### Step 2: Check VS Code Logs

1. Help → Toggle Developer Tools
2. Console tab
3. Look for errors or warnings
4. Look for: `🚀 Pawa AI Extension activated!`

### Step 3: Check Extension Host Logs

1. View → Output
2. Dropdown: Select "Extension Host"
3. Look for Pawa AI related messages

### Step 4: Test Backend Manually

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/ai-agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "conversation_history": [],
    "project_path": ".",
    "stream": false
  }'
```

### Step 5: Reinstall Extension

1. Uninstall:
   ```bash
   # In Extensions panel (Ctrl+Shift+X)
   # Search "Pawa AI" → Gear icon → Uninstall
   ```

2. Clean install:
   ```bash
   cd C:\Users\Jorams\genius-ai\vscode-extension
   code --install-extension pawa-ai-1.0.0.vsix
   ```

3. Reload VS Code

## Configuration Check

### Verify Settings

Press `Ctrl+,` and search "Pawa AI":

```json
{
  "pawa-ai.apiUrl": "http://localhost:8000",
  "pawa-ai.model": "llama-3.3-70b-versatile",
  "pawa-ai.maxTokens": 4096,
  "pawa-ai.temperature": 0.7,
  "pawa-ai.autoContextLines": 50,
  "pawa-ai.showDiffBeforeApply": true
}
```

### Reset to Defaults

If settings are wrong:
1. `Ctrl+,` → Search "Pawa AI"
2. Click gear icon next to each setting
3. Select "Reset Setting"

## Still Not Working?

### Collect Debug Information

1. **VS Code Version:**
   ```
   Help → About
   ```

2. **Extension Version:**
   ```
   Extensions panel → Pawa AI → Version
   ```

3. **Console Errors:**
   ```
   Help → Toggle Developer Tools → Console
   Copy any red error messages
   ```

4. **Backend Status:**
   ```bash
   curl http://localhost:8000/health
   ```

5. **Extension Files:**
   ```bash
   ls -la vscode-extension/out/
   ls -la vscode-extension/media/
   ```

### Test in Clean Environment

1. Close all VS Code windows
2. Open new window
3. File → New Window
4. Try extension features

### Rebuild from Source

If all else fails:
```bash
cd C:\Users\Jorams\genius-ai\vscode-extension

# Clean
rm -rf out node_modules

# Reinstall
npm install

# Recompile
npm run compile

# Repackage
vsce package

# Reinstall
code --install-extension pawa-ai-1.0.0.vsix
```

## Common Error Messages

### "Command 'pawa-ai.openChat' not found"

**Cause:** Extension not activated

**Fix:**
1. Check Extensions panel - enable extension
2. Reload window
3. Check activation events in package.json

### "ECONNREFUSED localhost:8000"

**Cause:** Backend not running

**Fix:**
```bash
cd backend
python super_intelligent_endpoint.py
```

### "Extension host terminated unexpectedly"

**Cause:** Extension crash

**Fix:**
1. Check Developer Tools for stack trace
2. Reload window
3. Check for conflicting extensions

### "Webview is disposed"

**Cause:** Chat panel closed unexpectedly

**Fix:**
1. Reload window
2. Open chat again
3. Check for errors in console

## Getting Help

If none of these solutions work:

1. **Check logs**: Copy errors from Developer Tools
2. **Backend logs**: Check terminal running backend
3. **Extension files**: Verify all files compiled
4. **VS Code version**: Must be 1.80.0+
5. **Node version**: Must be 16+

## Quick Reset

**Complete reset:**
```bash
# 1. Uninstall extension in VS Code
# 2. Close VS Code
# 3. Rebuild
cd vscode-extension
rm -rf out node_modules
npm install
npm run compile
vsce package

# 4. Start VS Code
# 5. Install extension
code --install-extension pawa-ai-1.0.0.vsix

# 6. Reload window
```

---

**Still having issues?** Let me know the specific error message and I'll help debug!
