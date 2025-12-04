(function () {
    const vscode = acquireVsCodeApi();

    const messagesContainer = document.getElementById('messages');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const clearBtn = document.getElementById('clearBtn');

    let isLoading = false;
    let currentAssistantMessage = null;

    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);

    // Send message on Enter (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Clear chat history
    clearBtn.addEventListener('click', () => {
        vscode.postMessage({ type: 'clearHistory' });
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message || isLoading) {
            return;
        }

        vscode.postMessage({
            type: 'sendMessage',
            message: message,
        });

        messageInput.value = '';
        messageInput.style.height = 'auto';
    }

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });

    // Handle messages from extension
    window.addEventListener('message', (event) => {
        const message = event.data;

        switch (message.type) {
            case 'userMessage':
                addUserMessage(message.message);
                break;
            case 'assistantChunk':
                appendAssistantChunk(message.chunk);
                break;
            case 'loading':
                isLoading = message.isLoading;
                if (message.isLoading) {
                    showLoading();
                } else {
                    hideLoading();
                }
                sendBtn.disabled = message.isLoading;
                break;
            case 'error':
                showError(message.error);
                break;
            case 'clearChat':
                messagesContainer.innerHTML = '';
                break;
        }
    });

    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `
            <div class="message-header">
                <div class="message-icon">👤</div>
                <span>You</span>
            </div>
            <div class="message-content">${escapeHtml(text)}</div>
        `;
        messagesContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function appendAssistantChunk(chunk) {
        if (!currentAssistantMessage) {
            currentAssistantMessage = document.createElement('div');
            currentAssistantMessage.className = 'message assistant-message';
            currentAssistantMessage.innerHTML = `
                <div class="message-header">
                    <div class="message-icon">🤖</div>
                    <span>Pawa AI</span>
                </div>
                <div class="message-content"></div>
            `;
            messagesContainer.appendChild(currentAssistantMessage);
        }

        const contentDiv = currentAssistantMessage.querySelector('.message-content');
        const currentContent = contentDiv.textContent || '';
        const newContent = currentContent + chunk;

        // Parse markdown-style code blocks
        contentDiv.innerHTML = parseMarkdown(newContent);
        scrollToBottom();
    }

    function showLoading() {
        hideLoading(); // Remove any existing loading indicator

        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant-message';
        loadingDiv.id = 'loading-indicator';
        loadingDiv.innerHTML = `
            <div class="message-header">
                <div class="message-icon">🤖</div>
                <span>Pawa AI</span>
            </div>
            <div class="loading">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        `;
        messagesContainer.appendChild(loadingDiv);
        scrollToBottom();

        // Prepare for new assistant message
        currentAssistantMessage = null;
    }

    function hideLoading() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    function showError(errorMessage) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = `Error: ${errorMessage}`;
        messagesContainer.appendChild(errorDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function parseMarkdown(text) {
        // Simple markdown parser for code blocks
        let html = escapeHtml(text);

        // Parse code blocks with language
        html = html.replace(
            /```(\w+)?\n([\s\S]*?)```/g,
            (match, lang, code) => {
                const language = lang || 'text';
                return `
                    <div class="code-block">
                        <div class="code-block-header">
                            <span>${language}</span>
                            <div class="code-block-actions">
                                <button onclick="copyCode(this)" title="Copy code">Copy</button>
                                <button onclick="applyCode(this, '${language}')" title="Apply to editor">Apply</button>
                            </div>
                        </div>
                        <pre><code>${code.trim()}</code></pre>
                    </div>
                `;
            }
        );

        // Parse inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Parse bold
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Parse italic
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Parse line breaks
        html = html.replace(/\n/g, '<br>');

        return html;
    }

    // Global functions for code block actions
    window.copyCode = function (button) {
        const codeBlock = button.closest('.code-block');
        const code = codeBlock.querySelector('code').textContent;

        navigator.clipboard.writeText(code).then(() => {
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
    };

    window.applyCode = function (button, language) {
        const codeBlock = button.closest('.code-block');
        const code = codeBlock.querySelector('code').textContent;

        vscode.postMessage({
            type: 'applyCode',
            code: code,
            language: language,
        });

        button.textContent = 'Applied!';
        setTimeout(() => {
            button.textContent = 'Apply';
        }, 2000);
    };
})();
