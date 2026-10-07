import 'dart:async';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../models/zone_model.dart';
import '../services/directions_service.dart';
import '../services/location_service.dart';
import '../services/notification_service.dart';
import '../services/zone_service.dart';
import 'alert_screen.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final LocationService _locationService = LocationService();
  final ZoneService _zoneService = ZoneService();
  final DirectionsService _directionsService = DirectionsService();

  final Set<Marker> _markers = <Marker>{};
  final Set<Polyline> _polylines = <Polyline>{};
  final Set<String> _alertedZoneIds = <String>{};

  GoogleMapController? _mapController;
  StreamSubscription<Position>? _positionSubscription;
  Position? _currentPosition;
  List<ZoneModel> _zones = <ZoneModel>[];
  bool _isLoading = true;
  bool _isRouting = false;

  static const LatLng _defaultDestination = LatLng(12.9352, 77.6245);

  @override
  void initState() {
    super.initState();
    _initializeScreen();
  }

  @override
  void dispose() {
    _positionSubscription?.cancel();
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _initializeScreen() async {
    try {
      await _locationService.ensureLocationPermission();
      final Position currentPosition = await _locationService.getCurrentPosition();
      final List<ZoneModel> zones = await _zoneService.fetchZones();

      if (!mounted) {
        return;
      }

      setState(() {
        _currentPosition = currentPosition;
        _zones = zones;
        _markers
          ..clear()
          ..addAll(_buildZoneMarkers(zones))
          ..add(_buildUserMarker(currentPosition));
        _isLoading = false;
      });

      await _drawSafeRoute();
      _startTracking();
    } catch (error) {
      if (!mounted) {
        return;
      }

      setState(() {
        _isLoading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Initialization failed: $error')),
      );
    }
  }

  void _startTracking() {
    _positionSubscription?.cancel();
    _positionSubscription = _locationService.getPositionStream().listen((
      Position position,
    ) async {
      if (!mounted) {
        return;
      }

      setState(() {
        _currentPosition = position;
        _markers.removeWhere((Marker marker) => marker.markerId.value == 'user');
        _markers.add(_buildUserMarker(position));
      });

      _animateTo(position);
      await _checkDangerZones(position);
    });
  }

  Set<Marker> _buildZoneMarkers(List<ZoneModel> zones) {
    return zones.map((ZoneModel zone) {
      return Marker(
        markerId: MarkerId(zone.id),
        position: zone.latLng,
        infoWindow: InfoWindow(
          title: zone.name,
          snippet: 'Risk: ${zone.riskLevel.name.toUpperCase()}',
        ),
        icon: BitmapDescriptor.defaultMarkerWithHue(_markerHue(zone.riskLevel)),
      );
    }).toSet();
  }

  Marker _buildUserMarker(Position position) {
    return Marker(
      markerId: const MarkerId('user'),
      position: LatLng(position.latitude, position.longitude),
      infoWindow: const InfoWindow(title: 'Your Location'),
      icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueAzure),
    );
  }

  double _markerHue(RiskLevel riskLevel) {
    switch (riskLevel) {
      case RiskLevel.high:
        return BitmapDescriptor.hueRed;
      case RiskLevel.medium:
        return BitmapDescriptor.hueYellow;
      case RiskLevel.low:
        return BitmapDescriptor.hueGreen;
    }
  }

  Future<void> _checkDangerZones(Position position) async {
    for (final ZoneModel zone in _zones.where((ZoneModel z) => z.isHighRisk)) {
      final double distance = Geolocator.distanceBetween(
        position.latitude,
        position.longitude,
        zone.latitude,
        zone.longitude,
      );

      if (distance <= 500 && !_alertedZoneIds.contains(zone.id)) {
        _alertedZoneIds.add(zone.id);

        await NotificationService.instance.showDangerNotification(
          title: 'Danger Zone Ahead',
          body:
              'You are near ${zone.name}. Slow down and drive carefully.',
        );

        if (mounted) {
          await showDialog<void>(
            context: context,
            builder: (BuildContext context) {
              return AlertScreen(
                zoneName: zone.name,
                distanceMeters: distance,
              );
            },
          );
        }
      } else if (distance > 650) {
        _alertedZoneIds.remove(zone.id);
      }
    }
  }

  Future<void> _drawSafeRoute() async {
    if (_currentPosition == null) {
      return;
    }

    setState(() {
      _isRouting = true;
    });

    try {
      final List<LatLng> route = await _directionsService.getSaferRoute(
        origin: LatLng(
          _currentPosition!.latitude,
          _currentPosition!.longitude,
        ),
        destination: _defaultDestination,
        zones: _zones,
      );

      if (!mounted) {
        return;
      }

      setState(() {
        _polylines
          ..clear()
          ..add(
            Polyline(
              polylineId: const PolylineId('safe_route'),
              points: route,
              color: Colors.blue,
              width: 5,
            ),
          );
      });
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Route generation failed: $error')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isRouting = false;
        });
      }
    }
  }

  Future<void> _animateTo(Position position) async {
    await _mapController?.animateCamera(
      CameraUpdate.newLatLng(
        LatLng(position.latitude, position.longitude),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final Position? currentPosition = _currentPosition;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Road Accident Danger Zone Alert'),
      ),
      body: _isLoading || currentPosition == null
          ? const Center(child: CircularProgressIndicator())
          : Stack(
              children: <Widget>[
                GoogleMap(
                  initialCameraPosition: CameraPosition(
                    target: LatLng(
                      currentPosition.latitude,
                      currentPosition.longitude,
                    ),
                    zoom: 14,
                  ),
                  myLocationEnabled: true,
                  myLocationButtonEnabled: true,
                  zoomControlsEnabled: false,
                  markers: _markers,
                  polylines: _polylines,
                  onMapCreated: (GoogleMapController controller) {
                    _mapController = controller;
                  },
                ),
                Positioned(
                  left: 16,
                  right: 16,
                  bottom: 16,
                  child: Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          Text(
                            'Current destination: Safer preset route',
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Markers: red = high, yellow = medium, green = low',
                          ),
                          const SizedBox(height: 12),
                          Row(
                            children: <Widget>[
                              Expanded(
                                child: OutlinedButton(
                                  onPressed: _isRouting ? null : _drawSafeRoute,
                                  child: Text(
                                    _isRouting
                                        ? 'Generating route...'
                                        : 'Refresh Safe Route',
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
    );
  }
}
