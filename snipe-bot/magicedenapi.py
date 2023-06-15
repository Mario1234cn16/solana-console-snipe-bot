from dataclasses import replace
from time import time
from unittest import result
from base58 import b58encode, b58decode
import requests
import solana
from solana.rpc.api import Client
import solana.system_program as sp
from solana.account import Account
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
import time
from theblockchainapi import TheBlockchainAPIResource, \
    SolanaNetwork, SolanaCurrencyUnit, SolanaWallet, SolanaExchange

#solana


cli = Client("https://api-mainnet.magiceden.dev/v2")
RESOURCE = TheBlockchainAPIResource(
    api_key_id="",
    api_secret_key=""
)

network = SolanaNetwork.MAINNET_BETA
exchange = SolanaExchange.MAGIC_EDEN
#wallet

keypair_file = open("keypair.txt", "r")
encoded_keypair = str(keypair_file.readlines())
encoded_keypair = encoded_keypair.replace("[","")
encoded_keypair = encoded_keypair.replace("]","")
encoded_keypair = encoded_keypair.replace("'","")
keypair = b58decode(encoded_keypair)
private_key1 = keypair[:32]
public_key = keypair[32:]
wallet_address = b58encode(public_key).decode()
should_mint_bool = False
private_key_str = str(private_key1)
#bot

collection_id = input('Enter the collection ID that you want to snipe : ')
target_floor_price = input('Enter the floor price that you want to buy under (bot buys if the list price is under this value) : ')
number_of_mints = input('Enter the amount of mints that the bot should do : ')
number_of_mints = int(number_of_mints)
url = "http://api-mainnet.magiceden.dev/v2/collections/" + collection_id + "/activities?offset=0&limit=15"
wallet_url = "http://api-mainnet.magiceden.dev/v2/wallets/" + wallet_address + "/escrow_balance"
number_of_times_minted = 0
continue_code = True
while True :
    while should_mint_bool == False :
        payload={}
        headers = {}
        payload3={}
        headers3 = {}
        minimum_price = float(target_floor_price)
        response = requests.request("GET", url, headers=headers, data=payload)
        wallet_balance = requests.request("GET", wallet_url, headers=headers3, data=payload3).text
        finalresponse = response.text
        splitoutput = finalresponse.replace(",","\n")
        metadata_array = splitoutput.split('}')
        fixed_array = []
        for i in range(0,14) :
            fixed_array.append(metadata_array[i].replace("delist"," "))
        matching_buynow = [s for s in fixed_array if "list" in s]
        word_price = 'price":'
        word_address1 = 'tokenMint":"'
        word_address2 = '"\n"collection"'
        word_address3 = 'seller":"'
        word_address4 = '"\n"sellerReferral"'
        first_item_metadata = matching_buynow[0]
        res1 = matching_buynow[0].partition(word_price)[2]
        res2 = matching_buynow[0].partition(word_address1)[2]
        nft_address = res2.partition(word_address2)[0]
        res3 = matching_buynow[0].partition(word_address3)[2]
        seller_address = res3.partition(word_address4)[0]
        price_float = float(res1)
        price_int = int(price_float)
        price_str = str(price_int)
        if price_float <= minimum_price : 
            print("[SNIPER] : Deal found, minting NFT for price of : " + price_str)
            should_mint_bool = True
            break
        should_mint_str = str(should_mint_bool)
        print("[SNIPER] : Deal not found, not minting, price of last listed NFT : " + price_str)
        time.sleep(1)
    if __name__ == '__main__':
        wallet_s = SolanaWallet(b58_private_key=str(b58encode(private_key1)))
        ATAresult = RESOURCE.get_associated_token_account_address(
            mint_address = nft_address,
            public_key = seller_address
        )
        buying_tx = RESOURCE.buy_nft(
            mint_address=nft_address,
            wallet=wallet_s,
            network=network,
            exchange=exchange,
            nft_price=price_int
        )

    buy_now_call = "https://api-mainnet.magiceden.io/v2/instructions/buy_now?buyer=" + wallet_address + "&seller=" + seller_address + "&auctionHouseAddress=E8cU1WiRWjanGxmn96ewBgk9vPTcL6AEZ1t6F6fkgUWe&tokenMint=" + nft_address + "&tokenATA=" + ATAresult + "&price=" + price_str + "&sellerReferral=autMW8SgBkVYeBgqYiTuJZnkvDZMVU2MHJh9Jh7CSQ2&sellerExpiry=0"
    minting_url = "https://api.blockchainapi.com/v1/solana/nft/marketplaces/magic-eden/buy/mainnet-beta/" + nft_address
    payload2 = {}
    headers2 = {}


    response2 = requests.request("GET", buy_now_call, headers=headers2, data=payload2)
    if should_mint_bool == True :

        print("[MINT BOT] : NFT minted at price of : " + price_str + " Continuing search.")
        number_of_times_minted = number_of_times_minted + 1
        should_mint_bool = False
        if number_of_times_minted == number_of_mints :
            break
        print("Taking a little break to wait for transaction to process. 2 minutes.")
        time.sleep(120)