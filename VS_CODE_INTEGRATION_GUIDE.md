# 🚀 VS Code + Pawa AI Integration Guide

## The Ultimate Development Setup

This guide shows you how to use **VS Code** and **Pawa AI** together for the best coding experience - instant file visibility, professional debugging, and AI-powered code generation!

---

## 🎯 Why Use VS Code with Pawa AI?

| Feature | Browser Only | With VS Code |
|---------|-------------|--------------|
| **File Visibility** | Manual refresh needed | Instant auto-detection |
| **Code Execution** | Limited terminal | Full VS Code terminal |
| **Debugging** | Not available | Professional debugger |
| **Extensions** | None | Thousands available |
| **Git Integration** | Basic | Full Git UI |
| **Multi-file Editing** | Limited | Full power |

---

## 📋 Quick Start (3 Steps)

### Step 1: Open Project in VS Code

**Option A: Double-click the batch file**
```
📁 C:\Users\Jorams\genius-ai\OPEN_IN_VSCODE.bat
```
Just double-click it! VS Code will open automatically.

**Option B: Manual method**
1. Open VS Code
2. Press `Ctrl+K Ctrl+O` (or File → Open Folder)
3. Navigate to: `C:\Users\Jorams\genius-ai`
4. Click "Select Folder"

### Step 2: Open Pawa AI in Browser

```
http://localhost:3000
```

Make sure both backend servers are running:
- Port 8000: AI Agent (`super_intelligent_endpoint.py`)
- Port 8001: Code Editor API (`code_editor_api.py`)

### Step 3: Start Coding!

1. **In Browser**: Open AI Agent (purple robot icon)
2. **In Browser**: Ask AI to create files
3. **In VS Code**: Watch files appear instantly! ✨
4. **In VS Code**: Run, debug, and edit code

---

## 🎬 Example Workflow

### Example 1: Create a Full-Stack App

**In Browser (Pawa AI):**
```
Create a production-ready task management API with:
- Express.js backend with TypeScript
- MongoDB models with validation
- JWT authentication
- CRUD endpoints for tasks
- Error handling middleware
- Docker setup
```

**In VS Code:**
1. Watch as files appear in real-time:
   - `backend/src/server.ts`
   - `backend/src/models/Task.ts`
   - `backend/src/routes/tasks.ts`
   - `backend/src/middleware/auth.ts`
   - `Dockerfile`
   - `docker-compose.yml`

2. Open integrated terminal (`Ctrl+` `)
3. Run the code:
   ```bash
   cd backend
   npm install
   npm run dev
   ```

4. Set breakpoints and debug!

### Example 2: Create React Components

**In Browser (Pawa AI):**
```
Create a React dashboard with:
- TypeScript
- Tailwind CSS
- Charts using recharts
- Authentication context
- Protected routes
```

**In VS Code:**
1. Files appear instantly
2. Open `src/components/Dashboard.tsx`
3. See syntax highlighting, IntelliSense, auto-imports
4. Run dev server:
   ```bash
   cd frontend
   npm run dev
   ```

---

## 🔧 Recommended VS Code Extensions

Install these for the best experience:

### Essential
- **ES7+ React/Redux/React-Native snippets** - React code snippets
- **Prettier - Code formatter** - Auto-format code
- **ESLint** - Linting for JavaScript/TypeScript
- **TypeScript Vue Plugin (Volar)** - TypeScript support
- **Python** - Python development
- **Tailwind CSS IntelliSense** - Tailwind autocomplete

### Nice to Have
- **GitLens** - Enhanced Git integration
- **Thunder Client** - API testing (like Postman)
- **Docker** - Docker file support
- **Error Lens** - Inline error display
- **Auto Rename Tag** - Rename paired HTML/JSX tags
- **Path Intellisense** - File path autocomplete

### Installation
1. Press `Ctrl+Shift+X` in VS Code
2. Search for extension name
3. Click "Install"

---

## ⚙️ VS Code Settings (Optional)

Create `.vscode/settings.json` in your project:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "javascript.updateImportsOnFileMove.enabled": "always",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

---

## 🐛 Debugging in VS Code

### Debug Node.js/TypeScript

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Backend",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/backend/src/server.ts",
      "preLaunchTask": "npm: build",
      "outFiles": ["${workspaceFolder}/backend/dist/**/*.js"]
    }
  ]
}
```

**Usage:**
1. Set breakpoints by clicking left of line numbers
2. Press `F5` to start debugging
3. Step through code with `F10` (step over) and `F11` (step into)

### Debug Python

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "super_intelligent_endpoint:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true
    }
  ]
}
```

---

## 🔄 Git Integration

VS Code has excellent Git support built-in:

### View Changes
- **Source Control** (`Ctrl+Shift+G`): See all changes
- **Diff View**: Click a file to see changes side-by-side

### Commit Changes
1. Open Source Control panel
2. Stage files by clicking `+` icon
3. Type commit message
4. Click ✓ to commit

### Advanced with GitLens
- See who changed each line
- View commit history
- Compare branches
- Much more!

---

## 📁 Workspace Organization

Recommended folder structure:

```
C:\Users\Jorams\genius-ai\
├── .vscode/              # VS Code settings
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
├── backend/              # Python backend
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                 # Documentation
├── scripts/              # Helper scripts
└── README.md
```

---

## 💡 Pro Tips

### 1. Multi-Cursor Editing
- `Alt+Click`: Add cursor
- `Ctrl+Alt+↑/↓`: Add cursor above/below
- `Ctrl+D`: Select next occurrence
- `Ctrl+Shift+L`: Select all occurrences

### 2. Quick Navigation
- `Ctrl+P`: Quick file open
- `Ctrl+Shift+F`: Search across all files
- `Ctrl+G`: Go to line number
- `F12`: Go to definition
- `Alt+←/→`: Navigate back/forward

### 3. Terminal Management
- `` Ctrl+` ``: Toggle terminal
- `Ctrl+Shift+` `: New terminal
- Split terminal with `Ctrl+Shift+5`
- Run multiple terminals (backend, frontend, etc.)

### 4. Code Snippets
Create custom snippets for common patterns:
- File → Preferences → User Snippets

Example React component snippet:
```json
"React Functional Component": {
  "prefix": "rfc",
  "body": [
    "import React from 'react'",
    "",
    "export default function ${1:ComponentName}() {",
    "  return (",
    "    <div>",
    "      $0",
    "    </div>",
    "  )",
    "}"
  ]
}
```

---

## 🚨 Troubleshooting

### Files Not Appearing in VS Code?

**Solution 1: Check file watcher**
```
File → Preferences → Settings → Search "files.watcherExclude"
```
Make sure your project folder isn't excluded.

**Solution 2: Reload window**
- `Ctrl+Shift+P`
- Type "Reload Window"
- Press Enter

### VS Code Terminal Not Working?

**Solution: Configure default shell**
1. `Ctrl+Shift+P`
2. Type "Terminal: Select Default Profile"
3. Choose "Git Bash" or "PowerShell"

### IntelliSense Not Working?

**For TypeScript/JavaScript:**
```bash
npm install --save-dev @types/node @types/react
```

**For Python:**
```bash
pip install pylint
```

---

## 🎯 Best Practices

### 1. Use Workspaces for Multiple Projects
- File → Add Folder to Workspace
- Save workspace: File → Save Workspace As...

### 2. Keep Extensions Lightweight
- Only install extensions you actually use
- Disable unused extensions per workspace

### 3. Use Integrated Terminal
- Avoid external terminals
- Use split terminals for multiple tasks
- Save terminal commands in `package.json` scripts

### 4. Leverage Tasks
Create `.vscode/tasks.json` for common commands:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd backend && npm run dev",
      "group": "build"
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "cd frontend && npm run dev",
      "group": "build"
    }
  ]
}
```

