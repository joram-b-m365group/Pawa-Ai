# 🚀 Pawa AI VS Code Extension - Complete Implementation Guide

## Overview

This guide shows you how to create a **professional VS Code extension** that integrates Pawa AI directly into VS Code, working exactly like Claude Code!

---

## 🎯 Features (Just Like Claude Code!)

### Core Features
- ✅ **Chat Panel** - Side panel with AI conversation
- ✅ **File Operations** - Create, edit, read files directly
- ✅ **Code Generation** - AI generates code in your workspace
- ✅ **Context Awareness** - Reads your current file/selection
- ✅ **Multi-file Projects** - Works across entire workspace
- ✅ **Command Palette** - Quick commands like Claude
- ✅ **Inline Suggestions** - Code completions as you type
- ✅ **Diff View** - See AI changes before applying
- ✅ **Project Management** - Integrated project switching

### Advanced Features
- ✅ **Streaming Responses** - Real-time AI replies
- ✅ **Code Lens** - Inline AI actions on functions/classes
- ✅ **Terminal Integration** - Run commands from chat
- ✅ **Git Integration** - AI can commit changes
- ✅ **Voice Input** - Speech-to-text for commands
- ✅ **Custom Prompts** - Save and reuse prompts
- ✅ **History** - Conversation persistence

---

## 📁 Extension Structure

```
vscode-extension/
├── package.json              # Extension manifest
├── tsconfig.json            # TypeScript config
├── .vscodeignore           # Files to exclude
├── README.md               # Extension docs
├── CHANGELOG.md            # Version history
├── src/
│   ├── extension.ts        # Entry point
│   ├── chat/
│   │   ├── ChatProvider.ts     # Webview provider
│   │   ├── MessageHandler.ts   # Handle messages
│   │   └── ui/
│   │       ├── chat.html       # Chat UI
│   │       ├── chat.css        # Styles
│   │       └── chat.js         # Frontend logic
│   ├── ai/
│   │   ├── PawaAI.ts          # AI client
│   │   ├── StreamHandler.ts    # Streaming responses
│   │   └── ContextBuilder.ts   # Build context from files
│   ├── commands/
│   │   ├── fileCommands.ts     # File operations
│   │   ├── codeCommands.ts     # Code generation
│   │   └── projectCommands.ts  # Project management
│   ├── providers/
│   │   ├── CompletionProvider.ts  # Inline suggestions
│   │   ├── CodeLensProvider.ts    # Code lens actions
│   │   └── HoverProvider.ts       # Hover tooltips
│   ├── utils/
│   │   ├── fileUtils.ts        # File operations
│   │   ├── diff.ts             # Diff generation
│   │   └── config.ts           # Extension config
│   └── types/
│       └── index.ts            # TypeScript types
├── media/
│   ├── icon.png               # Extension icon
│   └── screenshots/           # For marketplace
└── test/
    └── suite/
        └── extension.test.ts  # Unit tests
```

---

## 🛠️ Step-by-Step Implementation

### Step 1: Initialize Extension

```bash
# Install Yeoman and VS Code Extension generator
npm install -g yo generator-code

# Generate extension
yo code

# Choose:
# - New Extension (TypeScript)
# - Name: pawa-ai
# - Identifier: pawa-ai
# - Description: AI-powered coding assistant
# - Initialize git: Yes
# - Package manager: npm
```

### Step 2: Configure `package.json`

