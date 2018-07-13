#!/usr/bin/env python3

import argparse
import functools
import logging
import multiprocessing
import pathlib
import re
import requests

def get_review_url(group,id):
    real_group_name={'snh48':'SNH48','bej48':'BEJ48','gnz48':'GNZ48','shy48':'SHY48','ckg48':'CKG48'}
    path='/Index/invedio/id/%d'%id
    if group=='snh48':
        url='http://zhibo.ckg48.com%s'%path
    else:
        url='http://live.%s.com%s'%(group,path)
    while True:
        resp=requests.get(url)
        if re.match('^<Response\s\[(?P<code>.*)\]>$',str(resp)).group('code')=='200':
            if len(resp.text)>16:
                try:
                    review_url=re.findall('https?://.*\.m3u8[^"]*',resp.text)[0]
                except IndexError:
                    review_url=''
                break
            else:
                logging.warning('[%s] %d: Empty response'%(real_group_name[group],id))
        else:
            logging.warning('[%s] %d: 502 Bad Gateway'%(real_group_name[group],id))
    return '%d: %s'%(id,review_url)

def main():
    parser=argparse.ArgumentParser()
    add=parser.add_argument
    add('-j','--jobs',type=int,default=32)
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(levelname)s: %(message)s')
    file={'snh48':'0001-SNH48.txt','bej48':'2001-BEJ48.txt','gnz48':'3001-GNZ48.txt','shy48':'6001-SHY48.txt','ckg48':'8001-CKG48.txt'}
    real_group_name={'snh48':'SNH48','bej48':'BEJ48','gnz48':'GNZ48','shy48':'SHY48','ckg48':'CKG48'}
    dir=pathlib.Path('normal')
    try:
        dir.mkdir()
    except FileExistsError:
        pass
    for group_name in ['snh48','bej48','gnz48','shy48','ckg48']:
        if group_name=='snh48':
            url='http://zhibo.ckg48.com'
        else:
            url='http://live.%s.com'%group_name
        while True:
            resp=requests.get(url)
            if re.match('^<Response\s\[(?P<code>.*)\]>$',str(resp)).group('code')=='200':
                if len(resp.text)>16:
                    end_id=max([int(id) for id in re.findall('/Index/invedio/id/(?P<ids>\d+)',resp.text)])
                    break
                else:
                    logging.warning('[%s] Index: Empty response'%real_group_name[group_name])
            else:
                logging.warning('[%s] Index: 502 Bad Gateway'%real_group_name[group_name])
        work=functools.partial(get_review_url,group_name)
        pool=multiprocessing.Pool(args.jobs)
        results=pool.map(work,[id for id in range(1,end_id+1)])
        pool.close()
        pool.join()
        output=dir/file[group_name]
        f=open(output,'w')
        for line in results:
            f.write('%s\n'%line)
        f.close()
        logging.info('[%s] %d URLs written in %s'%(real_group_name[group_name],end_id,output))

if __name__=='__main__':
    main()
