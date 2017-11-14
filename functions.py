import hvac
import json
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

# generate token for created policy
def tokencreate(policyname, vaultaddress, vaulttoken, ttl):
    client = hvac.Client(url = vaultaddress, token = vaulttoken, verify = False)
    token = client.create_token(orphan = True, policies = policyname, ttl = ttl)
    return token["auth"]


# write generated token back to vault
def writetoken(token, tokenpath, vaultaddress, vaulttoken):
    client = hvac.Client(url = vaultaddress, token = vaulttoken, verify = False)
    client.write(path = tokenpath, **token)
