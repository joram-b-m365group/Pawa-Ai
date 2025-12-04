import * as vscode from 'vscode';
import { PawaAIClient } from '../ai/PawaAI';
import { ChatProvider } from '../chat/ChatProvider';

export function registerCommands(
    context: vscode.ExtensionContext,
    aiClient: PawaAIClient,
    chatProvider: ChatProvider
) {
    // Open Chat command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.openChat', () => {
            vscode.commands.executeCommand('pawa-ai.chatView.focus');
        })
    );

    // Generate Code command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.generateCode', async () => {
            const description = await vscode.window.showInputBox({
                prompt: 'What code do you want to generate?',
                placeHolder: 'e.g., A function to sort an array of objects by date',
            });

            if (!description) {
                return;
            }

            const editor = vscode.window.activeTextEditor;
            const language = editor?.document.languageId || 'typescript';

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Generating code with Pawa AI...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const code = await aiClient.generateCode(description, language);

                        if (editor) {
                            await editor.edit((editBuilder) => {
                                editBuilder.insert(editor.selection.active, code);
                            });
                            vscode.window.showInformationMessage('Code generated successfully!');
                        } else {
                            const document = await vscode.workspace.openTextDocument({
                                language: language,
                                content: code,
                            });
                            await vscode.window.showTextDocument(document);
                        }
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to generate code: ${error}`);
                    }
                }
            );
        })
    );

    // Explain Code command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.explainCode', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('Please select some code to explain');
                return;
            }

            const code = editor.document.getText(selection);
            const language = editor.document.languageId;

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Explaining code...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const explanation = await aiClient.explainCode(code, language);

                        // Show explanation in chat
                        chatProvider.sendMessage(`Explain this code:\n\`\`\`${language}\n${code}\n\`\`\``);

                        // Also show as notification
                        const action = await vscode.window.showInformationMessage(
                            'Code explanation ready in chat panel',
                            'Open Chat'
                        );
                        if (action === 'Open Chat') {
                            vscode.commands.executeCommand('pawa-ai.openChat');
                        }
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to explain code: ${error}`);
                    }
                }
            );
        })
    );

    // Refactor Code command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.refactorCode', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('Please select some code to refactor');
                return;
            }

            const code = editor.document.getText(selection);
            const language = editor.document.languageId;

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Refactoring code...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const refactoredCode = await aiClient.refactorCode(code, language);

                        // Show diff
                        const originalUri = editor.document.uri;
                        const tempUri = originalUri.with({
                            scheme: 'untitled',
                            path: originalUri.path + '.refactored',
                        });

                        const tempDoc = await vscode.workspace.openTextDocument(tempUri);
                        const tempEdit = new vscode.WorkspaceEdit();
                        tempEdit.insert(tempUri, new vscode.Position(0, 0), refactoredCode);
                        await vscode.workspace.applyEdit(tempEdit);

                        await vscode.commands.executeCommand(
                            'vscode.diff',
                            originalUri,
                            tempUri,
                            'Pawa AI: Refactored Code'
                        );
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to refactor code: ${error}`);
                    }
                }
            );
        })
    );

    // Fix Bug command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.fixBug', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('Please select some code to fix');
                return;
            }

            const bugDescription = await vscode.window.showInputBox({
                prompt: 'Describe the bug (optional)',
                placeHolder: 'e.g., Function returns undefined instead of array',
            });

            const code = editor.document.getText(selection);
            const language = editor.document.languageId;

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Fixing bug...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const fixedCode = await aiClient.fixBug(code, language, bugDescription);

                        // Replace selected code
                        await editor.edit((editBuilder) => {
                            editBuilder.replace(selection, fixedCode);
                        });

                        vscode.window.showInformationMessage('Bug fix applied!');
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to fix bug: ${error}`);
                    }
                }
            );
        })
    );

    // Add Comments command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.addComments', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('Please select some code to comment');
                return;
            }

            const code = editor.document.getText(selection);
            const language = editor.document.languageId;

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Adding comments...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const commentedCode = await aiClient.addComments(code, language);

                        // Replace selected code
                        await editor.edit((editBuilder) => {
                            editBuilder.replace(selection, commentedCode);
                        });

                        vscode.window.showInformationMessage('Comments added!');
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to add comments: ${error}`);
                    }
                }
            );
        })
    );

    // Generate Tests command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.generateTests', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('Please select some code to test');
                return;
            }

            const code = editor.document.getText(selection);
            const language = editor.document.languageId;

            vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'Generating tests...',
                    cancellable: false,
                },
                async () => {
                    try {
                        const tests = await aiClient.generateTests(code, language);

                        // Create new test file
                        const testFileName = editor.document.fileName.replace(
                            /\.(ts|js|py|java|go|rs)$/,
                            '.test$1'
                        );

                        const document = await vscode.workspace.openTextDocument({
                            language: language,
                            content: tests,
                        });
                        await vscode.window.showTextDocument(document);

                        vscode.window.showInformationMessage('Tests generated! Save the file to keep them.');
                    } catch (error) {
                        vscode.window.showErrorMessage(`Failed to generate tests: ${error}`);
                    }
                }
            );
        })
    );

    // Clear History command
    context.subscriptions.push(
        vscode.commands.registerCommand('pawa-ai.clearHistory', () => {
            chatProvider.clearHistory();
        })
    );
}
