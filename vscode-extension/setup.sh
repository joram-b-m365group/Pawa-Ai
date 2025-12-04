#!/bin/bash

# Pawa AI VS Code Extension - Setup Script
# This script sets up the development environment and builds the extension

set -e  # Exit on error

echo "🚀 Pawa AI VS Code Extension - Setup Script"
echo "============================================"
echo ""

# Check Node.js
echo "📦 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version is too old. Please upgrade to Node.js 16+."
    exit 1
fi

echo "✅ Node.js $(node -v) found"

# Check npm
echo "📦 Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi
echo "✅ npm $(npm -v) found"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Compile TypeScript
echo ""
echo "🔨 Compiling TypeScript..."
npm run compile

if [ $? -ne 0 ]; then
    echo "❌ TypeScript compilation failed"
    exit 1
fi
echo "✅ TypeScript compiled successfully"

# Check if vsce is installed
echo ""
echo "📦 Checking vsce (VS Code Extension Manager)..."
if ! command -v vsce &> /dev/null; then
    echo "⚠️  vsce not found. Installing globally..."
    npm install -g @vscode/vsce
    echo "✅ vsce installed"
else
    echo "✅ vsce found"
fi

# Verify build output
echo ""
echo "🔍 Verifying build output..."
if [ ! -d "out" ]; then
    echo "❌ Build output directory 'out' not found"
    exit 1
fi

if [ ! -f "out/extension.js" ]; then
    echo "❌ Main extension file 'out/extension.js' not found"
    exit 1
fi

echo "✅ Build output verified"

# Display next steps
echo ""
echo "============================================"
echo "✨ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Test the extension:"
echo "   - Open this folder in VS Code"
echo "   - Press F5 to launch Extension Development Host"
echo ""
echo "2️⃣  Package the extension:"
echo "   npm run package"
echo "   (Creates pawa-ai-1.0.0.vsix)"
echo ""
echo "3️⃣  Install the extension:"
echo "   code --install-extension pawa-ai-1.0.0.vsix"
echo ""
echo "4️⃣  Make sure Pawa AI backend is running:"
echo "   http://localhost:8000"
echo ""
echo "📚 Documentation:"
echo "   - QUICK_START.md  : Quick start guide"
echo "   - README.md       : Full documentation"
echo "   - INSTALLATION.md : Installation guide"
echo ""
echo "Happy coding with Pawa AI! 🎉"
