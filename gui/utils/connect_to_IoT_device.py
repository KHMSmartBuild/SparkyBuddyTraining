from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem

class IotDeviceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("IoT Device Connection")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.devices_list = QListWidget()
        self.add_demo_devices()  # Add demo devices to the list

        layout.addWidget(self.devices_list)

        button_layout = QHBoxLayout()

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_device)
        button_layout.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_device)
        button_layout.addWidget(self.disconnect_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_demo_devices(self):
        device_1 = QListWidgetItem("IoT Device 1")
        self.devices_list.addItem(device_1)

        device_2 = QListWidgetItem("IoT Device 2")
        self.devices_list.addItem(device_2)

    def connect_device(self):
        current_item = self.devices_list.currentItem()
        if current_item:
            print(f"Connecting to {current_item.text()}...")

            # Add your IoT device connection logic here
            # You can use Sparky or other means to establish the connection

            print(f"Connected to {current_item.text()}")

    def disconnect_device(self):
        current_item = self.devices_list.currentItem()
        if current_item:
            print(f"Disconnecting from {current_item.text()}...")

            # Add your IoT device disconnection logic here
            # You can use Sparky or other means to disconnect from the device

            print(f"Disconnected from {current_item.text()}")
