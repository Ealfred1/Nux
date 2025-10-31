import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/websocket_service.dart';
import '../widgets/listening_indicator.dart';
import '../widgets/command_display.dart';
import '../models/overlay_state.dart';

class OverlayScreen extends StatefulWidget {
  const OverlayScreen({super.key});

  @override
  State<OverlayScreen> createState() => _OverlayScreenState();
}

class _OverlayScreenState extends State<OverlayScreen> with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );
    
    // Connect to backend
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final wsService = Provider.of<WebSocketService>(context, listen: false);
      wsService.connect();
      
      // Listen to state changes
      wsService.addListener(() {
        if (wsService.currentState == OverlayStateType.listening ||
            wsService.currentState == OverlayStateType.processing) {
          _animationController.forward();
        } else if (wsService.currentState == OverlayStateType.idle) {
          _animationController.reverse();
        }
      });
    });
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Consumer<WebSocketService>(
        builder: (context, wsService, child) {
          return Center(
            child: FadeTransition(
              opacity: _fadeAnimation,
              child: Container(
                width: 400,
                height: 300,
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.85),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(
                    color: _getBorderColor(wsService.currentState),
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: _getBorderColor(wsService.currentState).withOpacity(0.5),
                      blurRadius: 20,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Logo/Brand
                    Text(
                      'NuxAI',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue[400],
                        letterSpacing: 2,
                      ),
                    ),
                    const SizedBox(height: 30),
                    
                    // Listening Indicator
                    ListeningIndicator(
                      state: wsService.currentState,
                    ),
                    
                    const SizedBox(height: 20),
                    
                    // Command Display
                    CommandDisplay(
                      command: wsService.lastCommand,
                      result: wsService.lastResult,
                      response: wsService.lastResponse,
                    ),
                    
                    const SizedBox(height: 20),
                    
                    // Status Text
                    Text(
                      _getStatusText(wsService.currentState),
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.grey[400],
                      ),
                    ),
                    
                    // Connection Status
                    if (!wsService.isConnected)
                      Padding(
                        padding: const EdgeInsets.only(top: 10),
                        child: Text(
                          'Connecting to backend...',
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.orange[400],
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Color _getBorderColor(OverlayStateType state) {
    switch (state) {
      case OverlayStateType.listening:
        return Colors.blue[400]!;
      case OverlayStateType.processing:
        return Colors.purple[400]!;
      case OverlayStateType.responding:
        return Colors.green[400]!;
      case OverlayStateType.error:
        return Colors.red[400]!;
      default:
        return Colors.grey[700]!;
    }
  }

  String _getStatusText(OverlayStateType state) {
    switch (state) {
      case OverlayStateType.listening:
        return 'Listening...';
      case OverlayStateType.processing:
        return 'Processing...';
      case OverlayStateType.responding:
        return 'Executing...';
      case OverlayStateType.error:
        return 'Error occurred';
      default:
        return 'Ready';
    }
  }
}

