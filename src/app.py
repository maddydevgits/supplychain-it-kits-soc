from flask import Flask,request,render_template,jsonify
from web3 import Web3,HTTPProvider
import json
import urllib3

blockchain='http://127.0.0.1:7545'

def connect():
    web3=Web3(HTTPProvider(blockchain))
    web3.eth.defaultAccount=web3.eth.accounts[0]

    artifact="../build/contracts/SupplyChain.json"
    with open(artifact) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    return contract,web3

app=Flask(__name__)

@app.route('/addProduct',methods=['GET','POST'])
def addProduct():
    # i,n
    id=request.args.get('id') # '123'
    id=int(id)
    name=request.args.get('name')
    contract,web3=connect()
    try:
        tx_hash=contract.functions.addProduct(id,name).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return 'transaction done'
    except:
        return 'transaction error'


@app.route('/addDistributor',methods=['GET','POST'])
def addDistributor():
    # i, address (d)
    id=request.args.get('id') 
    id=int(id)
    address=request.args.get('address')
    contract,web3=connect()
    tx_hash=contract.functions.addDistributor(id,address).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return 'Distribuor added'


@app.route('/addRetailer',methods=['GET','POST'])
def addRetailer():
    # i, address (r)
    id=request.args.get('id')
    id=int(id)
    address=request.args.get('address')
    contract,web3=connect()
    tx_hash=contract.functions.addRetailer(id,address).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return 'Retailer Added'

@app.route('/verifyProduct',methods=['GET','POST'])
def verifyProduct():
    # i
    id=request.args.get('id')
    id=int(id)
    contract,web3=connect()
    data=contract.functions.verifyProduct(id).call()
    return (jsonify(data))

@app.route('/',methods=['GET','POST'])
def addproductpage():
    return render_template('addproduct.html')

@app.route('/verifyproductpage',methods=['GET','POST'])
def verifyproductpage():
    return render_template('verifyproduct.html')

@app.route('/adddistributorpage',methods=['GET','POST'])
def adddistributorpage():
    return render_template('adddistributor.html')

@app.route('/addretailerpage',methods=['GET','POST'])
def addretailerpage():
    return render_template('addretailer.html')

@app.route('/addproductform',methods=['GET','POST'])
def addproductform():
    id=request.form['id']
    name=request.form['name']
    pipe=urllib3.PoolManager()
    response=pipe.request('get','http://127.0.0.1:4000/addProduct?id='+id+'&name='+name)
    response=response.data
    response=response.decode('utf-8')
    return render_template('addproduct.html',response=response)

@app.route('/verifyproductform',methods=['GET','POST'])
def verifyproductform():
    id=request.form['id']
    print(id)
    pipe=urllib3.PoolManager()
    response=pipe.request('get','http://127.0.0.1:4000/verifyProduct?id='+id)
    response=response.data
    response=response.decode('utf-8')
    return render_template('verifyproduct.html',response=response)

@app.route('/adddistributorform',methods=['GET','POST'])
def adddistributorform():
    id=request.form['id']
    address=request.form['address']
    pipe=urllib3.PoolManager()
    response=pipe.request('get','http://127.0.0.1:4000/addDistributor?id='+id+'&address='+address)
    response=response.data
    response=response.decode('utf-8')
    return render_template('adddistributor.html',response=response)

@app.route('/addretailerform',methods=['GET','POST'])
def addretailerform():
    id=request.form['id']
    address=request.form['address']
    pipe=urllib3.PoolManager()
    response=pipe.request('get','http://127.0.0.1:4000/addRetailer?id='+id+'&address='+address)
    response=response.data
    response=response.decode('utf-8')
    return render_template('addretailer.html',response=response)


if __name__=="__main__":
    app.run(
        host='0.0.0.0',
        port=4000
    )