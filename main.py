import bluetooth
import requests

def discover_bluetooth_devices():
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    return devices

def send_bluetooth_message(device_address, message):
    service_uuid = "00001101-0000-1000-8000-00805F9B34FB"  # UUID do serviço Serial Port Profile (SPP)

    try:
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((device_address, 1))
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

def main():
    print("Selecione o método de envio:")
    print("1. Bluetooth")
    print("2. Wi-Fi")
    choice = input("Escolha uma opção: ")

    if choice == "1":
        devices = discover_bluetooth_devices()
        if devices:
            print("Dispositivos Bluetooth encontrados:")
            for i, (device_address, device_name) in enumerate(devices):
                print(f"{i+1}. {device_name} ({device_address})")

            device_choice = int(input("Escolha um dispositivo: "))
            if device_choice > 0 and device_choice <= len(devices):
                device_address = devices[device_choice-1][0]
                message = input("Digite a mensagem a ser enviada: ")
                send_bluetooth_message(device_address, message)
            else:
                print("Opção inválida.")
        else:
            print("Nenhum dispositivo Bluetooth encontrado.")
    elif choice == "2":
        device_ip = input("Digite o endereço IP do dispositivo na rede local: ")
        message = input("Digite a mensagem a ser enviada: ")
        send_wifi_message(device_ip, message)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
