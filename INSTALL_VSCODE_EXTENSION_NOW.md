# Install Pawa AI VS Code Extension - RIGHT NOW

## What I Just Did

✅ Verified all extension files are compiled correctly
✅ Verified backend is running at `http://localhost:8000`
✅ Verified VSIX package exists (30 KB)
✅ Opened the VSIX file - VS Code should have launched

## What You Need to Do Now

### If VS Code Opened Automatically:

1. **VS Code should show an installation prompt**
   - Click **"Install"** button
   - Wait for installation to complete
   - Click **"Reload"** when prompted

### If No Prompt Appeared:

**Method 1: Through VS Code UI** (Easiest)
1. VS Code should be open now
2. Press `Ctrl+Shift+P`
3. Type: `Extensions: Install from VSIX`
4. Browse to: `C:\Users\Jorams\genius-ai\vscode-extension\pawa-ai-1.0.0.vsix`
5. Click **Open**
6. Click **Install**
7. Click **Reload** when prompted

**Method 2: Uninstall Old First** (If you already had it installed)
1. Press `Ctrl+Shift+X` (Extensions panel)
2. Search for "Pawa AI"
3. If you see it, click the **gear icon** ⚙️
4. Click **"Uninstall"**
5. Click **"Reload"**
6. Now follow Method 1 above to install fresh

## After Installation

### Step 1: Verify Installation
1. Press `Ctrl+Shift+X` (Extensions)
2. Search "Pawa AI"
3. Should show as **Installed** ✅

### Step 2: Check Activity Bar
Look at the left sidebar - you should see the Pawa AI icon (lightning bolt with neural network)

### Step 3: Open Chat
Press `Ctrl+Shift+P` - The chat panel should open in the sidebar!

### Step 4: Test It
In the chat, type: `"Hello, can you explain what TypeScript is?"`

## Troubleshooting

### Extension Not Showing
**Problem:** Don't see extension in Extensions panel

**Fix:**
```bash
# Run this command in terminal:
cd C:\Users\Jorams\genius-ai\vscode-extension
start "" "pawa-ai-1.0.0.vsix"
```
Then install through VS Code UI

### Chat Won't Open
**Problem:** Pressing Ctrl+Shift+P does nothing

**Fix:**
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type: `Reload Window`
3. Press Enter
4. Try `Ctrl+Shift+P` again

### "Failed to Connect" Error
**Problem:** Chat shows connection error

**Fix:** Backend needs to be running
```bash
cd C:\Users\Jorams\genius-ai\backend
python super_intelligent_endpoint.py
```

### No Icon in Activity Bar
**Problem:** Don't see Pawa AI icon in left sidebar

**Fix:**
1. Check extension is enabled in Extensions panel
2. Reload window: `Ctrl+Shift+P` → "Reload Window"

## Quick Commands

### Open Chat
```
Press: Ctrl+Shift+P
```

### Generate Code
```
Press: Ctrl+Shift+G
Then type what you want to generate
```

### Use Right-Click Menu
```
1. Select some code
2. Right-click
3. Choose "Pawa AI" submenu
4. Pick an action (Explain, Refactor, Fix Bug, etc.)
```

## Complete Reinstall (If Nothing Works)

If you're having issues, do a complete clean install:

```bash
# 1. Close VS Code completely

# 2. Recompile extension
cd C:\Users\Jorams\genius-ai\vscode-extension
npm run compile

# 3. Repackage
vsce package

# 4. Open VS Code

# 5. Uninstall old version:
#    Ctrl+Shift+X → Search "Pawa AI" → Uninstall

# 6. Install new version:
#    Ctrl+Shift+P → "Extensions: Install from VSIX"
#    Select: pawa-ai-1.0.0.vsix
```

## Features You Can Use

Once installed, try these:

### 1. AI Chat
- Press `Ctrl+Shift+P`
- Ask questions, get explanations
- Code appears with syntax highlighting
- Click "Copy" or "Apply" on code blocks

### 2. Generate Code
- Press `Ctrl+Shift+G`
- Describe what you want
- Code inserted at cursor

### 3. Explain Code
- Select code
- Right-click → Pawa AI → Explain Code
- Explanation appears in chat

### 4. Refactor Code
- Select code
- Right-click → Pawa AI → Refactor Code
- See diff preview, apply changes

### 5. Fix Bugs
- Select buggy code
- Right-click → Pawa AI → Fix Bug
- Bug fix applied

### 6. Add Comments
- Select code
- Right-click → Pawa AI → Add Comments
- Comments added automatically

### 7. Generate Tests
- Select function
- Right-click → Pawa AI → Generate Tests
- Test file opens

## What's Different from Before

The new version includes:
- ✅ Updated icon matching Pawa AI branding (lightning bolt + neural network)
- ✅ Proper SVG icon included
- ✅ All files properly compiled
- ✅ MIT License added
- ✅ Repository metadata added

## Verification Checklist

After installation, verify:

- [ ] Extension shows in Extensions panel (`Ctrl+Shift+X`)
- [ ] Pawa AI icon visible in activity bar (left sidebar)
- [ ] Chat opens with `Ctrl+Shift+P`
- [ ] Can send messages in chat
- [ ] Right-click menu shows "Pawa AI" submenu
- [ ] Backend connection works (no errors)

## Status Check

### Backend Status
```bash
# Should return: {"status":"healthy"...}
curl http://localhost:8000/health
```
✅ **Backend is running!**

### Extension Files
```bash
# All compiled correctly
ls vscode-extension/out/
```
✅ **All files present!**

### Extension Package
```bash
# Size: 30 KB
ls vscode-extension/pawa-ai-1.0.0.vsix
```
✅ **Package ready!**

## Next Steps

1. ✅ **Verify extension is installed** (Check Extensions panel)
2. ✅ **Press Ctrl+Shift+P** to open chat
3. ✅ **Start coding with AI!**

---

## Quick Start After Installation

```
1. Press Ctrl+Shift+P (opens chat)
2. Type: "Explain how async/await works in JavaScript"
3. Watch response stream in real-time
4. Select some code in your editor
5. Right-click → Pawa AI → Explain Code
6. Try generating code: Ctrl+Shift+G
7. Enjoy your AI coding assistant!
```

---

**The extension is ready! Just install it and start using it!** 🚀

**File Location:** `C:\Users\Jorams\genius-ai\vscode-extension\pawa-ai-1.0.0.vsix`
