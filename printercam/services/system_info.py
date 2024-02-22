import socket
import psutil
import cv2
import os


def get_main_disk_space():
    main_partition = os.path.abspath(os.sep)
    partition_info = psutil.disk_usage(main_partition)

    total_space_gb = partition_info.total / (1024 ** 3)  # Convert to gigabytes
    available_space_gb = partition_info.free / (1024 ** 3)  # Convert to gigabytes
    used_space_gb = (partition_info.total - partition_info.free) / (1024 ** 3)  # Convert to gigabytes

    result = f"{used_space_gb:.2f} GB of {total_space_gb:.2f} GB ({available_space_gb:.2f} GB left)"
    percentage_used = used_space_gb * 100 / total_space_gb
    disk = {"result": result, "percentage_used": percentage_used}
    return disk


def get_host_name():
    return socket.gethostname()


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


def get_available_webcams():
    available_webcams = []

    # Iterate through camera indices until no more cameras are found
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        cap.release()
        available_webcams.append(index)
        index += 1

    return available_webcams
