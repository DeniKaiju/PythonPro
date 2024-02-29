import time
import requests
import os
import threading
import multiprocessing
from pathlib import Path
from typing import Dict, List


def encrypt_file(path: Path, result_dict: Dict[str, float]):
    start_time = time.time()
    print(f"Processing file from {path} in process {os.getpid()}")
    _ = [i for i in range(100_000_000)]
    end_time = time.time()
    encryption_time = end_time - start_time
    result_dict["encryption_time"] = encryption_time


# I/O-bound task (downloading image from URL)
def download_image(image_url: str, result_dict: Dict[str, float]):
    start_time = time.time()
    print(f"Downloading image from {image_url} in process {os.getpid()}")
    response = requests.get(image_url)
    with open("image.jpg", "wb") as f:
        f.write(response.content)
    end_time = time.time()
    download_time = end_time - start_time
    result_dict["download_time"] = download_time


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    result_dict = manager.dict()

    processes: List[multiprocessing.Process] = []
    threads: List[threading.Thread] = []

    p1 = multiprocessing.Process(
        target=encrypt_file, args=(Path("rockyou.txt"), result_dict)
    )
    p2 = threading.Thread(
        target=download_image,
        args=("https://picsum.photos/1000/1000", result_dict),
    )

    start_total_time = time.time()

    p1.start()
    p2.start()

    processes.append(p1)
    threads.append(p2)

    for process in processes:
        process.join()

    for thread in threads:
        thread.join()

    end_total_time = time.time()
    total_time = end_total_time - start_total_time

    encryption_time = result_dict.get("encryption_time", 0)
    download_time = result_dict.get("download_time", 0)

    print(
        f"Time taken for encryption task: {encryption_time:.2f}, "
        f"I/O-bound task: {download_time:.2f}, Total: {total_time:.2f} seconds"
    )
    