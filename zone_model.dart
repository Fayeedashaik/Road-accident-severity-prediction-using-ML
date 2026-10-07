import 'package:google_maps_flutter/google_maps_flutter.dart';

enum RiskLevel {
  high,
  medium,
  low,
}

class ZoneModel {
  const ZoneModel({
    required this.id,
    required this.name,
    required this.latitude,
    required this.longitude,
    required this.riskLevel,
  });

  final String id;
  final String name;
  final double latitude;
  final double longitude;
  final RiskLevel riskLevel;

  LatLng get latLng => LatLng(latitude, longitude);

  bool get isHighRisk => riskLevel == RiskLevel.high;

  factory ZoneModel.fromJson(Map<String, dynamic> json) {
    return ZoneModel(
      id: json['id'] as String,
      name: json['name'] as String? ?? 'Unknown Zone',
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      riskLevel: _parseRiskLevel(json['riskLevel'] as String?),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'name': name,
      'latitude': latitude,
      'longitude': longitude,
      'riskLevel': riskLevel.name,
    };
  }

  static RiskLevel _parseRiskLevel(String? riskLevel) {
    switch ((riskLevel ?? '').toLowerCase()) {
      case 'high':
        return RiskLevel.high;
      case 'medium':
        return RiskLevel.medium;
      case 'low':
      default:
        return RiskLevel.low;
    }
  }
}
