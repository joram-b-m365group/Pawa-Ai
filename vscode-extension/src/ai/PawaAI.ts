import axios, { AxiosInstance } from 'axios';

export interface PawaAIConfig {
    apiUrl: string;
    model: string;
    maxTokens: number;
    temperature: number;
    useGemini?: boolean;
    geminiModel?: string;
}

export interface Message {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

export interface ChatResponse {
    response: string;
    files_created?: Array<{ path: string; content: string }>;
    files_modified?: Array<{ path: string; content: string }>;
}

export class PawaAIClient {
    private config: PawaAIConfig;
    private axios: AxiosInstance;

    constructor(config: PawaAIConfig) {
        this.config = config;
        this.axios = axios.create({
            baseURL: config.apiUrl,
            timeout: 120000, // 2 minutes
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    updateConfig(newConfig: Partial<PawaAIConfig>) {
        this.config = { ...this.config, ...newConfig };
        this.axios.defaults.baseURL = this.config.apiUrl;
    }

    /**
     * Stream chat response with callback for each chunk
     */
    async streamChat(
        message: string,
        history: Message[],
        context: string,
        onChunk: (chunk: string) => void,
        onComplete?: () => void,
        onError?: (error: Error) => void
    ): Promise<void> {
        try {
            // Build full message with context
            const fullMessage = context ? `${message}\n\n${context}` : message;

            const response = await this.axios.post(
                '/ai-agent/chat',
                {
                    message: fullMessage,
                    conversation_history: history.map(m => ({
                        role: m.role,
                        content: m.content,
                    })),
                    project_path: process.cwd(),
                    stream: true,
                },
                {
                    responseType: 'stream',
                }
            );

            // Handle streaming response
            let buffer = '';
            response.data.on('data', (chunk: Buffer) => {
                const text = chunk.toString();
                buffer += text;

                // Process complete lines
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.trim()) {
                        onChunk(line);
                    }
                }
            });

            response.data.on('end', () => {
                if (buffer.trim()) {
                    onChunk(buffer);
                }
                onComplete?.();
            });

            response.data.on('error', (error: Error) => {
                onError?.(error);
            });
        } catch (error) {
            onError?.(error as Error);
        }
    }

    /**
     * Non-streaming chat for simple requests
     */
    async chat(
        message: string,
        history: Message[] = [],
        context: string = ''
    ): Promise<ChatResponse> {
        try {
            const fullMessage = context ? `${message}\n\n${context}` : message;

            // Use Gemini if enabled and context is large
            if (this.config.useGemini) {
                const endpoint = '/gemini/chat';
                const response = await this.axios.post(endpoint, {
                    message: fullMessage,
                    conversation_history: history.map(m => ({
                        role: m.role === 'assistant' ? 'model' : m.role,
                        content: m.content,
                    })),
                    model: this.config.geminiModel || 'gemini-2.0-flash',
                    temperature: this.config.temperature,
                });

                return {
                    response: response.data.response || '',
                    files_created: [],
                    files_modified: [],
                };
            }

            const response = await this.axios.post('/ai-agent/chat', {
                message: fullMessage,
                conversation_history: history.map(m => ({
                    role: m.role,
                    content: m.content,
                })),
                project_path: process.cwd(),
                stream: false,
            });

            return {
                response: response.data.response || '',
                files_created: response.data.files_created || [],
                files_modified: response.data.files_modified || [],
            };
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(
                    `Pawa AI API error: ${error.response?.data?.detail || error.message}`
                );
            }
            throw error;
        }
    }

    /**
     * Generate code based on description
     */
    async generateCode(
        description: string,
        language: string,
        context: string = ''
    ): Promise<string> {
        const message = `Generate ${language} code for: ${description}`;
        const response = await this.chat(message, [], context);
        return response.response;
    }

    /**
     * Explain code
     */
    async explainCode(code: string, language: string): Promise<string> {
        const message = `Explain this ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``;
        const response = await this.chat(message);
        return response.response;
    }

    /**
     * Refactor code
     */
    async refactorCode(code: string, language: string): Promise<string> {
        const message = `Refactor this ${language} code to improve readability and performance:\n\n\`\`\`${language}\n${code}\n\`\`\``;
        const response = await this.chat(message);
        return response.response;
    }

    /**
     * Fix bugs in code
     */
    async fixBug(code: string, language: string, bugDescription?: string): Promise<string> {
        const message = bugDescription
            ? `Fix this bug in ${language} code: ${bugDescription}\n\n\`\`\`${language}\n${code}\n\`\`\``
            : `Find and fix bugs in this ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``;
        const response = await this.chat(message);
        return response.response;
    }

    /**
     * Add comments to code
     */
    async addComments(code: string, language: string): Promise<string> {
        const message = `Add clear, helpful comments to this ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``;
        const response = await this.chat(message);
        return response.response;
    }

    /**
     * Generate unit tests
     */
    async generateTests(code: string, language: string, testFramework?: string): Promise<string> {
        const framework = testFramework || this.detectTestFramework(language);
        const message = `Generate ${framework} unit tests for this ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``;
        const response = await this.chat(message);
        return response.response;
    }

    /**
     * Detect appropriate test framework based on language
     */
    private detectTestFramework(language: string): string {
        const frameworks: Record<string, string> = {
            typescript: 'Jest',
            javascript: 'Jest',
            python: 'pytest',
            java: 'JUnit',
            csharp: 'xUnit',
            go: 'testing',
            rust: 'built-in test',
            ruby: 'RSpec',
            php: 'PHPUnit',
        };
        return frameworks[language.toLowerCase()] || 'appropriate';
    }

    /**
     * Check if API is reachable
     */
    async healthCheck(): Promise<boolean> {
        try {
            await this.axios.get('/health');
            return true;
        } catch {
            return false;
        }
    }
}
