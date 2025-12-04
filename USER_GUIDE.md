# Genius AI - User Guide

Welcome to Genius AI! Your intelligent assistant powered by FREE 70B AI models.

## Getting Started

### Access the App
Open your browser and go to: **http://localhost:3000**

You'll see a beautiful welcome screen with quick-action buttons.

---

## Basic Features

### 1. Ask Questions
Simply type your question in the text box and press Enter!

**Examples:**
- "What is artificial intelligence?"
- "Explain quantum physics in simple terms"
- "Write a poem about coding"
- "Help me debug this Python code"

### 2. Code Generation
Genius AI can write code in any programming language!

**Try asking:**
- "Write a Python function to calculate fibonacci"
- "Create a React component with state"
- "Show me SQL to join tables"
- "Write a JavaScript array sorting function"

**Bonus:** Code is automatically highlighted with beautiful syntax colors!

### 3. Upload Images
Click the paperclip icon (📎) to upload and analyze images.

**What you can do:**
- "What's in this image?"
- "Describe the colors and composition"
- "Read any text in this image"
- "What's the mood of this photo?"
- "Identify objects in this picture"

**Supported formats:** PNG, JPG, JPEG, GIF, WebP

### 4. Analyze Documents
Upload text files, PDFs, or code files for analysis.

**Use cases:**
- Summarize long documents
- Find bugs in code
- Translate documents
- Extract key points
- Answer questions about the content

**Supported formats:** TXT, PDF, MD, code files

---

## Advanced Features

### 5. Switch AI Models
Click the Settings icon (⚙️) in the input area to see 5 different AI models:

**Models:**
- **Llama 3.3 70B** (Default) - Most intelligent, best for complex tasks
- **Llama 3.1 8B Instant** - Super fast responses
- **Mixtral 8x7B** - Best for long documents (32k tokens)
- **Gemma 2 9B** - Balanced speed and quality
- **Llama 3.2 90B Vision** - Automatic for image analysis

**When to switch:**
- Need faster responses? → 8B Instant
- Long document? → Mixtral 8x7B
- Complex task? → Keep 70B (default)

### 6. Copy AI Responses
Hover over any AI message and click the copy icon (top-right corner).

Perfect for:
- Copying code snippets
- Saving explanations
- Sharing with others

### 7. Export Conversations
Click the "Export" button to download your entire chat as a text file.

**Use cases:**
- Save important conversations
- Archive research notes
- Keep code examples
- Create documentation

### 8. Share Conversations
Click "Share" to share via:
- WhatsApp (mobile)
- Email
- Social media
- Or copy to clipboard (desktop)

### 9. Voice Input
Click the microphone icon (🎤) to record voice messages.

**How it works:**
- Click mic → Grant permission
- Speak your message
- Click again to stop
- (Text conversion coming soon!)

### 10. Clear Conversation
Click the red "Clear" button to start a new conversation.

**Note:** You'll be asked to confirm (prevents accidents)

---

## Tips & Tricks

### Keyboard Shortcuts
- **Enter** - Send message
- **Shift + Enter** - New line (for multi-line messages)

### Multi-line Messages
Hold Shift and press Enter to write longer messages:
```
Tell me about:
1. Machine learning
2. Deep learning
3. Neural networks
```

### Follow-up Questions
Genius AI remembers your conversation! Ask follow-up questions naturally:

**Example:**
```
You: "What's React?"
AI: [explains React]
You: "Show me an example"
AI: [provides React code - knows you mean React!]
You: "How do I add styling?"
AI: [explains React styling]
```

### File Uploads
**Best practices:**
- Keep images under 10MB for faster processing
- For documents, first 50,000 characters are analyzed
- Supported: Images, PDFs, text files, code files

### Getting Better Responses
**Be specific:**
- ❌ "Write code"
- ✅ "Write a Python function to validate email addresses"

**Provide context:**
- ❌ "Fix this"
- ✅ "Fix this Python code that's giving a syntax error on line 5"

