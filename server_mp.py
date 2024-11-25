import socket
import threading
import time
import logging
import configparser

logging.basicConfig(filename='server_log_mp.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def handle_client(client_socket, client_address):
    logging.info(f'Client connected: {client_address}')
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:  # Если сообщение пустое, клиент отключился
                break

            logging.info(f'Received message: {message}')

            # Обработка данных (имитация задержки)
            response = f"{message[::-1]}. Сервер написан Нуриевым Н.Н.. М3О-411Б-21"
            client_socket.send(response.encode('utf-8'))
            logging.info(f'Sent message: {response}')
    except Exception as e:
        logging.error(f'Error with client {client_address}: {e}')
    finally:
        logging.info(f'Client disconnected: {client_address}')
        client_socket.close()

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    address = config.get('server', 'Address', fallback='127.0.0.1')
    port = config.getint('server', 'Port', fallback=3000)

    return address, port

def main():
    config_file = 'config.ini'
    address, port = load_config(config_file)

    logging.info(f'Server configuration: Address={address}, Port={port}')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, port))
    server.listen(5) 
    logging.info('Threaded server started and listening for connections')

    try:
        while True:
            logging.info('Waiting for a new connection...')
            client_socket, client_address = server.accept()
            logging.info(f'Accepted connection from {client_address}')
            
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        logging.info('Server shutting down')
    finally:
        server.close()

if __name__ == "__main__":
    main()