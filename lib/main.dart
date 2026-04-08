import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const EcoRutaApp());
}

class EcoRutaApp extends StatelessWidget {
  const EcoRutaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EcoRuta',
      debugShowCheckedModeBanner: false,

      theme: ThemeData(
        useMaterial3: true,

        // 🔥 COLOR PRINCIPAL
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
          brightness: Brightness.dark,
        ),

        // 🔥 TIPOGRAFÍA GLOBAL
        fontFamily: 'Poppins',

        // 🔥 BOTONES
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green.shade600,
            foregroundColor: Colors.white,
            elevation: 5,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),

        // 🔥 INPUTS MÁS LIMPIOS
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white.withOpacity(0.08),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          labelStyle: const TextStyle(color: Colors.white70),
        ),
      ),

      builder: (context, child) {
        return ScrollConfiguration(
          behavior: ScrollConfiguration.of(context).copyWith(
            overscroll: false,
          ),
          child: child!,
        );
      },

      home: const LoginScreen(),
    );
  }
}