**Ask for formatting:**
- "Explain with examples and bullet points"
- "Write in simple terms for beginners"
- "Provide step-by-step instructions"

---

## Common Use Cases

### For Students
- Homework help and explanations
- Research assistance
- Essay brainstorming
- Math problem solving
- Study notes generation

### For Developers
- Code generation
- Bug fixing
- Code review
- Documentation writing
- Algorithm explanations

### For Writers
- Content creation
- Brainstorming ideas
- Proofreading
- Style suggestions
- Research assistance

### For Business
- Email drafting
- Report summarization
- Data analysis insights
- Presentation outlines
- Meeting notes organization

### For Creators
- Image analysis and descriptions
- Creative prompts
- Story ideas
- Design feedback
- Content ideation

---

## Limitations

### Rate Limits
- 60 requests per minute
- If exceeded, wait 60 seconds

### File Sizes
- Maximum: 20MB per file
- Recommended: Under 10MB for images

### Context Length
- Most models: 8,192 tokens (~6,000 words)
- Mixtral: 32,768 tokens (~24,000 words)

---

## Privacy & Security

### What We Store
- Conversations are stored **only in your browser**
- No data sent to our servers (except API calls to Groq)
- Clear browser data = conversations deleted

### What We DON'T Store
- Your personal information
- Account details (no accounts needed!)
- Uploaded files (processed and discarded)
- Conversation history on servers

### Groq Privacy
- Groq processes your requests
- Read Groq's privacy policy at console.groq.com
- Your data is not used to train models

---

## Troubleshooting

### "Error: Request failed"
**Solution:**
- Check your internet connection
- Refresh the page
- Try again in a few seconds

### "Rate limit exceeded"
**Solution:**
- Wait 60 seconds
- Reduce request frequency

### "File too large"
**Solution:**
- Compress your image
- Split large documents
- Maximum: 20MB

### Page won't load
**Solution:**
- Check if you're on http://localhost:3000
- Clear browser cache
- Try a different browser

### AI gives weird response
**Solution:**
- Rephrase your question
- Be more specific
- Try a different AI model

---

## Feedback & Support

### Found a bug?
Let us know! We want to make Genius AI better.

### Have suggestions?
We'd love to hear your ideas for new features.

### Need help?
Check these docs or contact support.

---

## Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| Enter | Send message |
| Shift + Enter | New line |
| Ctrl/Cmd + K | Focus input (planned) |
| Esc | Close modals (planned) |

---

## Quick Tips Summary

1. ✅ **Be specific** in your questions
2. ✅ **Use follow-ups** - AI remembers context
3. ✅ **Try different models** for different tasks
4. ✅ **Upload images** for visual analysis
5. ✅ **Copy responses** with one click
6. ✅ **Export chats** to save important conversations
7. ✅ **Shift+Enter** for multi-line messages
8. ✅ **Hover to copy** any AI response

---

## Example Conversations

### Example 1: Learning to Code
```
You: I want to learn Python. Where do I start?
AI: [explains Python basics]
You: Show me a simple example
AI: [provides "Hello World" code]
You: How do I run this?
AI: [explains how to execute Python]
```

### Example 2: Image Analysis
```
[Upload photo of a sunset]
You: Describe this image
AI: [detailed description of sunset, colors, composition]
You: What time of day was this taken?
AI: [analyzes lighting and estimates time]
```

### Example 3: Code Debugging
```
You: This Python code gives an error [paste code]
AI: [identifies bug on line X]
You: How do I fix it?
AI: [provides corrected code with explanation]
```

---

## Welcome to Genius AI!

You now have access to:
- 🤖 5 powerful AI models
- 🖼️ Image analysis
- 📄 Document processing
- 💻 Code generation with syntax highlighting
- 📱 Mobile-friendly interface
- 💾 Export & share capabilities
- 🎤 Voice input (coming soon)

**100% FREE. No limits on creativity.**

Start chatting now! 🚀