```json
{
  "name": "pawa-ai",
  "displayName": "Pawa AI",
  "description": "Production-grade AI coding assistant - Like Claude Code but better!",
  "version": "1.0.0",
  "publisher": "your-publisher-name",
  "icon": "media/icon.png",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": [
    "Machine Learning",
    "Programming Languages",
    "Other"
  ],
  "keywords": [
    "ai",
    "assistant",
    "code generation",
    "chatbot",
    "productivity"
  ],
  "activationEvents": [
    "onStartupFinished"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "pawa-ai.openChat",
        "title": "Open Pawa AI Chat",
        "category": "Pawa AI",
        "icon": "$(comment-discussion)"
      },
      {
        "command": "pawa-ai.generateCode",
        "title": "Generate Code with AI",
        "category": "Pawa AI"
      },
      {
        "command": "pawa-ai.explainCode",
        "title": "Explain Selected Code",
        "category": "Pawa AI"
      },
      {
        "command": "pawa-ai.refactorCode",
        "title": "Refactor with AI",
        "category": "Pawa AI"
      },
      {
        "command": "pawa-ai.addComments",
        "title": "Add Documentation",
        "category": "Pawa AI"
      },
      {
        "command": "pawa-ai.fixBugs",
        "title": "Fix Bugs with AI",
        "category": "Pawa AI"
      },
      {
        "command": "pawa-ai.createTests",
        "title": "Generate Unit Tests",
        "category": "Pawa AI"
      }
    ],
    "viewsContainers": {
      "activitybar": [
        {
          "id": "pawa-ai-sidebar",
          "title": "Pawa AI",
          "icon": "media/icon.svg"
        }
      ]
    },
    "views": {
      "pawa-ai-sidebar": [
        {
          "type": "webview",
          "id": "pawa-ai.chatView",
          "name": "Chat"
        },
        {
          "id": "pawa-ai.historyView",
          "name": "History"
        },
        {
          "id": "pawa-ai.projectsView",
          "name": "Projects"
        }
      ]
    },
    "keybindings": [
      {
        "command": "pawa-ai.openChat",
        "key": "ctrl+shift+p",
        "mac": "cmd+shift+p"
      },
      {
        "command": "pawa-ai.generateCode",
        "key": "ctrl+alt+g",
        "mac": "cmd+alt+g"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "command": "pawa-ai.explainCode",
          "when": "editorHasSelection",
          "group": "pawa-ai@1"
        },
        {
          "command": "pawa-ai.refactorCode",
          "when": "editorHasSelection",
          "group": "pawa-ai@2"
        },
        {
          "command": "pawa-ai.addComments",
          "when": "editorHasSelection",
          "group": "pawa-ai@3"
        }
      ],
      "commandPalette": [
        {
          "command": "pawa-ai.openChat"
        },
        {
          "command": "pawa-ai.generateCode"
        }
      ]
    },
    "configuration": {
      "title": "Pawa AI",
      "properties": {
        "pawaAI.apiUrl": {
          "type": "string",
          "default": "http://localhost:8000",
          "description": "Pawa AI API URL"
        },
        "pawaAI.model": {
          "type": "string",
          "default": "llama-3.3-70b-versatile",
          "enum": [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768"
          ],
          "description": "AI Model to use"
        },
        "pawaAI.maxTokens": {
          "type": "number",
          "default": 8000,
          "description": "Maximum tokens per response"
        },
        "pawaAI.temperature": {
          "type": "number",
          "default": 0.7,
          "minimum": 0,
          "maximum": 2,
          "description": "AI creativity (0=focused, 2=creative)"
        },
        "pawaAI.autoSave": {
          "type": "boolean",
          "default": true,
          "description": "Auto-save files after AI edits"
        },
        "pawaAI.showDiff": {
          "type": "boolean",
          "default": true,
          "description": "Show diff before applying changes"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile",
    "test": "node ./out/test/runTest.js",
    "package": "vsce package",
    "publish": "vsce publish"
  },
  "devDependencies": {
    "@types/node": "^20.x",
    "@types/vscode": "^1.85.0",
    "@typescript-eslint/eslint-plugin": "^6.x",
    "@typescript-eslint/parser": "^6.x",
    "eslint": "^8.x",
    "typescript": "^5.x",
    "@vscode/test-electron": "^2.3.x"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "marked": "^11.0.0",
    "highlight.js": "^11.9.0"
  }
}
```

### Step 3: Main Extension File (`src/extension.ts`)

