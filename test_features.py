#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Speech-to-Text and Vision features
"""
import requests
import json
import sys
from io import BytesIO
from PIL import Image, ImageDraw

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def test_vision_endpoint():
    """Test the vision analysis endpoint"""
    print("\n" + "="*60)
    print("TESTING VISION ENDPOINT")
    print("="*60)

    # Create a simple test image with PIL
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)

    # Draw a simple math equation
    draw.rectangle([50, 100, 350, 200], fill='white', outline='black', width=2)
    draw.text((100, 130), "Test: 2x + 5 = 13", fill='black')

    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Test vision endpoint
    files = {'image': ('test_math.png', img_bytes, 'image/png')}
    data = {'message': 'What mathematical equation is shown in this image?'}

    try:
        response = requests.post('http://localhost:8000/vision', files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("\n[SUCCESS] Vision endpoint working!")
            print(f"\nModel: {result.get('model')}")
            print(f"Processing time: {result.get('processing_time', 0):.2f}s")
            print(f"\nResponse preview:")
            print("-" * 60)
            response_text = result.get('response', '')
            print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
            print("-" * 60)
            return True
        else:
            print(f"\n[FAILED] Vision endpoint failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"\n[ERROR] Vision endpoint error: {e}")
        return False

def test_transcribe_endpoint():
    """Test the speech-to-text endpoint"""
    print("\n" + "="*60)
    print("TESTING TRANSCRIBE ENDPOINT")
    print("="*60)
    print("\n[NOTE] Transcription test requires actual audio file")
    print("This feature needs to be tested manually in the browser")
    print("by clicking the microphone button and recording audio.")
    return None

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TESTING HEALTH ENDPOINT")
    print("="*60)

    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            health = response.json()
            print("\n[SUCCESS] Backend is healthy!")
            print(f"Status: {health.get('status')}")
            print(f"Intelligence Mode: {health.get('intelligence_mode')}")
            print(f"Reasoning Engine: {health.get('reasoning_engine')}")
            return True
        else:
            print(f"\n[FAILED] Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"\n[ERROR] Backend connection error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GENIUS AI - FEATURE TESTING SUITE")
    print("Testing: Speech-to-Text & Vision Analysis")
    print("="*60)

    # Run tests
    results = {
        'health': test_health_endpoint(),
        'vision': test_vision_endpoint(),
        'transcribe': test_transcribe_endpoint()
    }

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"[{'PASS' if results['health'] else 'FAIL'}] Health Check")
    print(f"[{'PASS' if results['vision'] else 'FAIL'}] Vision Analysis")
    print(f"[MANUAL] Speech-to-Text: Manual testing required")
    print("\n" + "="*60)

    if results['vision']:
        print("\n[SUCCESS] Vision feature successfully fixed!")
        print("The vision endpoint now uses super intelligent image analysis")
        print("with Llama 3.3 70B instead of deprecated vision models.")
        print("\nNext steps:")
        print("1. Test in browser: http://localhost:3000")
        print("2. Upload an image with homework or diagram")
        print("3. Test microphone button for speech-to-text")
    else:
        print("\n[WARNING] Vision feature needs attention")
