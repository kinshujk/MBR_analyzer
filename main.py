#!/usr/bin/python3

import sys
import os
import hashlib
import struct
from partitions import PARTITIONS 

BUFFER_SIZE = 65536

def main():
    if len(sys.argv) < 1:
        print("Try again with a filename")
        exit(1)

    fileName = sys.argv[1]
    
    check_hash(fileName)
    table = generateTable(fileName)
    printTable(table)

def check_hash(fileName):
    # Check the md5 and sha1 hashes of the file and write them to appropriately named files
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()   

    # Read the file using a buffer, don't overuse memory
    f = open(fileName, 'rb')
    while True:
        data = f.read(BUFFER_SIZE)
        if not data:
            break
        md5.update(data)
        sha1.update(data)
    
    md5_file = open(f"MD5-{fileName}.txt", "w")
    md5_file.write(md5.hexdigest())
    md5_file.close()

    sha1_file = open(f"SHA1-{fileName}.txt", "w")
    sha1_file.write(sha1.hexdigest())
    sha1_file.close()

class PartitionEntry:
    def __init__(self, data):
        self.type = bytes(data[4:5])
        self.lba = int.from_bytes(bytes(data[8:12]), "little")
        self.size = int.from_bytes(bytes(data[12:16]), "little")
        self.last8BytesStartAddr = self.last8addr(self.lba, self.size)
        self.last8BytesEndAddr = self.last8BytesStartAddr + 8
        self.last8Bytes = []
        
    def last8addr(self, lba, size):
        # Return the address of the 8th byte from the end of the partition (512 bytes in 1 sector * LBA + (512 - 8))
        addr = lba * 512 + 504
        return addr

def generateTable(fileName):
    # Read in the whole file and parse the partition entries
    mbr = open(fileName, 'rb').read()
    table = []
    
    for i in range(446, 510, 16):
        newEntry = PartitionEntry(mbr[i:i+16])

        # Populate the last8bytes list using the the starting address of the last 8 bytes
        for byte in mbr[newEntry.last8BytesStartAddr:newEntry.last8BytesEndAddr]:
            newEntry.last8Bytes.append(byte)
        
        table.append(newEntry)
    
    return table

def printTable(table):
    # Print the key of the partition type, the starting LBA address and the size of the partition all formatted to 10 digits
    for entry in table:
        key = '0x' + str(entry.type)[4:6]
        lba_addr_formatted = str(entry.lba).zfill(10)
        size_formatted = str(entry.size).zfill(10)
        print(f"({key[2:]}), {PARTITIONS[key]}, {lba_addr_formatted}, {size_formatted}")
    
    # Print the partition number and format the last 8 bytes of the boot record to display hex
    for number, entry in enumerate(table):
        print(f"Partition number: {number} ")
        print(f"Last 8 bytes of boot record: {' '.join([str(hex(x))[2:].zfill(2).upper() for x in entry.last8Bytes])}")

if __name__ == '__main__':
    main()