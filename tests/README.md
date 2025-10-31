# 🧪 NuxAI Tests

Test suite for verifying NuxAI functionality.

## 📋 Available Tests

### test_api.py
Complete API and WebSocket test suite.

```bash
# Make sure backend is running first!
cd backend && python main.py &

# Run tests
python tests/test_api.py
```

Tests:
- ✅ Root endpoint (GET /)
- ✅ Health check (GET /api/health)
- ✅ Status endpoint (GET /api/status)
- ✅ Settings UI (GET /settings)
- ✅ API documentation (GET /docs)
- ✅ WebSocket connection (WS /ws/overlay)

### Expected Output

```
🚀 NuxAI API Test Suite
============================================================

🧪 Testing: Root Endpoint (GET /)
✅ Status: 200
ℹ️  Service: NuxAI v1.0.0

🧪 Testing: WebSocket Connection (WS /ws/overlay)
✅ WebSocket connected
✅ Received: connected

============================================================
📊 Test Summary
============================================================
✅ PASS - Root Endpoint
✅ PASS - Health Check
✅ PASS - Status Endpoint
✅ PASS - Settings UI
✅ PASS - API Documentation
✅ PASS - WebSocket

Results: 6/6 tests passed
🎉 All tests passed!
```

## 🔧 Prerequisites

```bash
pip install aiohttp
```

## 🚦 Running Tests

### 1. Start Backend

```bash
cd backend
python main.py
```

### 2. Run Tests

```bash
python tests/test_api.py
```

## 📊 Test Coverage

- REST API endpoints
- WebSocket connections
- Health checks
- Service status
- Web UI availability
- API documentation

## 🐛 Troubleshooting

### Backend not running
```
Error: Connection refused
```
**Solution:** Start backend first

### Port conflict
```
Error: Address already in use
```
**Solution:** Stop other services on port 8000

### Missing dependencies
```
ModuleNotFoundError: No module named 'aiohttp'
```
**Solution:** `pip install aiohttp`

## 📝 Adding New Tests

Add test functions to `test_api.py`:

```python
async def test_my_feature():
    """Test my new feature"""
    print_test("My Feature (GET /my-endpoint)")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/my-endpoint") as response:
            if response.status == 200:
                print_success("Feature works!")
                return True
    return False
```

Then add to `run_all_tests()`:
```python
tests = [
    # ... existing tests
    ("My Feature", test_my_feature),
]
```

## 🎯 CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    python backend/main.py &
    sleep 5
    python tests/test_api.py
```

See [docs/guides/RUN_TESTS.md](../docs/guides/RUN_TESTS.md) for more details.