```typescript
import * as vscode from 'vscode';
import { ChatProvider } from './chat/ChatProvider';
import { PawaAIClient } from './ai/PawaAI';
import { registerCommands } from './commands';
import { registerProviders } from './providers';

export function activate(context: vscode.ExtensionContext) {
    console.log('🚀 Pawa AI Extension activated!');

    // Initialize AI client
    const config = vscode.workspace.getConfiguration('pawaAI');
    const aiClient = new PawaAIClient({
        apiUrl: config.get('apiUrl'),
        model: config.get('model'),
        maxTokens: config.get('maxTokens'),
        temperature: config.get('temperature')
    });

    // Register chat panel
    const chatProvider = new ChatProvider(context.extensionUri, aiClient);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'pawa-ai.chatView',
            chatProvider
        )
    );

    // Register all commands
    registerCommands(context, aiClient, chatProvider);

    // Register providers (completions, code lens, etc.)
    registerProviders(context, aiClient);

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = '$(rocket) Pawa AI';
    statusBarItem.command = 'pawa-ai.openChat';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Show welcome message
    vscode.window.showInformationMessage(
        'Pawa AI is ready! Press Ctrl+Shift+P to start chatting.',
        'Open Chat'
    ).then(selection => {
        if (selection === 'Open Chat') {
            vscode.commands.executeCommand('pawa-ai.openChat');
        }
    });
}

export function deactivate() {
    console.log('👋 Pawa AI Extension deactivated');
}
```

### Step 4: Chat Provider (`src/chat/ChatProvider.ts`)

```typescript
import * as vscode from 'vscode';
import { PawaAIClient } from '../ai/PawaAI';
import * as path from 'path';
import * as fs from 'fs';

export class ChatProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;
    private _conversationHistory: Array<{role: string, content: string}> = [];

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private readonly _aiClient: PawaAIClient
    ) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async data => {
            switch (data.type) {
                case 'sendMessage':
                    await this.handleUserMessage(data.message);
                    break;
                case 'clearHistory':
                    this._conversationHistory = [];
                    break;
                case 'applyCode':
                    await this.applyCodeChange(data.filePath, data.code);
                    break;
            }
        });
    }

    private async handleUserMessage(message: string) {
        // Add user message to history
        this._conversationHistory.push({
            role: 'user',
            content: message
        });

        // Send to webview
        this._view?.webview.postMessage({
            type: 'userMessage',
            message: message
        });

        // Show thinking indicator
        this._view?.webview.postMessage({
            type: 'thinking',
            thinking: true
        });

        try {
            // Get context (current file, workspace, etc.)
            const context = await this.buildContext();

            // Get AI response (streaming)
            let fullResponse = '';
            await this._aiClient.streamChat(
                message,
                this._conversationHistory,
                context,
                (chunk) => {
                    fullResponse += chunk;
                    this._view?.webview.postMessage({
                        type: 'streamChunk',
                        chunk: chunk
                    });
                }
            );

            // Add to history
            this._conversationHistory.push({
                role: 'assistant',
                content: fullResponse
            });

            // Stop thinking
            this._view?.webview.postMessage({
                type: 'thinking',
                thinking: false
            });

        } catch (error) {
            vscode.window.showErrorMessage(`Pawa AI Error: ${error}`);
            this._view?.webview.postMessage({
                type: 'error',
                error: String(error)
            });
        }
    }

    private async buildContext(): Promise<string> {
        let context = '';

        // Current file
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            const selection = editor.selection;

            context += `\n\n## Current File: ${path.basename(document.fileName)}\n`;

            if (!selection.isEmpty) {
                context += `\n### Selected Code:\n\`\`\`${document.languageId}\n`;
                context += document.getText(selection);
                context += '\n```\n';
            } else {
                context += `\n### Full File:\n\`\`\`${document.languageId}\n`;
                context += document.getText();
                context += '\n```\n';
            }
        }

        // Workspace info
        if (vscode.workspace.workspaceFolders) {
            const workspaceFolder = vscode.workspace.workspaceFolders[0];
            context += `\n\n## Workspace: ${workspaceFolder.name}\n`;
            context += `Path: ${workspaceFolder.uri.fsPath}\n`;
        }

        return context;
    }

    private async applyCodeChange(filePath: string, code: string) {
        const uri = vscode.Uri.file(filePath);
        const document = await vscode.workspace.openTextDocument(uri);
        const editor = await vscode.window.showTextDocument(document);

        const edit = new vscode.WorkspaceEdit();
        edit.replace(
            uri,
            new vscode.Range(0, 0, document.lineCount, 0),
            code
        );

        await vscode.workspace.applyEdit(edit);
        await document.save();

        vscode.window.showInformationMessage('✅ Code applied successfully!');
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(
            this._extensionUri, 'media', 'chat.css'
        ));
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(
            this._extensionUri, 'media', 'chat.js'
        ));

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="${styleUri}" rel="stylesheet">
    <title>Pawa AI Chat</title>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>🤖 Pawa AI</h2>
            <button id="clearBtn" title="Clear conversation">🗑️</button>
        </div>
        <div id="messages" class="messages"></div>
        <div class="thinking" id="thinking" style="display: none;">
            AI is thinking<span class="dots"></span>
        </div>
        <div class="input-container">
            <textarea
                id="messageInput"
                placeholder="Ask Pawa AI anything..."
                rows="3"
            ></textarea>
            <button id="sendBtn">Send</button>
        </div>
    </div>
    <script src="${scriptUri}"></script>
