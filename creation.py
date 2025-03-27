import hashlib
import json
from time import time
from typing import List, Dict

class Blockchain:
    def __init__(self):
        # Initialize the blockchain with a genesis block
        self.chain: List[Dict] = []
        self.pending_transactions: List[Dict] = []
        
        # Create the genesis block
        self.create_block(previous_hash="0", proof=100)

    def create_block(self, proof: int, previous_hash: str = None) -> Dict:
       
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        # Reset pending transactions
        self.pending_transactions = []
        
        # Add block to the chain
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        
        self.pending_transactions.append(transaction)
        return len(self.chain) + 1

    @staticmethod
    def hash(block: Dict) -> str:
        """
        Create a SHA-256 hash of a block
        
        :param block: Block to hash
        :return: Hash of the block
        """
        # We must make sure the dictionary is ordered to get consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
       
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
       
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def main():
    # Create a blockchain instance
    blockchain = Blockchain()

    # Simulate some transactions
    blockchain.new_transaction(
        sender="SYSTEM", 
        recipient="Alice", 
        amount=50
    )

    # Mine a new block
    last_block = blockchain.chain[-1]
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Add the new block to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)

    # Print the blockchain
    print("Blockchain created successfully!")
    print("\nFull Blockchain:")
    for block in blockchain.chain:
        print(json.dumps(block, indent=2))

if __name__ == "__main__":
    main()
