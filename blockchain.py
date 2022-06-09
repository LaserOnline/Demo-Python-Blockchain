from crypt import methods
import datetime
import json
import hashlib
from urllib import response
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        # * เก็บกลุ่มของ block
        self.chain = []  # * list ของ Block
        self.transactions = 0
        # * Genesis Block
        self.create_block(nonce=1, previous_hash="0")
        # * Block ที่สร้างขึ้นมา

    def proof_of_work(self, previous_nonce):
        # * อยากได้ ค่า Nonceที่ส่งผลให้ได้target hash ---> 4 หลักแรก --> 0000xxxxxxxxxxx
        new_nonce = 1  # * ค่า Nonce ที่ต้องการ
        check_proof = False  # * ตรวจสอบค่า Nonce ให้ได้ ตาม target ที่กำหนด

        # * แก้โจทย์ของ Proof of Work โจทย์ทางคณิตศาสตร์
        while check_proof is False:
            # * เลขฐาน 16 หนึ่งชุด
            hashoperation = hashlib.sha256(
                str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

# * -------------------------------------------------------------------------------------------------------------------

    def create_block(self, nonce, previous_hash):
        # * เก็บส่วนประกอบของ Block แต่ละ Block
        block = {
            # * 1 หมายเลข Block
            "index": len(self.chain) + 1,
            # * 2 วันที่ทำการสร้าง Block
            "timestamp": str(datetime.datetime.now()),
            # * 3 ค่า Nonce
            "nonce": nonce,
            "data": self.transactions,
            # * 4 ค่า Hash ของ Block ก่อนหน้า
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

# * -------------------------------------------------------------------------------------------------------------------

        # * ให้บริการเกี่ยวกับ Block ก่อนหน้านี้
    def get_previous_block(self):
        return self.chain[-1]

    # * การเข้า รหัสข้อมูล
    def hash(self, block):
        # * แปลง Python Object (dict) เป็น JSON Object
        encode_block = json.dumps(block, sort_keys=True).encode()
        # * Sha-256 ของข้อมูลที่เข้ารหัส
        return hashlib.sha256(encode_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]  # * nonce ของ block ที่ตรวจสอบ
            hashoperation = hashlib.sha256(

                str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] != "0000":
                return False
            previous_block = block_index
            block_index += 1
        return True


# * -------------------------------------------------------------------------------------------------------------------
# * ใช้งาน Blockchain
blockchain = Blockchain()

# * เข้ารหัส Block
# * print(blockchain.hash(blockchain.chain[0]))

# * เว็บ Server

app = Flask(__name__)

# * routing


@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mining', methods=["GET"])
def mining_block():
    amount = 100000
    blockchain.transactions = blockchain.transactions+amount
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    nonce = blockchain.proof_of_work(previous_nonce)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        "message": "Mining Block Success",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "data": block["data"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            "message": "Blockchain is valid"
        }
    else:
        response = {
            "message": "Blockchain is not valid"
        }
    return jsonify(response), 200

    # * run server
if __name__ == '__main__':
    app.run()
