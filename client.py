import threading
import time
import numpy as np
import deepgnn.graph_engine.snark.distributed as distributed
class Load(threading.Thread):
    def run(self, *args, **kwargs):
        servers = ["10.1.0.4:50051", "10.1.0.4:50052", "10.1.0.4:50053", "10.1.0.4:50054", "10.1.0.4:50055", "10.1.0.4:50056"]
        graph = distributed.Client(servers)
        print(f"Created client, connected to servers")
        while True:
            node_ids = np.random.randint(0, 152410, 1000, dtype=np.int64)
            nbs_1hop  = graph.sample_neighbors(nodes=node_ids, edge_types=np.array([0], np.int32), count=10)[0]
            nbs_2hop  = graph.sample_neighbors(nodes=nbs_1hop.flatten(), edge_types=np.array([0], np.int32), count=10)[0]
            all_nodes = np.concatenate((node_ids, nbs_1hop.flatten(), nbs_2hop.flatten()))
            f = graph.node_features(nodes=all_nodes, features=np.array([[0, 300], [1, 50]], dtype=np.int32), feature_type=np.float32)
            print(f"Got features: {f.sum()}")
            assert f.sum() > 0
            time.sleep(0.1)

l = Load()
l.start()