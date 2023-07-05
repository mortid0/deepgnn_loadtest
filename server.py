import deepgnn.graph_engine.data.reddit as reddit
import deepgnn.graph_engine.snark.server as server
import os


def download_data(dir: str, num_partitions: int = 6):
    if os.path.exists(dir):
        print("Data already exists. Skipping download.")
        return 
    # use a separate function to unload Reddit graph from temp memory
    os.makedirs(dir, exist_ok=True)
    r = reddit.Reddit(output_dir=dir, num_partitions=num_partitions)

def start_servers(dir: str, addresses: list[str] = None, partitions: list[list[int]] = None):
    # start the servers
    assert len(addresses) == len(partitions)
    servers = []
    for i in range(len(addresses)):
        servers.append(server.Server(dir, partitions[i], addresses[i]))
        print(f"Started server {i} at {addresses[i]}")
    return servers

data_dir = "/tmp/reddit"
addresses = ["10.1.0.4:50051", "10.1.0.4:50052", "10.1.0.4:50053", "10.1.0.4:50054", "10.1.0.4:50055", "10.1.0.4:50056"]
partitions = [[0], [1], [2], [3], [4], [5]]
print("Downloading data...")
download_data(data_dir, len(addresses))
print("Starting servers...")
s = start_servers(data_dir, addresses, partitions)
input("Serving requests. Press Enter to stop and exit...")


