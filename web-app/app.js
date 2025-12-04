// Configuration
const CONFIG = {
    API_URL: 'http://localhost:8000',
    MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
    SUPPORTED_IMAGES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    SUPPORTED_VIDEOS: ['video/mp4', 'video/webm', 'video/ogg'],
    MAX_MESSAGE_LENGTH: 10000,
};

// State Management
const state = {
    conversationId: null,
    messages: [],
    attachments: [],
    isProcessing: false,
    messagesCount: 0,
    avgResponseTime: 2.0,
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    checkBackendStatus();
    setInterval(checkBackendStatus, 30000); // Check every 30s
});

async function initializeApp() {
    console.log('🚀 Genius AI initialized');
    loadConversations();
    setupEventListeners();
}

function setupEventListeners() {
    const messageInput = document.getElementById('messageInput');
    messageInput.addEventListener('input', () => {
        updateCharCount();
    });
}

// Backend Status Check
async function checkBackendStatus() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/health`);
        const data = await response.json();
        updateStatusIndicator(true, data);
    } catch (error) {
        updateStatusIndicator(false);
        console.error('Backend connection failed:', error);
    }
}

function updateStatusIndicator(isOnline, data = null) {
    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.status-dot');

    if (isOnline) {
        statusText.textContent = 'Connected to Intelligent AI Server';
        statusDot.style.background = 'var(--success)';
    } else {
        statusText.textContent = 'Disconnected - Attempting to reconnect...';
        statusDot.style.background = 'var(--danger)';
    }
}

// Conversation Management
function startNewChat() {
    state.conversationId = null;
    state.messages = [];
    state.attachments = [];
    clearMessages();
    showWelcomeScreen();
    saveConversations();
}

function loadConversations() {
    const saved = localStorage.getItem('genius_conversations');
    if (saved) {
        const conversations = JSON.parse(saved);
        renderConversations(conversations);
    }
}

function saveConversations() {
    // Save to localStorage
    const conversations = state.messages.length > 0 ? [{
        id: state.conversationId,
        title: state.messages[0]?.content?.substring(0, 50) || 'New Chat',
        timestamp: Date.now(),
        messages: state.messages
    }] : [];

    localStorage.setItem('genius_conversations', JSON.stringify(conversations));
}

function renderConversations(conversations) {
    const list = document.getElementById('conversationsList');
    list.innerHTML = conversations.map(conv => `
        <div class="conversation-item ${conv.id === state.conversationId ? 'active' : ''}"
             onclick="loadConversation('${conv.id}')">
            <div style="font-weight: 600; margin-bottom: 0.25rem;">${conv.title}</div>
            <div style="font-size: 0.75rem; color: var(--text-tertiary);">
                ${new Date(conv.timestamp).toLocaleDateString()}
            </div>
        </div>
    `).join('');
}

// Message Handling
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message && state.attachments.length === 0) return;
    if (state.isProcessing) return;

    hideWelcomeScreen();

    // Add user message
    addMessage({
        role: 'user',
        content: message,
        attachments: [...state.attachments],
        timestamp: Date.now()
    });

    // Clear input
    input.value = '';
    state.attachments = [];
    document.getElementById('attachmentsPreview').innerHTML = '';
    updateCharCount();

    // Process message
    state.isProcessing = true;
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    try {
        const startTime = Date.now();

        // Show thinking indicator
        const thinkingId = addThinkingIndicator();

        // Send to backend with real-time streaming
        await sendToBackend(message, state.attachments);

        // Remove thinking indicator
        removeThinkingIndicator(thinkingId);

        // Update stats
        const responseTime = (Date.now() - startTime) / 1000;
        updateStats(responseTime);

    } catch (error) {
        console.error('Send message error:', error);
        addMessage({
            role: 'assistant',
            content: `❌ **Error**: ${error.message}\n\nPlease ensure the backend server is running at ${CONFIG.API_URL}`,
            timestamp: Date.now()
        });
    } finally {
        state.isProcessing = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

async function sendToBackend(message, attachments) {
    // Prepare request
    const requestBody = {
        message: message,
        conversation_id: state.conversationId,
        use_rag: true,
        temperature: 0.7,
        max_tokens: 2048,
    };

    // For demo: simulate image/video analysis
    if (attachments.length > 0) {
        const mediaDesc = attachments.map(att => {
            if (att.type.startsWith('image/')) {
                return `[Uploaded image: ${att.name}]`;
            } else if (att.type.startsWith('video/')) {
                return `[Uploaded video: ${att.name}]`;
            }
            return `[Uploaded file: ${att.name}]`;
        }).join(' ');

        requestBody.message = `${mediaDesc}\n\n${message}`;
    }

    // Send request
    const response = await fetch(`${CONFIG.API_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Update conversation ID
    state.conversationId = data.conversation_id;

    // Add assistant response
    addMessage({
        role: 'assistant',
        content: data.response,
        timestamp: Date.now(),
        metadata: data.metadata
    });

    saveConversations();
}

function sendExample(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
}

// Message Display
function addMessage(message) {
    state.messages.push(message);

    const container = document.getElementById('messagesContainer');
    const messageEl = createMessageElement(message);

    container.appendChild(messageEl);
    scrollToBottom();
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message ${message.role}-message`;

    const avatarIcon = message.role === 'user'
        ? '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2m8-10a4 4 0 100-8 4 4 0 000 8z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        : '<path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';

    div.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                ${avatarIcon}
            </svg>
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-author">${message.role === 'user' ? 'You' : 'Genius AI'}</span>
                <span class="message-time">${formatTime(message.timestamp)}</span>
            </div>
            <div class="message-body">
                ${formatMessageContent(message)}
            </div>
        </div>
    `;

    return div;
}

