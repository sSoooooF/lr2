import 'dart:convert';
import 'dart:io';
import 'package:intl/intl.dart';

void main() async {
  final socket = await Socket.connect('127.0.0.1', 3000);
  print('Connected to ${socket.remoteAddress.address}:${socket.remotePort}');

  String studentInfo = "Нуриев Наиль Ниязович, М3О-411Б-21";

  logConnection('Connected to server');

  socket.write(studentInfo);
  print('Sent: $studentInfo');

  socket.cast<List<int>>().transform(utf8.decoder).listen((response) {
    print('Received: $response');

    logMessageReceived(response);

    socket.close();
  }, onDone: () {
    print('Server closed the connection');
  });
}

void logConnection(String message) {
  final now = DateTime.now();
  final formatter = DateFormat('yyyy-MM-dd HH:mm:ss');
  final formattedDate = formatter.format(now);

  File('client_log.txt')
      .writeAsStringSync('$formattedDate - $message\n', mode: FileMode.append);
}

void logMessageReceived(String message) {
  final now = DateTime.now();
  final formatter = DateFormat('yyyy-MM-dd HH:mm:ss');
  final formattedDate = formatter.format(now);

  File('client_log.txt').writeAsStringSync(
      '$formattedDate - Received message: $message\n',
      mode: FileMode.append,
      encoding: utf8);
}
