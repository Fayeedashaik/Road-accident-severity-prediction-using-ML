import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:firebase_database/firebase_database.dart';

import '../models/zone_model.dart';

class ZoneService {
  final FirebaseDatabase _database = FirebaseDatabase.instance;

  Future<List<ZoneModel>> fetchZones() async {
    try {
      final DatabaseEvent event = await _database.ref('zones').once();
      final Object? value = event.snapshot.value;

      if (value is Map<Object?, Object?> && value.isNotEmpty) {
        final List<ZoneModel> zones = value.values.map((Object? item) {
          final Map<String, dynamic> zoneMap =
              Map<String, dynamic>.from(item as Map);
          return ZoneModel.fromJson(zoneMap);
        }).toList();

        return zones;
      }
    } catch (_) {
      // Fall back to the bundled JSON asset if Firebase is unavailable.
    }

    final String jsonString = await rootBundle.loadString(
      'assets/data/accident_zones.json',
    );
    final List<dynamic> decoded = jsonDecode(jsonString) as List<dynamic>;
    return decoded
        .map((dynamic item) => ZoneModel.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
