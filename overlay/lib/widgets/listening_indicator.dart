import 'package:flutter/material.dart';
import '../models/overlay_state.dart';

class ListeningIndicator extends StatefulWidget {
  final OverlayStateType state;

  const ListeningIndicator({
    super.key,
    required this.state,
  });

  @override
  State<ListeningIndicator> createState() => _ListeningIndicatorState();
}

class _ListeningIndicatorState extends State<ListeningIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);
    
    _animation = Tween<double>(begin: 0.5, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isActive = widget.state == OverlayStateType.listening ||
        widget.state == OverlayStateType.processing;

    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: _getColor().withOpacity(isActive ? _animation.value * 0.3 : 0.1),
            border: Border.all(
              color: _getColor(),
              width: 3,
            ),
          ),
          child: Center(
            child: Icon(
              _getIcon(),
              size: 40,
              color: _getColor(),
            ),
          ),
        );
      },
    );
  }

  Color _getColor() {
    switch (widget.state) {
      case OverlayStateType.listening:
        return Colors.blue[400]!;
      case OverlayStateType.processing:
        return Colors.purple[400]!;
      case OverlayStateType.responding:
        return Colors.green[400]!;
      case OverlayStateType.error:
        return Colors.red[400]!;
      default:
        return Colors.grey[600]!;
    }
  }

  IconData _getIcon() {
    switch (widget.state) {
      case OverlayStateType.listening:
        return Icons.mic;
      case OverlayStateType.processing:
        return Icons.psychology;
      case OverlayStateType.responding:
        return Icons.check_circle;
      case OverlayStateType.error:
        return Icons.error;
      default:
        return Icons.mic_none;
    }
  }
}

