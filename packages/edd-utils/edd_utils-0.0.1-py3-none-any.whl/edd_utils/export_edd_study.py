#!/bin/python
import argparse
import getpass
from __init__ import login, export_study

parser = argparse.ArgumentParser(description="Download an Study CSV from an EDD Instance")

#Slug (Required)
parser.add_argument("slug", help="The EDD instance study slug to download.")

#UserName (Optional) [Defaults to Computer User Name]
parser.add_argument('--username', help='Username for login to EDD instance.',default=getpass.getuser())

#EDD Server (Optional) [Defaults to edd.jbei.org]
parser.add_argument('--server', help='EDD instance server',default='edd.jbei.org')

args = parser.parse_args()

#Login to EDD
session = login(edd_url=args.server,user=args.username)

if session is not None:
    #Download Study to Dataframe
    df = export_study(session,args.slug)

    #Write to CSV
    df.to_csv(f'{args.slug}.csv')