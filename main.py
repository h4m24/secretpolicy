#!/usr/bin/python3

import argparse
import sys
from functions import *

ConfigFilePath = './config.json'
SecretsFilePath = './secrets.json'


def main():
    parser = argparse.ArgumentParser(
        description='Connect to vault and write secrets to it specified in secrets.json file'
                    '\n and create a policy and writing that into vault aswell '
                    'and printing out the policy into an hcl file.\n\n its important '
                    'to note thatsecret keys MUST BE UNIQUE otherwise the last duplicate'
                    ' Secret ID will overwrite the duplicates')

    parser.add_argument('-t', nargs=1, action='store', dest='target',
                        help="set topic of secret , example: service_web OR team_developers", type=str)

    args = parser.parse_args()
    # print(args.target[0])

    vaultconfig = readconfig(ConfigFilePath)
    vaultaddress = vaultconfig['vaultaddress']
    vaulttoken = vaultconfig['vaulttoken']
    secretspathlist = []

    for SecretDocument in readsecrets(SecretsFilePath)['secrets']:
        if secretexists(SecretDocument['path'], vaultaddress, vaulttoken):
            print("Following secret path already populated with a secret, refusing to overwrite")
            print(SecretDocument['path'])
            sys.exit(2)
        else:
            for SecretEntry in SecretDocument['entries']:
                writetovault(SecretDocument['path'], SecretEntry, vaultaddress, vaulttoken)
            secretspathlist.append(SecretDocument['path'])
    writepolicy(args.target, secretspathlist, vaultaddress, vaulttoken)


main()
