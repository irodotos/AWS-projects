import boto3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import matplotlib.pyplot as plt
from tkinter import * 
priceA = {  # key=advertisers id , value=price
    '0' : 12,
    '1' : 12,
    '2' : 12
}

priceB = {  # key=advertisers id , value=price
    '0' : 20, 
    '1' : 12, 
    '2' : 8  
}

bids = {  # key=advertisers id , value=[round , clicks , sales , bid]
    0 : [],
    1 : [],
    2 : []
}

advertisers = []
round = 1
adv0Profit = []
adv1Profit = []
adv2Profit = []
providerRev = []

class advertiser:

    def __init__(self , id):
        print('advertiser init')
        self.id = id

class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/advertisers':
            # Insert your code here
            print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_headers()
        # self.send_response(200)

    def do_POST(self):
        if self.path == '/advertisers':
            # Insert your code here
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            global round
            print('ROUND {}'.format(round))
            print('body of message = ' , json.loads(post_data.decode('utf-8')))
            self._set_headers()
            round += 1
            play(json.loads(post_data.decode('utf-8'))['Message'])
        # self.send_response(200)

def graphs():
    client = boto3.client('dynamodb')
    respone = client.scan(TableName='Actions')
    # print('repsonse = ' , respone)
    # print('type = ' , type(respone))
    items = respone['Items']
    newDict = {}
    for item in items:
        # print('item = ' , item)
        # print('type item = ' , type(item))
        newDict[item['id']['S']] = json.loads(item['value']['S'])
    
    print('newDict = ' , newDict)
    x = [1 ,2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10]
    adv0Bids = []
    adv1Bids = []
    adv2Bids =[]
    for i in range(1,11):
        adv0Bids.append(newDict[str(i)]['0'][3])
        adv1Bids.append(newDict[str(i)]['1'][3])
        adv2Bids.append(newDict[str(i)]['2'][3])
    print('adv0Bids = ' , adv0Bids)
    print('adv1Bids = ' , adv1Bids)
    print('adv2Bids = ' , adv2Bids)
    print('adv0Profit = ' , adv0Profit)
    print('adv1Profit = ' , adv1Profit)
    print('adv2Profit = ' , adv2Profit)
    print('providerRevenue = ' , providerRev)
    return

