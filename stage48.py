#!/usr/bin/env python3

import argparse
import bs4
import json
import logging
import multiprocessing
import re
import requests
from urllib import parse

def get_review_url(id):
    while True:
        while True:
            try:
                resp=requests.get('https://live.48.cn/Index/invedio/club/1/id/%d'%id)
                break
            except Exception as e:
                logging.warning('[SNH48 Group] %d: %s'%(id,e))
        if resp.status_code==200:
            if len(resp.text)>=36000:
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
        logging.warning('[SNH48 Group] %d: %s'%(id,message))
    return id,review_url

def main():
    parser=argparse.ArgumentParser()
    add=parser.add_argument
    add('-j','--jobs',type=int,default=32)
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(levelname)s: %(message)s')
    while True:
        while True:
            try:
                resp=requests.get('https://live.48.cn/Index/main/club/1')
                break
            except Exception as e:
                logging.warning('[SNH48 Group] Index: %s'%e)
        if resp.status_code==200:
            if len(resp.text)>16:
                ids=[]
                for item in bs4.BeautifulSoup(resp.text,'html.parser').find_all('a',target='_blank'):
                    m=re.match(r'^/Index/invedio/club/1/id/(?P<id>\d+)$',item['href'])
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
        logging.warning('[SNH48 Group] Index: %s'%message)
    pool=multiprocessing.Pool(args.jobs)
    results=pool.map(get_review_url,range(1,end_id+1))
    pool.close()
    pool.join()
    data={}
    for id,review_url in results:
        data[str(id)]=review_url
    output='urls.json'
    f=open(output,'w')
    f.write(json.dumps(data,indent=2))
    f.write('\n')
    f.close()
    logging.info('[SNH48 Group] %d URLs written in %s'%(end_id,output))

if __name__=='__main__':
    main()
