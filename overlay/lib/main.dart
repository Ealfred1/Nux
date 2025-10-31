import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:window_manager/window_manager.dart';
import 'services/websocket_service.dart';
import 'screens/overlay_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Configure window for overlay mode (Linux)
  try {
    await windowManager.ensureInitialized();
    
    WindowOptions windowOptions = const WindowOptions(
      size: Size(400, 300),
      center: true,
      backgroundColor: Colors.transparent,
      skipTaskbar: false,
      alwaysOnTop: true,
      titleBarStyle: TitleBarStyle.hidden,
    );
    
    windowManager.waitUntilReadyToShow(windowOptions, () async {
      await windowManager.show();
      await windowManager.focus();
    });
  } catch (e) {
    // Window manager not available (testing/development)
    debugPrint('Window manager not available: $e');
  }
  
  runApp(const NuxAIOverlayApp());
}

class NuxAIOverlayApp extends StatelessWidget {
  const NuxAIOverlayApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => WebSocketService(),
      child: MaterialApp(
        title: 'NuxAI Overlay',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          brightness: Brightness.dark,
          colorScheme: ColorScheme.dark(
            primary: Colors.blue[400]!,
            secondary: Colors.purple[400]!,
            surface: Colors.grey[900]!,
          ),
        ),
        home: const OverlayScreen(),
      ),
    );
  }
}

