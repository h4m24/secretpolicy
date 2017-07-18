import argparse
import hvac
import json
import sys

ConfigFilePath = './config.json'
SecretsFilePath = './secrets.json'

# read configuration from json file


def readconfig(configfilepath):
    with open(configfilepath, encoding='utf-8-sig') as json_file:
        text = json_file.read()
        json_data = json.loads(text)
        return json_data

# read secrets and paths from json file


def readsecrets(secretfilepath):
    with open(secretfilepath, encoding='utf-8-sig') as json_file:
        text = json_file.read()
        json_data = json.loads(text)
        return json_data


# check if secrets are stored


def secretexists(path, vaultaddress, vaulttoken):
    # print(path, vaultaddress, vaulttoken)
    client = hvac.Client(url=vaultaddress, token=vaulttoken, verify=False)
    if client.read(path)is None:
        return False
    return True

# write secrets to paths


def writetovault(path,  secretdict, vaultaddress, vaulttoken):
    client = hvac.Client(url=vaultaddress, token=vaulttoken, verify=False)
    client.write(path, **secretdict)


# generate a policy file in the output
# write policy file to vault
# spit out policy name


def writepolicy(topicname, pathslist, vaultaddress, vaulttoken):
    client = hvac.Client(url=vaultaddress, token=vaulttoken, verify=False)
    outputfile = topicname[0] + ".hcl"

    # Create a file
    with open(outputfile, 'w') as out:
        for path in pathslist:
            blockhead = "path \"" + path + "\""
            out.write(blockhead)
            out.write("\n")
            out.write('{ capabilities = ["read"] }')
            out.write("\n")
            out.write("\n")

    # write file to vault
    with open(outputfile, 'r') as policyfile:
        client.set_policy(topicname[0], policyfile.read())
        print(client.get_policy(topicname[0]))


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
