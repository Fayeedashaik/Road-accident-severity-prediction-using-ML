import 'dart:convert';
import 'dart:math' as math;

import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:google_polyline_algorithm/google_polyline_algorithm.dart';
import 'package:http/http.dart' as http;

import '../models/zone_model.dart';

class DirectionsService {
  static const String _directionsApiKey = 'YOUR_GOOGLE_DIRECTIONS_API_KEY';

  Future<List<LatLng>> getSaferRoute({
    required LatLng origin,
    required LatLng destination,
    required List<ZoneModel> zones,
  }) async {
    final List<LatLng> detourWaypoints = _buildAvoidanceWaypoints(
      origin: origin,
      destination: destination,
      zones: zones.where((ZoneModel zone) => zone.isHighRisk).toList(),
    );

    final String waypoints = detourWaypoints.isEmpty
        ? ''
        : '&waypoints=${Uri.encodeComponent(detourWaypoints
            .map((LatLng point) => '${point.latitude},${point.longitude}')
            .join('|'))}';

    final Uri uri = Uri.parse(
      'https://maps.googleapis.com/maps/api/directions/json'
      '?origin=${origin.latitude},${origin.longitude}'
      '&destination=${destination.latitude},${destination.longitude}'
      '$waypoints'
      '&mode=driving'
      '&key=$_directionsApiKey',
    );

    final http.Response response = await http.get(uri);
    if (response.statusCode != 200) {
      throw Exception('Directions API failed with ${response.statusCode}.');
    }

    final Map<String, dynamic> payload =
        jsonDecode(response.body) as Map<String, dynamic>;
    final List<dynamic> routes = payload['routes'] as List<dynamic>;
    if (routes.isEmpty) {
      throw Exception('No route returned by Directions API.');
    }

    final String encoded =
        (routes.first as Map<String, dynamic>)['overview_polyline']['points']
            as String;

    final List<List<num>> decoded = decodePolyline(encoded);
    return decoded
        .map((List<num> point) => LatLng(
              point[0].toDouble(),
              point[1].toDouble(),
            ))
        .toList();
  }

  List<LatLng> _buildAvoidanceWaypoints({
    required LatLng origin,
    required LatLng destination,
    required List<ZoneModel> zones,
  }) {
    final List<LatLng> waypoints = <LatLng>[];

    for (final ZoneModel zone in zones) {
      final double distanceFromOrigin =
          _distanceMeters(origin, zone.latLng);
      final double distanceToDestination =
          _distanceMeters(destination, zone.latLng);

      if (distanceFromOrigin < 8000 && distanceToDestination < 8000) {
        final LatLng offsetPoint = _offsetWaypoint(zone.latLng);
        waypoints.add(offsetPoint);
      }
    }

    return waypoints.take(3).toList();
  }

  LatLng _offsetWaypoint(LatLng point) {
    // Add a small offset to encourage the route to bypass the risk point.
    return LatLng(point.latitude + 0.008, point.longitude + 0.008);
  }

  double _distanceMeters(LatLng first, LatLng second) {
    const double earthRadius = 6371000;
    final double dLat = _toRadians(second.latitude - first.latitude);
    final double dLng = _toRadians(second.longitude - first.longitude);

    final double a = math.sin(dLat / 2) * math.sin(dLat / 2) +
        math.cos(_toRadians(first.latitude)) *
            math.cos(_toRadians(second.latitude)) *
            math.sin(dLng / 2) *
            math.sin(dLng / 2);
    final double c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    return earthRadius * c;
  }

  double _toRadians(double degree) => degree * math.pi / 180;
}