def play(message):
    messageDict = json.loads(message)   # key = id , value=[round , clicks , buy , bid]
    bids = messageDict
    print('bids = ' , bids)
    total_clicks = 0
    providerRevenue = 0
    for adv in advertisers:
        total_clicks += bids[adv.id][1]
    # -------------------- PHASE A -----------------------------------
    # ----------------------------------------------------------------
    # for adv in advertisers:
    #     clicks = bids[adv.id][1]
    #     if(clicks == -1):
    #         clicks=0
    #     sales = bids[adv.id][2]
    #     if(sales == -1):
    #         sales = 0
    #     rev = sales*priceA[adv.id]
    #     cost = bids[adv.id][3]*clicks
    #     profit = rev-cost
    #     providerRevenue += cost
    #     print("advertiser {}: revenue= {} , cost= {} , profit= {}".format(adv.id,rev,cost,profit))
    #     if(adv.id == '0'):
    #         adv0Profit.append(profit)
    #     elif(adv.id == '1'):
    #         adv1Profit.append(profit)
    #     elif(adv.id == '2'):
    #         adv2Profit.append(profit)
    #     if( sales > (clicks*40)/100 ):         # if my sales is more than 40% of my clicks bid more
    #         print('advertiser {} have high sales percentage according clicks. May need to increase bid'.format(adv.id))
    #         if(bids[adv.id][3] + priceA[adv.id]/4 < (priceA[adv.id]*60)/100):
    #             bids[adv.id][3] = bids[adv.id][3] + priceA[adv.id]/4
    #             print('advertiser {} increase its bid beacuse he have a lot sales'.format(adv.id))
    #         if ( clicks < (total_clicks*40)/100):                  # if my clicks are low but i already have high sale percentage => MORE BID
    #             if(bids[adv.id][3] + priceA[adv.id]/4 < (priceA[adv.id]*60)/100):
    #                 bids[adv.id][3] = bids[adv.id][3] +  priceA[adv.id]/4
    #                 print('advertiser {} increase its bid beacuse he have a lot sales and low clicks'.format(adv.id))
    #     elif( sales < (clicks*20)/100 ):        # if my sales are less than 20% of my clicks bid less
    #         print('avdertiser {} have low sales (if his bid is more than price/4+1 we will decrease it)'.format(adv.id))
    #         if( bids[adv.id][3] > priceA[adv.id]/4+1 ):
    #             bids[adv.id][3] = bids[adv.id][3] - priceA[adv.id]/4
    #             print('advertiser {} decrease its bid beacuse he have low sales'.format(adv.id))
    #         if(clicks > (total_clicks*40)/100):                     # if my clicks are high but i already have low sale percentage => LESS BID
    #             if( bids[adv.id][3] > priceA[adv.id]/4+1):
    #                 bids[adv.id][3] = bids[adv.id][3] - priceA[adv.id]/4
    #                 print('advertiser {} decrease its bid beacuse he have low salws and high clicks'.format(adv.id))
    #     else:
    #         print('advertiser {} didnt change his bid'.format(adv.id))
    #     bids[adv.id][0] = round
    #     bids[adv.id][1] = -1
    #     bids[adv.id][2] = -1

    # -------------------- PHASE B -----------------------------------
    # ----------------------------------------------------------------
    for adv in advertisers:
        clicks = bids[adv.id][1]
        if(clicks == -1):
            clicks=0
        sales = bids[adv.id][2]
        if(sales == -1):
            sales = 0
        rev = sales*priceB[adv.id]
        cost = bids[adv.id][3]*clicks
        providerRevenue += cost
        profit = rev-cost
        print("advertiser {}: revenue= {} , cost= {} , profit= {}".format(adv.id,rev,cost,profit))
        if(adv.id == '0'):
            adv0Profit.append(profit)
        elif(adv.id == '1'):
            adv1Profit.append(profit)
        elif(adv.id == '2'):
            adv2Profit.append(profit)
        
        if( sales > (clicks*40)/100 ):         # if my sales is more than 40% of my clicks bid more
            print('advertiser {} have high sales percentage according clicks. May need to increase bid'.format(adv.id))
            if(bids[adv.id][3] + priceB[adv.id]/4 < (priceB[adv.id]*60)/100):
                bids[adv.id][3] = bids[adv.id][3] + priceB[adv.id]/4
                print('advertiser {} increase its bid beacuse he have a lot sales'.format(adv.id))
            if ( clicks < (total_clicks*40)/100):                  # if my clicks are low but i already have high sale percentage => MORE BID
                if(bids[adv.id][3] + priceB[adv.id]/4 < (priceB[adv.id]*60)/100):
                    bids[adv.id][3] = bids[adv.id][3] +  priceB[adv.id]/4
                    print('advertiser {} increase its bid beacuse he have a lot sales and low clicks'.format(adv.id))
        elif( sales < (clicks*20)/100 ):        # if my sales are less than 20% of my clicks bid less
            print('avdertiser {} have low sales (if his bid is more than price/4+1 we will decrease it)'.format(adv.id))
            if( bids[adv.id][3] > priceB[adv.id]/4+1 ):
                bids[adv.id][3] = bids[adv.id][3] - priceB[adv.id]/4
                print('advertiser {} decrease its bid beacuse he have low sales'.format(adv.id))
            if(clicks > (total_clicks*40)/100):                     # if my clicks are high but i already have low sale percentage => LESS BID
                if( bids[adv.id][3] > priceB[adv.id]/4+1):
                    bids[adv.id][3] = bids[adv.id][3] - priceB[adv.id]/4
                    print('advertiser {} decrease its bid beacuse he have low salws and high clicks'.format(adv.id))
        else:
            print('advertiser {} didnt change his bid'.format(adv.id))
        bids[adv.id][0] = round
        bids[adv.id][1] = -1
        bids[adv.id][2] = -1

    if round == 11:
        graphs()
        return
    print('new bids = ' , bids)
    providerRev.append(providerRevenue)
    sqs = boto3.client('sqs')
    response = sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/535490399091/Bids',
            MessageBody= json.dumps(bids)
        )

def main():
    print('main')

    # init the 3 advertisers
    for i in range(3):
        tmp = advertiser(str(i))
        advertisers.append(tmp)
        rand = random.randint(1 , 5)   # RANDOM BID FROM 1 TO 5
        bids[i] = [1 , -1 , -1 , rand]
    
    sqs = boto3.client('sqs')
    response = sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/535490399091/Bids',
            MessageBody= json.dumps(bids)
        )
    
    httpd = HTTPServer(("", 8080), MyHandler)#socketserver.TCPServer(("", 8080), MyHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()