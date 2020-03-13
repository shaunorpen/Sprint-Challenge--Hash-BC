import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

proofs = {}

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here

    last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()

    while True:
        hash = hashlib.sha256(str(proof).encode()).hexdigest()
        print(len(proofs))
        if hash in proofs:
            print("Proof found: " + str(proofs[hash]) + " in " + str(timer() - start))
            return proofs[hash]
        elif valid_proof(last_hash, proof) is True:
            print("Proof found: " + str(proof) + " in " + str(timer() - start))
            return proof
        else:
            proofs[hash] = proof
            proof += 1


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    must_match = str(last_hash)[-6:]
    potential_match = hashlib.sha256(str(proof).encode()).hexdigest()[:6]
    return must_match == potential_match

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    # f = open("my_id.txt", "r")
    # id = f.read()
    id = 'shaun-orpen'
    print("ID is", id)
    # f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
