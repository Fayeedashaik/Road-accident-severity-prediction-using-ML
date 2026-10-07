import 'package:flutter/material.dart';

class AlertScreen extends StatelessWidget {
  const AlertScreen({
    super.key,
    required this.zoneName,
    required this.distanceMeters,
  });

  final String zoneName;
  final double distanceMeters;

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Danger Zone Ahead'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text('High-risk zone: $zoneName'),
          const SizedBox(height: 8),
          Text(
            'You are ${distanceMeters.toStringAsFixed(0)} meters away. '
            'Drive carefully and reduce speed.',
          ),
        ],
      ),
      actions: <Widget>[
        FilledButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('OK'),
        ),
      ],
    );
  }
}
