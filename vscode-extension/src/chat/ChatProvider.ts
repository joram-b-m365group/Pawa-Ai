import * as vscode from 'vscode';
import * as path from 'path';
import { PawaAIClient, Message } from '../ai/PawaAI';

export class ChatProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;
    private conversationHistory: Message[] = [];

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private aiClient: PawaAIClient,
        private context: vscode.ExtensionContext
    ) {
        // Load conversation history from storage
        this.loadHistory();
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(this._extensionUri, 'media'),
            ],
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'sendMessage':
                    await this.handleUserMessage(data.message);
                    break;
                case 'clearHistory':
                    this.clearHistory();
                    break;
                case 'applyCode':
                    await this.applyCode(data.code, data.language, data.filePath);
                    break;
            }
        });
    }

    private async handleUserMessage(userMessage: string) {
        if (!this._view) {
            return;
        }

        // Add user message to history
        this.conversationHistory.push({
            role: 'user',
            content: userMessage,
        });

        // Show user message in webview
        this._view.webview.postMessage({
            type: 'userMessage',
            message: userMessage,
        });

        // Build context from current editor
        const context = await this.buildContext();

        // Show loading state
        this._view.webview.postMessage({ type: 'loading', isLoading: true });

        // Stream AI response
        let fullResponse = '';
        try {
            await this.aiClient.streamChat(
                userMessage,
                this.conversationHistory.slice(0, -1), // Exclude current message
                context,
                (chunk) => {
                    fullResponse += chunk;
                    this._view?.webview.postMessage({
                        type: 'assistantChunk',
                        chunk: chunk,
                    });
                },
                () => {
                    // On complete
                    this.conversationHistory.push({
                        role: 'assistant',
                        content: fullResponse,
                    });
                    this.saveHistory();
                    this._view?.webview.postMessage({
                        type: 'loading',
                        isLoading: false,
                    });
                },
                (error) => {
                    // On error
                    console.error('Pawa AI error:', error);
                    this._view?.webview.postMessage({
                        type: 'error',
                        error: error.message,
                    });
                    this._view?.webview.postMessage({
                        type: 'loading',
                        isLoading: false,
                    });
                }
            );
        } catch (error) {
            console.error('Streaming error:', error);
            this._view?.webview.postMessage({
                type: 'error',
                error: 'Failed to connect to Pawa AI. Make sure the backend is running.',
            });
            this._view?.webview.postMessage({
                type: 'loading',
                isLoading: false,
            });
        }
    }

    private async buildContext(): Promise<string> {
        let context = '';

        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            const selection = editor.selection;

            // Add current file info
            context += `\n\n## Current File: ${path.basename(document.fileName)}\n`;
            context += `Language: ${document.languageId}\n`;

            // If there's a selection, include it
            if (!selection.isEmpty) {
                const selectedText = document.getText(selection);
                context += `\n### Selected Code:\n\`\`\`${document.languageId}\n${selectedText}\n\`\`\`\n`;
            } else {
                // Include some context lines around cursor
                const config = vscode.workspace.getConfiguration('pawa-ai');
                const contextLines = config.get<number>('autoContextLines') || 50;

                const startLine = Math.max(0, selection.start.line - contextLines);
                const endLine = Math.min(document.lineCount - 1, selection.start.line + contextLines);
                const range = new vscode.Range(startLine, 0, endLine, document.lineAt(endLine).text.length);
                const contextText = document.getText(range);

                context += `\n### Context (lines ${startLine + 1}-${endLine + 1}):\n\`\`\`${document.languageId}\n${contextText}\n\`\`\`\n`;
            }

            // Add cursor position
            context += `\nCursor position: Line ${selection.start.line + 1}, Column ${selection.start.character + 1}\n`;
        }

        // Add workspace info
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            context += `\n## Workspace: ${workspaceFolder.name}\n`;
            context += `Path: ${workspaceFolder.uri.fsPath}\n`;
        }

        return context;
    }

    private async applyCode(code: string, language: string, filePath?: string) {
        const config = vscode.workspace.getConfiguration('pawa-ai');
        const showDiff = config.get<boolean>('showDiffBeforeApply') || true;

        if (filePath) {
            // Apply to specific file
            const uri = vscode.Uri.file(filePath);
            try {
                const document = await vscode.workspace.openTextDocument(uri);
                const editor = await vscode.window.showTextDocument(document);

                if (showDiff) {
                    // Show diff first
                    const tempUri = uri.with({ scheme: 'untitled', path: uri.path + '.new' });
                    const tempDoc = await vscode.workspace.openTextDocument(tempUri);
                    const tempEdit = new vscode.WorkspaceEdit();
                    tempEdit.insert(tempUri, new vscode.Position(0, 0), code);
                    await vscode.workspace.applyEdit(tempEdit);

                    await vscode.commands.executeCommand('vscode.diff', uri, tempUri, 'Pawa AI Changes');
                } else {
                    // Apply directly
                    const edit = new vscode.WorkspaceEdit();
                    const fullRange = new vscode.Range(
                        document.positionAt(0),
                        document.positionAt(document.getText().length)
                    );
                    edit.replace(uri, fullRange, code);
                    await vscode.workspace.applyEdit(edit);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to apply code: ${error}`);
            }
        } else {
            // Insert at cursor position
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                await editor.edit((editBuilder) => {
                    editBuilder.insert(editor.selection.active, code);
                });
            } else {
                // Create new file
                const document = await vscode.workspace.openTextDocument({
                    language: language,
                    content: code,
                });
                await vscode.window.showTextDocument(document);
            }
        }
    }

    public sendMessage(message: string) {
        if (this._view) {
            this._view.webview.postMessage({
                type: 'userMessage',
                message: message,
            });
            this.handleUserMessage(message);
        }
    }

    public clearHistory() {
        this.conversationHistory = [];
        this.saveHistory();
        this._view?.webview.postMessage({ type: 'clearChat' });
        vscode.window.showInformationMessage('Chat history cleared');
    }

    private loadHistory() {
        const saved = this.context.globalState.get<Message[]>('pawa-ai.chatHistory');
        if (saved) {
            this.conversationHistory = saved;
        }
    }

    private saveHistory() {
        // Keep only last 50 messages to avoid storage issues
        const recentHistory = this.conversationHistory.slice(-50);
        this.context.globalState.update('pawa-ai.chatHistory', recentHistory);
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        const styleUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.css')
        );
        const scriptUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.js')
        );

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
            <h2>Pawa AI</h2>
            <button id="clearBtn" title="Clear chat history">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M2 5v9a1 1 0 001 1h10a1 1 0 001-1V5H2zm3 8H4V7h1v6zm2 0H6V7h1v6zm2 0H8V7h1v6zm2 0h-1V7h1v6z"/>
                    <path d="M13.5 2H10V.5A.5.5 0 009.5 0h-3a.5.5 0 00-.5.5V2H2.5a.5.5 0 000 1h11a.5.5 0 000-1zM9 2H7V1h2v1z"/>
                </svg>
            </button>
        </div>

        <div id="messages" class="messages"></div>

        <div class="input-container">
            <textarea
                id="messageInput"
                placeholder="Ask Pawa AI anything..."
                rows="3"
            ></textarea>
            <button id="sendBtn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2.01 2L2 8l13 2-13 2 .01 6L21 10z"/>
                </svg>
            </button>
        </div>
    </div>

    <script src="${scriptUri}"></script>
</body>
</html>`;
    }
}
