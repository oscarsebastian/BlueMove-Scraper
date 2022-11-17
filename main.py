import cloudscraper
import datetime
import pytz
import time
import csv
from discord_webhook import DiscordWebhook,DiscordEmbed

def send_hook(collection_name:str,
              collection_description:str,
              avatar:str,
              project_banner:str,
              total_nfts:str,
              nft_per_user:str,
              module_address:str,
              start_time:str,
              price_per_item:str,
              launchpad_name_extension:str,
              launchpad_slug:str):
    
    webhook = DiscordWebhook(
        url=
        'YOUR_WEBHOOK_URL'
    )
    embed = DiscordEmbed(title=f'{collection_name} loaded!',
                         description=collection_description,
                         url=f"https://bluemove.net/launchpad-detail/{launchpad_slug}",
                         color='0x7b253c')
    
    if total_nfts:
        embed.add_embed_field(name='Supply', value=total_nfts, inline=False)
    if nft_per_user:
        embed.add_embed_field(name='Max Per Wallet', value=nft_per_user, inline=False)
    if price_per_item:
        embed.add_embed_field(name='Price', value=f"{str(int(price_per_item)/100000000)} APTOS", inline=False)
    if module_address:
        embed.add_embed_field(name='Contract', value=module_address, inline=False)
    if start_time:
        embed.add_embed_field(name='Drop Time', value=f"<t:{start_time}>", inline=False)
    if launchpad_name_extension:
        embed.add_embed_field(name='Status', value=launchpad_name_extension, inline=False)
    if avatar:
        embed.set_thumbnail(url=avatar)
    if project_banner:
         embed.set_image(url=project_banner)

    embed.set_timestamp()
    webhook.add_embed(embed)
    hook_response = webhook.execute()
    while hook_response.status_code == 429:
        hook_response = webhook.execute()
        time.sleep(2)


def checked_collections(launchpad_slug:str):
    with open('checked_collections.csv', 'r') as fp:
                checked_collections = fp.read()
    if launchpad_slug not in checked_collections:
        f = open('checked_collections.csv', 'a', newline="")
        writer = csv.writer(f)
        writer.writerow((launchpad_slug, 'Checked'))
        f.close()
        return False
    else:
        return True

def fetch_information(drop_json:dict):
    fetched_info={}
    to_fetch=['collection_name','collection_description','avatar','project_banner','total_nfts','nft_per_user','module_address','start_time','price_per_item','launchpad_name_extension','launchpad_slug']
    for key in to_fetch:
        if key in drop_json.keys():
            fetched_info[key]=drop_json[key]
    return fetched_info

def scrape_api(delay:int):
    while True:
        scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
        url = 'https://aptos-mainnet-api.bluemove.net/api/launchpads'
        req= scraper.get(url)
        parsed=req.json()
        for drop in parsed['data']:
            drop_info=fetch_information(drop['attributes'])
            collection_name,collection_description,avatar,project_banner,\
            total_nfts,nft_per_user,module_address,start_time,price_per_item,\
            launchpad_name_extension,launchpad_slug=drop_info['collection_name'],drop_info['collection_description'],\
                                            drop_info['avatar'],drop_info['project_banner'],\
                                            drop_info['website'],drop_info['twitter'],\
                                            drop_info['total_nfts'],drop_info['nft_per_user'],\
                                            drop_info['module_address'],drop_info['start_time'],\
                                            drop_info['price_per_item'],drop_info['launchpad_name_extension'],drop_info['launchpad_slug']

            start_time=int(start_time[:-3])
            drop_date=datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d')
            today = datetime.datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d")
            if drop_date == today and not checked_collections(launchpad_slug):
                print(f"Collection : {launchpad_slug} dropping today!")
                send_hook(collection_name,
                            collection_description,
                            avatar,
                            project_banner,
                            total_nfts,
                            nft_per_user,
                            module_address,
                            start_time,
                            price_per_item,
                            launchpad_name_extension,
                            launchpad_slug)
        print('Sleeping..')
        time.sleep(delay)

scrape_api(15)