import hashlib
import time
import json
import os

BLOCKCHAIN_FILE = "blockchain_data.json"

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash_value=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash_value or self.calculate_hash()

    def calculate_hash(self):
        value = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(value.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_data):
        return Block(
            index=block_data["index"],
            timestamp=block_data["timestamp"],
            data=block_data["data"],
            previous_hash=block_data["previous_hash"],
            hash_value=block_data["hash"]
        )

class Blockchain:
    def __init__(self):
        self.chain = self.load_chain()

    def create_block(self, index, data):
        timestamp = time.time()
        previous_hash = self.chain[-1].hash if self.chain else "0"
        new_block = Block(index, timestamp, data, previous_hash)
        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def save_chain(self):
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=2)

    def load_chain(self):
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r") as f:
                blocks = json.load(f)
                return [Block.from_dict(b) for b in blocks]
        else:
            # Start with Genesis block
            return [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")
