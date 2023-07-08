import bluetooth
import requests
import uuid

def discover_bluetooth_devices():
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    return devices

def send_bluetooth_message(device_address, message, service_uuid):
    try:
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((device_address, 1, bluetooth.CIPHER_NONE, service_uuid))
        socket.send(message)
        socket.close()
        print("Mensagem enviada com sucesso!")
    except bluetooth.btcommon.BluetoothError as e:
        print(f"Erro ao enviar mensagem via Bluetooth: {e}")

def send_wifi_message(device_ip, message):
    url = f"http://{device_ip}/endpoint"  # Substitua 'endpoint' pelo endpoint adequado do dispositivo
    data = {'message': message}  # Crie um dicionário com os dados a serem enviados

    try:
        response = requests.post(url, json=data)  # Envia uma requisição POST com os dados em formato JSON
        if response.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Erro ao enviar mensagem. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")

def send_message_to_all_devices(devices, message, service_uuid):
    for device_address, _ in devices:
        send_bluetooth_message(device_address, message, service_uuid)

def main():
    service_uuid = str(uuid.uuid4())

    print("Selecione o método de envio:")
    print("1. Bluetooth")
    print("2. Wi-Fi")
    print("3. Ambos (Bluetooth e Wi-Fi)")
    choice = input("Escolha uma opção: ")

    if choice == "1":
        devices = discover_bluetooth_devices()
        if devices:
            print("Dispositivos Bluetooth encontrados:")
            for i, (device_address, device_name) in enumerate(devices):
                print(f"{i+1}. {device_name} ({device_address})")

            device_choice = int(input("Escolha um dispositivo (ou 0 para enviar para todos): "))
            if device_choice == 0:
                message = input("Digite a mensagem a ser enviada: ")
                send_message_to_all_devices(devices, message, service_uuid)
            elif device_choice > 0 and device_choice <= len(devices):
                device_address = devices[device_choice-1][0]
                message = input("Digite a mensagem a ser enviada: ")
                send_bluetooth_message(device_address, message, service_uuid)
            else:
                print("Opção inválida.")
        else:
            print("Nenhum dispositivo Bluetooth encontrado.")
    elif choice == "2":
        device_ip = input("Digite o endereço IP do dispositivo na rede local: ")
        message = input("Digite a mensagem a ser enviada: ")
        send_wifi_message(device_ip, message)
    elif choice == "3":
        devices = discover_bluetooth_devices()
        if devices:
            message = input("Digite a mensagem a ser enviada: ")
            send_message_to_all_devices(devices, message, service_uuid)
        else:
            print("Nenhum dispositivo Bluetooth encontrado.")
        device_ip = input("Digite o endereço IP do dispositivo na rede local: ")
        message = input("Digite a mensagem a ser enviada: ")
        send_wifi_message(device_ip, message)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
