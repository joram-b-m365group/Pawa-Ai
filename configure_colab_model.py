#!/usr/bin/env python3
"""
Quick setup script to configure your Colab model with Genius AI
"""
import requests
import sys

def configure_model(ngrok_url):
    """Configure Genius AI to use your Colab model"""

    # Ensure URL ends with /chat
    if not ngrok_url.endswith('/chat'):
        if ngrok_url.endswith('/'):
            ngrok_url = ngrok_url + 'chat'
        else:
            ngrok_url = ngrok_url + '/chat'

    print("=" * 60)
    print("CONFIGURING GENIUS AI - CUSTOM MODEL")
    print("=" * 60)
    print(f"\nModel URL: {ngrok_url}")

    try:
        # Configure the model
        response = requests.post(
            'http://localhost:8000/custom-model/config',
            json={
                'model_url': ngrok_url,
                'model_name': 'Colab Custom Model',
                'timeout': 60
            }
        )

        if response.status_code == 200:
            result = response.json()
            print("\n✅ Configuration successful!")
            print(f"   Model: {result['model_name']}")
            print(f"   URL: {result['model_url']}")

            # Test the connection
            print("\n🔍 Testing connection...")
            test_response = requests.post(
                'http://localhost:8000/custom-chat',
                json={'message': 'Hello! This is a test from Genius AI.'}
            )

            if test_response.status_code == 200:
                print("✅ Connection test successful!")
                test_result = test_response.json()
                print(f"   Model responded: {test_result['model']}")
                print(f"   Response time: {test_result.get('processing_time', 0):.2f}s")
            else:
                print(f"⚠️  Connection test failed: {test_response.status_code}")
                print(f"   Error: {test_response.text}")
                print("\n💡 Make sure:")
                print("   1. Your Colab notebook is running")
                print("   2. The ngrok tunnel is active")
                print("   3. Your Flask endpoint accepts POST requests at /chat")

            print("\n" + "=" * 60)
            print("READY TO USE!")
            print("=" * 60)
            print("\n📌 Available endpoints:")
            print("   /chat          - Groq (default)")
            print("   /custom-chat   - Your Colab model")
            print("   /hybrid-chat   - Groq + Colab (best of both!)")
            print("\n🌐 Open: http://localhost:3000")
            print("=" * 60)

        else:
            print(f"\n❌ Configuration failed: {response.status_code}")
            print(f"   Error: {response.text}")

    except requests.ConnectionError:
        print("\n❌ Cannot connect to Genius AI backend")
        print("   Make sure the backend is running on http://localhost:8000")
        print("   Run: cd backend && python super_intelligent_endpoint.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("GENIUS AI - COLAB MODEL SETUP")
    print("=" * 60)

    if len(sys.argv) > 1:
        # URL provided as command line argument
        ngrok_url = sys.argv[1]
        configure_model(ngrok_url)
    else:
        # Interactive mode
        print("\n📝 Enter your Colab ngrok URL:")
        print("   Example: https://abc123.ngrok.io")
        print("   (The /chat endpoint will be added automatically)\n")

        ngrok_url = input("ngrok URL: ").strip()

        if ngrok_url:
            configure_model(ngrok_url)
        else:
            print("\n❌ No URL provided. Exiting.")
            print("\nUsage:")
            print("   python configure_colab_model.py https://your-ngrok-url.ngrok.io")
            print("   OR")
            print("   python configure_colab_model.py  (interactive mode)")
