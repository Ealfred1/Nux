#!/usr/bin/env python3
"""
NuxAI API Test Suite
Tests all endpoints, WebSocket, and features
"""
import asyncio
import aiohttp
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/overlay"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}🧪 Testing: {name}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ️  {msg}{Colors.END}")

async def test_root_endpoint():
    """Test root endpoint"""
    print_test("Root Endpoint (GET /)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {response.status}")
                    print_info(f"Service: {data.get('name')} v{data.get('version')}")
                    print_info(f"Message: {data.get('message')}")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_health_endpoint():
    """Test health check endpoint"""
    print_test("Health Check (GET /api/health)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {data.get('status')}")
                    print_info(f"Service: {data.get('service')} v{data.get('version')}")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_status_endpoint():
    """Test detailed status endpoint"""
    print_test("Status Check (GET /api/status)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {data.get('status')}")
                    print_info(f"Personality: {data.get('personality', {}).get('name')}")
                    
                    features = data.get('features', {})
                    print_info(f"Features: {len([k for k, v in features.items() if v])} enabled")
                    for feature, enabled in features.items():
                        status = "✓" if enabled else "✗"
                        print(f"    {status} {feature}")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_settings_page():
    """Test settings web UI"""
    print_test("Settings UI (GET /settings)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/settings") as response:
                if response.status == 200:
                    html = await response.text()
                    print_success(f"Settings page loaded ({len(html)} bytes)")
                    if "NuxAI Settings" in html:
                        print_info("Page contains expected content")
                        return True
                    else:
                        print_error("Page content unexpected")
                        return False
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_websocket_connection():
    """Test WebSocket connection"""
    print_test("WebSocket Connection (WS /ws/overlay)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(WS_URL) as ws:
                print_success("WebSocket connected")
                
                # Send overlay ready message
                await ws.send_json({
                    "type": "overlay_ready",
                    "timestamp": datetime.now().timestamp()
                })
                print_info("Sent: overlay_ready")
                
                # Wait for response
                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=5.0)
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        print_success(f"Received: {data.get('type')}")
                        print_info(f"Message: {data.get('message', 'N/A')}")
                        return True
                except asyncio.TimeoutError:
                    print_error("Timeout waiting for response")
                    return False
                    
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_api_docs():
    """Test API documentation"""
    print_test("API Documentation (GET /docs)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/docs") as response:
                if response.status == 200:
                    html = await response.text()
                    print_success(f"API docs accessible ({len(html)} bytes)")
                    print_info(f"URL: {BASE_URL}/docs")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def run_all_tests():
    """Run all tests"""
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}🚀 NuxAI API Test Suite{Colors.END}")
    print(f"{'='*60}")
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Status Endpoint", test_status_endpoint),
        ("Settings UI", test_settings_page),
        ("API Documentation", test_api_docs),
        ("WebSocket", test_websocket_connection),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test failed with exception: {e}")
            results.append((name, False))
        
        await asyncio.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}📊 Test Summary{Colors.END}")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 All tests passed!{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}⚠️  Some tests failed{Colors.END}")
        return 1

async def main():
    """Main entry point"""
    print(f"{Colors.YELLOW}Connecting to NuxAI backend...{Colors.END}")
    print(f"{Colors.YELLOW}Make sure the backend is running: python backend/main.py{Colors.END}")
    
    await asyncio.sleep(1)
    
    exit_code = await run_all_tests()
    
    print(f"\n{Colors.BLUE}Quick Links:{Colors.END}")
    print(f"  • API Docs: {BASE_URL}/docs")
    print(f"  • Settings: {BASE_URL}/settings")
    print(f"  • Health: {BASE_URL}/api/health")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted{Colors.END}")
        sys.exit(1)

