# This file is used to store database credentials
host="ec2-79-125-126-205.eu-west-1.compute.amazonaws.com"
database="d9eqc1kq3rl4pl"
user="hjarwfeiklyxyb"
password="4b2862371520d9d6dcd0419778ed66ebdc426dbffa5d7cc9a42c44113b51d719"
url="postgres://hjarwfeiklyxyb:4b2862371520d9d6dcd0419778ed66ebdc426dbffa5d7cc9a42c44113b51d719@ec2-79-125-126-205.eu-west-1.compute.amazonaws.com:5432/d9eqc1kq3rl4pl"

def connection():
    return host, database, user, password, url
