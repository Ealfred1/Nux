#!/usr/bin/env python3
"""
Comprehensive NuxAI API Test Script
Tests all endpoints with curl-like functionality using Python requests
"""
import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws/overlay"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}")

def print_test(name):
    print(f"\n{Colors.BLUE}🧪 {name}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ️  {msg}{Colors.END}")

async def test_root_endpoint():
    """Test root endpoint"""
    print_test("1. ROOT ENDPOINT (GET /)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {response.status}")
                    print(json.dumps(data, indent=2))
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_health_endpoint():
    """Test health check endpoint"""
    print_test("2. HEALTH CHECK (GET /api/health)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {response.status}")
                    print(json.dumps(data, indent=2))
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_status_endpoint():
    """Test detailed status endpoint"""
    print_test("3. STATUS ENDPOINT (GET /api/status)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print_success(f"Status: {response.status}")
                    print(json.dumps(data, indent=2))
                    
                    # Show feature summary
                    features = data.get('features', {})
                    enabled = sum(1 for v in features.values() if v)
                    print_info(f"Features: {enabled}/{len(features)} enabled")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_settings_page():
    """Test settings web UI"""
    print_test("4. SETTINGS UI (GET /settings)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/settings") as response:
                if response.status == 200:
                    html = await response.text()
                    print_success(f"Status: {response.status}")
                    print_info(f"Page size: {len(html)} bytes")
                    print_info(f"Contains 'NuxAI Settings': {'Yes' if 'NuxAI Settings' in html else 'No'}")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_api_docs():
    """Test API documentation"""
    print_test("5. API DOCUMENTATION (GET /docs)")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/docs") as response:
                if response.status == 200:
                    html = await response.text()
                    print_success(f"Status: {response.status}")
                    print_info(f"Swagger UI loaded ({len(html)} bytes)")
                    return True
                else:
                    print_error(f"Status: {response.status}")
                    return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

async def test_websocket():
    """Test WebSocket connection"""
    print_test("6. WEBSOCKET (WS /ws/overlay)")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(WS_URL) as ws:
                print_success("WebSocket connected")
                
                # Send test message
                test_msg = {
                    "type": "overlay_ready",
                    "timestamp": datetime.now().timestamp()
                }
                await ws.send_json(test_msg)
                print_info(f"Sent: {test_msg['type']}")
                
                # Wait for response
                try:
                    msg = await asyncio.wait_for(ws.receive(), timeout=5.0)
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        print_success(f"Received: {data.get('type', 'unknown')}")
                        print(json.dumps(data, indent=2))
                        return True
                except asyncio.TimeoutError:
                    print_error("Timeout waiting for response")
                    return False
                    
    except Exception as e:
        print_error(f"Error: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print_header("🚀 NuxAI Comprehensive API Test Suite")
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Status Endpoint", test_status_endpoint),
        ("Settings UI", test_settings_page),
        ("API Documentation", test_api_docs),
        ("WebSocket", test_websocket),
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
    print_header("📊 Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed ({passed*100//total}%){Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 All tests passed!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️  {total-passed} test(s) failed{Colors.END}")
    
    print_header("🔗 Quick Links")
    print(f"  • API Docs: {BASE_URL}/docs")
    print(f"  • Settings: {BASE_URL}/settings")
    print(f"  • Health: {BASE_URL}/api/health")
    print(f"  • Status: {BASE_URL}/api/status")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
