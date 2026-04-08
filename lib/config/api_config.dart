class ApiConfig {
  ApiConfig._();

  static const String _defaultHost = String.fromEnvironment(
    'ECORUTA_API_HOST',
    defaultValue: '192.168.44.88',
  );

  static const String _authPort = String.fromEnvironment(
    'ECORUTA_AUTH_PORT',
    defaultValue: '3000',
  );

  static const String _iaPort = String.fromEnvironment(
    'ECORUTA_IA_PORT',
    defaultValue: '8000',
  );

  static String get host => _defaultHost;

  static String get authBaseUrl => 'http://$host:$_authPort';

  static String get iaBaseUrl => 'http://$host:$_iaPort';
}
