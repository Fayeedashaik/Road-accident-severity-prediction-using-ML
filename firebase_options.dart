import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

/// Replace these placeholder values by running `flutterfire configure`.
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError('Web is not configured for this sample.');
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return const FirebaseOptions(
          apiKey: 'YOUR_FIREBASE_API_KEY',
          appId: 'YOUR_FIREBASE_APP_ID',
          messagingSenderId: 'YOUR_FIREBASE_MESSAGING_SENDER_ID',
          projectId: 'YOUR_FIREBASE_PROJECT_ID',
          databaseURL: 'https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com',
          storageBucket: 'YOUR_FIREBASE_STORAGE_BUCKET',
        );
      case TargetPlatform.iOS:
        return const FirebaseOptions(
          apiKey: 'YOUR_FIREBASE_API_KEY',
          appId: 'YOUR_FIREBASE_APP_ID',
          messagingSenderId: 'YOUR_FIREBASE_MESSAGING_SENDER_ID',
          projectId: 'YOUR_FIREBASE_PROJECT_ID',
          databaseURL: 'https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com',
          iosBundleId: 'com.example.roadAccidentDangerZoneAlert',
          storageBucket: 'YOUR_FIREBASE_STORAGE_BUCKET',
        );
      default:
        throw UnsupportedError('This platform is not configured.');
    }
  }
}