function formatMessageContent(message) {
    let content = message.content;

    // Handle attachments
    if (message.attachments && message.attachments.length > 0) {
        const attachmentsHtml = message.attachments.map(att => {
            if (att.type.startsWith('image/')) {
                return `<img src="${att.dataUrl}" alt="${att.name}" onclick="openMediaModal('${att.dataUrl}', 'image')">`;
            } else if (att.type.startsWith('video/')) {
                return `<video src="${att.dataUrl}" controls onclick="openMediaModal('${att.dataUrl}', 'video')"></video>`;
            }
            return '';
        }).join('');

        content = attachmentsHtml + content;
    }

    // Format markdown-style content
    content = content
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');

    // Handle code blocks
    content = content.replace(/```(.+?)```/gs, '<pre><code>$1</code></pre>');

    // Add metadata badge if available
    if (message.metadata) {
        content += `
            <div style="margin-top: 1rem; padding: 0.75rem; background: var(--surface); border-radius: var(--radius-md); font-size: 0.875rem;">
                <strong>🧠 Agent Analysis:</strong><br>
                Agents used: ${message.metadata.agents_used?.join(', ') || 'N/A'}<br>
                Mode: ${message.metadata.mode || 'standard'}
            </div>
        `;
    }

    return content;
}

function addThinkingIndicator() {
    const id = `thinking-${Date.now()}`;
    const container = document.getElementById('messagesContainer');

    const div = document.createElement('div');
    div.id = id;
    div.className = 'message assistant-message';
    div.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-body">
                <div class="thinking-indicator">
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                </div>
            </div>
        </div>
    `;

    container.appendChild(div);
    scrollToBottom();

    return id;
}

function removeThinkingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function clearMessages() {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '';
}

// File Handling
function handleFileSelect(event) {
    const files = Array.from(event.target.files);

    files.forEach(file => {
        if (file.size > CONFIG.MAX_FILE_SIZE) {
            alert(`File ${file.name} is too large. Maximum size is 50MB.`);
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            state.attachments.push({
                name: file.name,
                type: file.type,
                size: file.size,
                dataUrl: e.target.result
            });

            renderAttachments();
        };

        reader.readAsDataURL(file);
    });

    // Reset input
    event.target.value = '';
}

function renderAttachments() {
    const preview = document.getElementById('attachmentsPreview');
    preview.innerHTML = state.attachments.map((att, index) => {
        const isImage = att.type.startsWith('image/');
        const isVideo = att.type.startsWith('video/');

        return `
            <div class="attachment-item">
                ${isImage ? `<img src="${att.dataUrl}" alt="${att.name}">` : ''}
                ${isVideo ? `<video src="${att.dataUrl}"></video>` : ''}
                ${!isImage && !isVideo ? `<div style="padding: 1rem;">📄 ${att.name}</div>` : ''}
                <div class="attachment-remove" onclick="removeAttachment(${index})">×</div>
            </div>
        `;
    }).join('');
}

function removeAttachment(index) {
    state.attachments.splice(index, 1);
    renderAttachments();
}

// Voice Input (Placeholder)
function toggleVoiceInput() {
    alert('Voice input feature coming soon! 🎤');
    // TODO: Implement Web Speech API
}

// UI Utilities
function showWelcomeScreen() {
    document.getElementById('welcomeScreen').style.display = 'block';
}

function hideWelcomeScreen() {
    document.getElementById('welcomeScreen').style.display = 'none';
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function updateCharCount() {
    const input = document.getElementById('messageInput');
    const count = document.getElementById('charCount');
    count.textContent = `${input.value.length} / ${CONFIG.MAX_MESSAGE_LENGTH}`;

    if (input.value.length > CONFIG.MAX_MESSAGE_LENGTH) {
        count.style.color = 'var(--danger)';
    } else {
        count.style.color = 'var(--text-tertiary)';
    }
}

function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;

    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function updateStats(responseTime) {
    state.messagesCount++;
    state.avgResponseTime = ((state.avgResponseTime * (state.messagesCount - 1)) + responseTime) / state.messagesCount;

    document.getElementById('messagesCount').textContent = state.messagesCount;
    document.getElementById('avgResponseTime').textContent = `~${state.avgResponseTime.toFixed(1)}s`;
}

// Modal Functions
function openMediaModal(url, type) {
    const modal = document.getElementById('mediaModal');
    const body = document.getElementById('modalBody');

    if (type === 'image') {
        body.innerHTML = `<img src="${url}" style="max-width: 100%; border-radius: var(--radius-lg);">`;
    } else if (type === 'video') {
        body.innerHTML = `<video src="${url}" controls autoplay style="max-width: 100%; border-radius: var(--radius-lg);"></video>`;
    }

    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('mediaModal').classList.remove('active');
}

// Keyboard Shortcuts
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Loading Overlay
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

// Error Handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// Export for debugging
window.GeniusAI = {
    state,
    sendMessage,
    startNewChat,
    checkBackendStatus,
};

console.log('✨ Genius AI loaded. Use window.GeniusAI to access app state.');
