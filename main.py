#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import argparse
import sys
from functions import *
import logging
import pprint

ConfigFilePath = './config.json'


def main():

    parser = argparse.ArgumentParser(
        description='Connect to vault and write secrets to it specified in secrets.json file'
                    '\n and create a policy and writing that into vault aswell '
                    'and printing out the policy into an hcl file.\n\n its important '
                    'to note thatsecret keys MUST BE UNIQUE otherwise the last duplicate'
                    ' Secret ID will overwrite the duplicates')

    parser.add_argument('-t', nargs=1, action='store', dest='target',
                        help="set topic of secret , example: service_web OR team_developers", type=str)
    parser.add_argument('-s', nargs=1, action='store', dest='SecretsFilePath',
                        help="secrets.json file path", type=str)
    parser.add_argument('-ttl', nargs=1, action='store', dest='tokenttl',
                        help="time to leave for token", type=str)
    parser.add_argument('-l', nargs=1, action='store', dest='LogLevel',
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'],
                        help="log level DEBUG ERROR WARN CRITICAL", type=str)

    args = parser.parse_args()

    if args.target and args.SecretsFilePath:

        if not args.LogLevel:
            logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                                format='[%(asctime)s] %(levelname)s  %(message)s')
        else:
            logging.basicConfig(level=args.LogLevel[0], datefmt='%Y-%m-%d %H:%M:%S',
                                format='[%(asctime)s] %(levelname)s  %(message)s')

        vaultconfig = readconfig(ConfigFilePath)
        vaultaddress = vaultconfig['vaultaddress']
        vaulttoken = vaultconfig['vaulttoken']
        secretspathlist = []

        for SecretDocument in readsecrets(args.SecretsFilePath[0])['secrets']:
            if secretexists(SecretDocument['path'], vaultaddress, vaulttoken):
                print("Following secret path already populated with a secret, refusing to overwrite")
                print(SecretDocument['path'])
                sys.exit(2)
            else:
                for SecretEntry in SecretDocument['entries']:
                    logging.info("writing secrets")
                    writetovault(SecretDocument['path'], SecretEntry, vaultaddress, vaulttoken)
                secretspathlist.append(SecretDocument['path'])
        logging.info("writing policies")
        writepolicy(args.target, secretspathlist, vaultaddress, vaulttoken)
        token = tokencreate(args.target, vaultaddress, vaulttoken, args.tokenttl[0])
        #this is path where we will store token. it is tokenspath from config file + topicname
        tokenpath = vaultconfig['tokenspath'] + args.target[0]
        #writing token to this path
        writetoken(token, tokenpath, vaultaddress, vaulttoken)
    else:
        print("please provide topic and secret file path ")
        sys.exit(2)


main()
