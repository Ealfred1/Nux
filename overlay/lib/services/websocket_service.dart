import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/overlay_state.dart';

class WebSocketService extends ChangeNotifier {
  static const String wsUrl = 'ws://127.0.0.1:8000/ws/overlay';
  
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  Timer? _reconnectTimer;
  
  bool _isConnected = false;
  OverlayStateType _currentState = OverlayStateType.idle;
  String? _lastCommand;
  String? _lastResult;
  String? _lastResponse;

  bool get isConnected => _isConnected;
  OverlayStateType get currentState => _currentState;
  String? get lastCommand => _lastCommand;
  String? get lastResult => _lastResult;
  String? get lastResponse => _lastResponse;

  void connect() {
    try {
      debugPrint('Connecting to WebSocket: $wsUrl');
      
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      _isConnected = true;
      notifyListeners();

      // Send initial message
      sendMessage({
        'type': 'overlay_ready',
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      });

      // Listen to messages
      _subscription = _channel!.stream.listen(
        _onMessage,
        onError: _onError,
        onDone: _onDisconnect,
      );

      debugPrint('✅ Connected to backend');
    } catch (e) {
      debugPrint('WebSocket connection error: $e');
      _scheduleReconnect();
    }
  }

  void _onMessage(dynamic message) {
    try {
      final data = json.decode(message);
      final type = data['type'] as String?;

      debugPrint('Received message: $type');

      switch (type) {
        case 'connected':
          debugPrint('Backend confirmed connection');
          break;

        case 'wake_word_detected':
          _updateState(OverlayStateType.listening);
          break;

        case 'listening_started':
          _updateState(OverlayStateType.listening);
          break;

        case 'command_received':
          _lastCommand = data['command'] as String?;
          _updateState(OverlayStateType.processing);
          break;

        case 'command_result':
          final result = data['result'] as Map<String, dynamic>?;
          final response = data['response'] as String?;
          if (result != null) {
            _lastResult = result['result'] as String?;
            _lastResponse = response;
            if (result['success'] == true) {
              _updateState(OverlayStateType.responding);
            } else {
              _updateState(OverlayStateType.error);
            }
          }
          // Return to idle after 4 seconds (longer for TTS)
          Future.delayed(const Duration(seconds: 4), () {
            _updateState(OverlayStateType.idle);
            _lastCommand = null;
            _lastResult = null;
            _lastResponse = null;
          });
          break;

        case 'listening_timeout':
          _updateState(OverlayStateType.error);
          Future.delayed(const Duration(seconds: 2), () {
            _updateState(OverlayStateType.idle);
          });
          break;

        case 'error':
          _updateState(OverlayStateType.error);
          Future.delayed(const Duration(seconds: 2), () {
            _updateState(OverlayStateType.idle);
          });
          break;

        case 'pong':
          // Heartbeat response
          break;
      }
    } catch (e) {
      debugPrint('Error parsing message: $e');
    }
  }

  void _onError(error) {
    debugPrint('WebSocket error: $error');
    _isConnected = false;
    _updateState(OverlayStateType.error);
    _scheduleReconnect();
  }

  void _onDisconnect() {
    debugPrint('WebSocket disconnected');
    _isConnected = false;
    _updateState(OverlayStateType.idle);
    notifyListeners();
    _scheduleReconnect();
  }

  void _scheduleReconnect() {
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(const Duration(seconds: 5), () {
      if (!_isConnected) {
        debugPrint('Attempting to reconnect...');
        connect();
      }
    });
  }

  void _updateState(OverlayStateType newState) {
    if (_currentState != newState) {
      _currentState = newState;
      notifyListeners();
    }
  }

  void sendMessage(Map<String, dynamic> message) {
    if (_channel != null && _isConnected) {
      _channel!.sink.add(json.encode(message));
    }
  }

  void sendHeartbeat() {
    sendMessage({
      'type': 'ping',
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    });
  }

  @override
  void dispose() {
    _reconnectTimer?.cancel();
    _subscription?.cancel();
    _channel?.sink.close();
    super.dispose();
  }
}

