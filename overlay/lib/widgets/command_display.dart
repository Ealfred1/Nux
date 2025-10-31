import 'package:flutter/material.dart';

class CommandDisplay extends StatelessWidget {
  final String? command;
  final String? result;
  final String? response;

  const CommandDisplay({
    super.key,
    this.command,
    this.result,
    this.response,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        children: [
          if (command != null)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blue[900]!.withOpacity(0.3),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.keyboard_voice, size: 16, color: Colors.blue[300]),
                  const SizedBox(width: 8),
                  Flexible(
                    child: Text(
                      command!,
                      style: TextStyle(
                        color: Colors.blue[300],
                        fontSize: 14,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
            ),
          if (command != null && (result != null || response != null)) 
            const SizedBox(height: 8),
          if (response != null || result != null)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.green[900]!.withOpacity(0.3),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.check, size: 16, color: Colors.green[300]),
                  const SizedBox(width: 8),
                  Flexible(
                    child: Text(
                      response ?? result ?? '',
                      style: TextStyle(
                        color: Colors.green[300],
                        fontSize: 12,
                      ),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 2,
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

