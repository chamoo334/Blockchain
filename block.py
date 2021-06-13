from flask import Flask, jsonify
import datetime, json, hashlib


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.genesis(proof=1, prev_hash='0')

    def self.genesis(self, proof, prev_hash):
        block = {}
