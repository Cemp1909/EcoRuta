import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:geolocator/geolocator.dart';

class MapaScreen extends StatefulWidget {
  const MapaScreen({super.key});

  @override
  State<MapaScreen> createState() => _MapaScreenState();
}

class _MapaScreenState extends State<MapaScreen> {
  final MapController _mapController = MapController();

  final LatLng _villavicencio = const LatLng(4.1420, -73.6266);
  LatLng? _miUbicacion;
  bool _cargandoUbicacion = true;

  @override
  void initState() {
    super.initState();
    _obtenerUbicacion();
  }

  Future<void> _obtenerUbicacion() async {
    try {
      bool servicioActivo = await Geolocator.isLocationServiceEnabled();
      if (!servicioActivo) {
        setState(() => _cargandoUbicacion = false);
        return;
      }

      LocationPermission permiso = await Geolocator.checkPermission();

      if (permiso == LocationPermission.denied) {
        permiso = await Geolocator.requestPermission();
      }

      if (permiso == LocationPermission.denied ||
          permiso == LocationPermission.deniedForever) {
        setState(() => _cargandoUbicacion = false);
        return;
      }

      final posicion = await Geolocator.getCurrentPosition();

      if (!mounted) return;

      setState(() {
        _miUbicacion = LatLng(posicion.latitude, posicion.longitude);
        _cargandoUbicacion = false;
      });

      _mapController.move(_miUbicacion!, 15);
    } catch (e) {
      if (!mounted) return;
      setState(() => _cargandoUbicacion = false);
    }
  }

  void _irAVillavicencio() {
    _mapController.move(_villavicencio, 13);
  }

  void _irAMiUbicacion() {
    if (_miUbicacion != null) {
      _mapController.move(_miUbicacion!, 15);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mapa de reciclaje'),
        backgroundColor: const Color(0xFF1A3A2A),
      ),
      body: Stack(
        children: [
          FlutterMap(
            mapController: _mapController,
            options: const MapOptions(
              initialCenter: LatLng(4.1420, -73.6266),
              initialZoom: 13,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.ecoruta_temp',
              ),
              MarkerLayer(
                markers: [
                  Marker(
                    point: _villavicencio,
                    width: 80,
                    height: 80,
                    child: const Icon(
                      Icons.location_city,
                      size: 40,
                      color: Colors.red,
                    ),
                  ),
                  if (_miUbicacion != null)
                    Marker(
                      point: _miUbicacion!,
                      width: 80,
                      height: 80,
                      child: const Icon(
                        Icons.my_location,
                        size: 38,
                        color: Colors.blue,
                      ),
                    ),
                ],
              ),
            ],
          ),
          if (_cargandoUbicacion)
            const Positioned(
              top: 16,
              left: 16,
              right: 16,
              child: Card(
                color: Color(0xDD1A3A2A),
                child: Padding(
                  padding: EdgeInsets.all(12),
                  child: Text(
                    'Obteniendo ubicación...',
                    style: TextStyle(color: Colors.white),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            heroTag: 'villavo',
            backgroundColor: const Color(0xFF2E7D32),
            onPressed: _irAVillavicencio,
            child: const Icon(Icons.location_city),
          ),
          const SizedBox(height: 12),
          FloatingActionButton(
            heroTag: 'miposicion',
            backgroundColor: const Color(0xFF1565C0),
            onPressed: _irAMiUbicacion,
            child: const Icon(Icons.my_location),
          ),
        ],
      ),
    );
  }
}