Run with: `Ctrl+Shift+B`

---

## 🎉 Complete Workflow Example

### Building a Blog Platform

**Step 1: Generate with Pawa AI**
```
In browser: "Create a production-ready blog platform with:
- Next.js 14 frontend with TypeScript
- PostgreSQL database with Prisma ORM
- User authentication with NextAuth.js
- Rich text editor with TipTap
- Image upload with AWS S3
- API routes for CRUD operations
- Responsive design with Tailwind
- Unit tests with Jest
- Deployment config for Vercel"
```

**Step 2: Watch in VS Code**
Files appear instantly:
- `app/page.tsx`
- `app/api/posts/route.ts`
- `prisma/schema.prisma`
- `lib/auth.ts`
- `components/Editor.tsx`
- `tests/posts.test.ts`
- `next.config.js`
- `vercel.json`

**Step 3: Set Up in Terminal**
```bash
# Terminal 1: Install dependencies
npm install

# Terminal 2: Set up database
npx prisma generate
npx prisma db push

# Terminal 3: Run dev server
npm run dev

# Terminal 4: Run tests
npm test
```

**Step 4: Debug and Refine**
1. Set breakpoints in API routes
2. Press `F5` to start debugging
3. Test in browser
4. Fix issues in VS Code
5. Use Pawa AI for additional features

**Step 5: Deploy**
```bash
git add .
git commit -m "Initial blog platform"
git push origin main
# Auto-deploys to Vercel!
```

---

## 🆘 Need Help?

### VS Code Resources
- Official Docs: https://code.visualstudio.com/docs
- Keyboard Shortcuts: `Ctrl+K Ctrl+S`
- Interactive Playground: Help → Welcome

### Pawa AI Resources
- Check `FILE_REFRESH_DEBUG.md` for debugging
- Check `PAWA_AI_UPGRADE_COMPLETE.md` for AI capabilities
- Console logs (F12 in browser) for troubleshooting

---

## ✅ Quick Checklist

Before starting a new project:

- [ ] VS Code opened at `C:\Users\Jorams\genius-ai`
- [ ] Both backends running (ports 8000 & 8001)
- [ ] Browser open at `http://localhost:3000`
- [ ] Recommended extensions installed
- [ ] Git initialized (if needed)
- [ ] `.vscode/settings.json` configured
- [ ] Integrated terminal ready

---

## 🎊 You're All Set!

You now have the **ULTIMATE** development setup:

✅ **Pawa AI** generates production-ready code
✅ **VS Code** gives you professional tools
✅ **Files appear instantly** in both places
✅ **Full debugging** capabilities
✅ **Git integration** for version control
✅ **Thousands of extensions** available

**Start building amazing software! 🚀**

---

*Last Updated: 2025-01-04*
*Pawa AI v6.0 + VS Code Integration*
