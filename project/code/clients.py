import boto3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import random 

clickWeight = [6 , 3 , 1]     # the weight of each position to click

purchaseA = [4 , 6]             # 40% chance to buy and 60% not to buy

purchaseB0 = [2 , 8]            # 20% chance to buy from advertiser0 and 80% not to buy

purchaseB1 = [4 , 6]          # 45% chance to buy from advertiser1 and 55% not to buy

purchaseB2 = [7 , 3]          # 65% chance to buy from advertiser2 and 35% not to buy

clients = []

round = 1

class client:

    def __init__(self , id):
        print('client init')
        self.id = id
    

class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/clients':
            # Insert your code here
            print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_headers()
        # self.send_response(200)

    def do_POST(self):
        if self.path == '/clients':
            # Insert your code here
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            global round
            if round == 11:
                return
            print('ROUND {}'.format(round))
            print('body of message = ' , json.loads(post_data.decode('utf-8')))
            self._set_headers()
            play(json.loads(post_data.decode('utf-8'))['Message'])
            round += 1
        # self.send_response(200)

def play(message):
    messageDict = json.loads(message)   # key = id , value=[round , clicks , buy , bid]
    print("messageDict: " , messageDict)
    # ----------------------- PHASE A ------------------------------------
    # --------------------------------------------------------------------
    # for client in clients:
    #     # decide which i am gona click
    #     idsOrder = list(messageDict)        # descending order ids according bid
    #     clickChooseId = random.choices(idsOrder , clickWeight)
    #     if messageDict[clickChooseId[0]][1] == -1:
    #         messageDict[clickChooseId[0]][1] = messageDict[clickChooseId[0]][1]+2
    #     else:
    #         messageDict[clickChooseId[0]][1] = messageDict[clickChooseId[0]][1]+1

    #     #dicede if i am gona buy the item
    #     buy = [clickChooseId[0] , -1]
    #     isBought = random.choices(buy , purchaseA)
    #     if(isBought[0] == clickChooseId[0]):    # the client bought the item
    #         if messageDict[clickChooseId[0]][2] == -1:
    #             messageDict[clickChooseId[0]][2] = messageDict[clickChooseId[0]][2] + 2
    #         else:
    #             messageDict[clickChooseId[0]][2] = messageDict[clickChooseId[0]][2] + 1
    #         print('client {} click advertiser {} and buy it'.format(client.id , clickChooseId[0]))
    #     else:
    #         print('client {} click advertiser {} and dont buy it'.format(client.id , clickChooseId[0]))
    
    # ------------------ PHASE B -------------------------------------
    # ----------------------------------------------------------------
    for client in clients:
        # decide which i am gona click
        idsOrder = list(messageDict)        # descending order ids according bid
        clickChooseId = random.choices(idsOrder , weights=clickWeight)
        if messageDict[clickChooseId[0]][1] == -1:
            messageDict[clickChooseId[0]][1] = messageDict[clickChooseId[0]][1]+2
        else:
            messageDict[clickChooseId[0]][1] = messageDict[clickChooseId[0]][1]+1
        
        #dicede if i am gona buy the item
        buy = [clickChooseId[0] , -1]
        if(clickChooseId[0] == '0'):
            isBought = random.choices(buy , weights=purchaseB0)
        elif(clickChooseId[0] == '1'):
            isBought = random.choices(buy , weights=purchaseB1)
        else:
            isBought = random.choices(buy , weights=purchaseB2)

        if(isBought[0] == clickChooseId[0]):    # the client bought the item
            if messageDict[clickChooseId[0]][2] == -1:
                messageDict[clickChooseId[0]][2] = messageDict[clickChooseId[0]][2] + 2
            else:
                messageDict[clickChooseId[0]][2] = messageDict[clickChooseId[0]][2] + 1
            print("clientId {} choose to click the AdvertiserId: {} and buy it ".format(client.id , clickChooseId[0]))
        else:
            print("clientId {} choose to click the AdvertiserId: {} and dont buy it ".format(client.id , clickChooseId[0]))

    print("message dict after clicks and buys: " , messageDict)
    sqs = boto3.client('sqs')
    response = sqs.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/535490399091/Action',
                MessageBody= json.dumps(messageDict)
            )



def main():
    print('main')

    # init 10 clients
    for i in range(10):
        tmp = client(i)
        clients.append(tmp)

    # init SNS subscription
    httpd = HTTPServer(("", 8080), MyHandler)#socketserver.TCPServer(("", 8080), MyHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()