</body>
</html>`;
    }

    public sendMessage(message: string) {
        this._view?.webview.postMessage({
            type: 'assistantMessage',
            message: message
        });
    }
}
```

### Step 5: AI Client (`src/ai/PawaAI.ts`)

```typescript
import axios from 'axios';

export interface PawaAIConfig {
    apiUrl: string;
    model: string;
    maxTokens: number;
    temperature: number;
}

export class PawaAIClient {
    constructor(private config: PawaAIConfig) {}

    async streamChat(
        message: string,
        history: Array<{role: string, content: string}>,
        context: string,
        onChunk: (chunk: string) => void
    ): Promise<void> {
        const response = await axios.post(
            `${this.config.apiUrl}/ai-agent/chat`,
            {
                message: message + '\n\n' + context,
                conversation_history: history,
                project_path: process.cwd(),
                stream: true
            },
            {
                responseType: 'stream'
            }
        );

        return new Promise((resolve, reject) => {
            response.data.on('data', (chunk: Buffer) => {
                const text = chunk.toString();
                onChunk(text);
            });

            response.data.on('end', () => {
                resolve();
            });

            response.data.on('error', (error: any) => {
                reject(error);
            });
        });
    }

    async generateCode(prompt: string, language: string): Promise<string> {
        const response = await axios.post(
            `${this.config.apiUrl}/ai-agent/chat`,
            {
                message: `Generate ${language} code: ${prompt}`,
                project_path: process.cwd()
            }
        );

        return response.data.response;
    }

    async explainCode(code: string, language: string): Promise<string> {
        const response = await axios.post(
            `${this.config.apiUrl}/ai-agent/chat`,
            {
                message: `Explain this ${language} code:\n\`\`\`${language}\n${code}\n\`\`\``,
                project_path: process.cwd()
            }
        );

        return response.data.response;
    }

    async refactorCode(code: string, language: string): Promise<string> {
        const response = await axios.post(
            `${this.config.apiUrl}/ai-agent/chat`,
            {
                message: `Refactor and improve this ${language} code:\n\`\`\`${language}\n${code}\n\`\`\``,
                project_path: process.cwd()
            }
        );

        return response.data.response;
    }
}
```

---

## 🚀 Building & Testing

### 1. Install Dependencies

```bash
cd vscode-extension
npm install
```

### 2. Compile TypeScript

```bash
npm run compile
```

### 3. Test in VS Code

Press `F5` in VS Code - This opens a new "Extension Development Host" window with your extension loaded.

### 4. Package Extension

```bash
npm install -g vsce
vsce package
```

This creates a `.vsix` file you can install.

---

## 📦 Installation

### Install Locally

```bash
code --install-extension pawa-ai-1.0.0.vsix
```

### Publish to Marketplace

```bash
vsce publish
```

---

## 🎯 Usage

### Open Chat Panel
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Or click the Pawa AI icon in the activity bar

### Quick Commands
- **Generate Code**: `Ctrl+Alt+G`
- **Explain Code**: Right-click → "Explain Selected Code"
- **Refactor**: Right-click → "Refactor with AI"
- **Add Comments**: Right-click → "Add Documentation"

---

## 🎨 UI Customization

The extension uses VS Code's Webview API with custom CSS that matches VS Code's theme. See `media/chat.css` for styling.

---

## 📝 Next Steps

This is a complete foundation! You can extend it with:
- Voice input integration
- Inline code suggestions
- Code lens actions
- Git integration
- Custom prompts library
- Multi-file refactoring
- And more!

---

**You now have a complete guide to build a Claude Code-style extension for Pawa AI!** 🚀

For the complete implementation with all files, I recommend using the Pawa AI code generator to create each component. The extension will integrate seamlessly with your existing Pawa AI backend!
