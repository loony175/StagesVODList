#!/usr/bin/env python3

import argparse
import bs4
import functools
import json
import logging
import multiprocessing
import pathlib
import re
import requests
from urllib import parse

def get_review_url(group,id):
    real_group_name={'snh48':'SNH48','bej48':'BEJ48','gnz48':'GNZ48','shy48':'SHY48','ckg48':'CKG48'}
    path='/Index/invedio/id/%d'%id
    if group=='snh48':
        url='http://zhibo.ckg48.com%s'%path
    else:
        url='http://live.%s.com%s'%(group,path)
    while True:
        while True:
            try:
                resp=requests.get(url)
                break
            except Exception as e:
                logging.warning('[%s] %d: %s'%(real_group_name[group],id,e))
        if resp.status_code==200:
            if len(resp.text)>=36996:
                try:
                    review_url=bs4.BeautifulSoup(resp.text,'html.parser').find_all('input',id='chao_url')[0]['value']
                except IndexError:
                    review_url=''
                if parse.urlparse(review_url).hostname=='ts.48.cn':
                    review_url=review_url.replace('http://','https://')
                break
            else:
                message='Incomplete response'
        elif resp.status_code==502:
            message='502 Bad Gateway'
        else:
            message='HTTP status code not 200 OK'
        logging.warning('[%s] %d: %s'%(real_group_name[group],id,message))
    return id,review_url

def main():
    parser=argparse.ArgumentParser()
    add=parser.add_argument
    add('-j','--jobs',type=int,default=32)
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(levelname)s: %(message)s')
    file={'snh48':'0001-SNH48.json','bej48':'2001-BEJ48.json','gnz48':'3001-GNZ48.json','shy48':'6001-SHY48.json','ckg48':'8001-CKG48.json'}
    real_group_name={'snh48':'SNH48','bej48':'BEJ48','gnz48':'GNZ48','shy48':'SHY48','ckg48':'CKG48'}
    dir=pathlib.Path('normal')
    dir.mkdir(exist_ok=True)
    for group_name in ['snh48','bej48','gnz48','shy48','ckg48']:
        if group_name=='snh48':
            url='http://zhibo.ckg48.com'
        else:
            url='http://live.%s.com'%group_name
        while True:
            while True:
                try:
                    resp=requests.get(url)
                    break
                except Exception as e:
                    logging.warning('[%s] Index: %s'%(real_group_name[group],e))
            if resp.status_code==200:
                if len(resp.text)>16:
                    ids=[]
                    for item in bs4.BeautifulSoup(resp.text,'html.parser').find_all('a',target='_blank'):
                        m=re.match(r'^/Index/invedio/id/(?P<id>\d+)$',item['href'])
                        if m:
                            ids.append(int(m.group('id')))
                    end_id=max(ids)
                    break
                else:
                    message='Incomplete response'
            elif resp.status_code==502:
                message='502 Bad Gateway'
            else:
                message='HTTP status code not 200 OK'
            logging.warning('[%s] Index: %s'%(real_group_name[group],message))
        work=functools.partial(get_review_url,group_name)
        pool=multiprocessing.Pool(args.jobs)
        results=pool.map(work,range(1,end_id+1))
        pool.close()
        pool.join()
        data={}
        for id,review_url in results:
            data[str(id)]=review_url
        output=dir/file[group_name]
        f=open(output,'w')
        f.write(json.dumps(data,indent=2))
        f.write('\n')
        f.close()
        logging.info('[%s] %d URLs written in %s'%(real_group_name[group_name],end_id,output))

if __name__=='__main__':
    main()
