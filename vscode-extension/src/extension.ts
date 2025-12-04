import * as vscode from 'vscode';
import { ChatProvider } from './chat/ChatProvider';
import { PawaAIClient } from './ai/PawaAI';
import { registerCommands } from './commands';

let aiClient: PawaAIClient;
let chatProvider: ChatProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('🚀 Pawa AI Extension activated!');

    // Get configuration
    const config = vscode.workspace.getConfiguration('pawa-ai');

    // Initialize AI client
    aiClient = new PawaAIClient({
        apiUrl: config.get('apiUrl') || 'http://localhost:8000',
        model: config.get('model') || 'llama-3.3-70b-versatile',
        maxTokens: config.get('maxTokens') || 4096,
        temperature: config.get('temperature') || 0.7,
    });

    // Initialize chat provider
    chatProvider = new ChatProvider(context.extensionUri, aiClient, context);

    // Register webview provider
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'pawa-ai.chatView',
            chatProvider
        )
    );

    // Register all commands
    registerCommands(context, aiClient, chatProvider);

    // Show welcome message
    vscode.window.showInformationMessage(
        '🎉 Pawa AI is ready! Press Ctrl+Shift+P to open chat.',
        'Open Chat'
    ).then(selection => {
        if (selection === 'Open Chat') {
            vscode.commands.executeCommand('pawa-ai.openChat');
        }
    });

    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('pawa-ai')) {
                const newConfig = vscode.workspace.getConfiguration('pawa-ai');
                aiClient.updateConfig({
                    apiUrl: newConfig.get('apiUrl') || 'http://localhost:8000',
                    model: newConfig.get('model') || 'llama-3.3-70b-versatile',
                    maxTokens: newConfig.get('maxTokens') || 4096,
                    temperature: newConfig.get('temperature') || 0.7,
                });
            }
        })
    );
}

export function deactivate() {
    console.log('👋 Pawa AI Extension deactivated');
}
