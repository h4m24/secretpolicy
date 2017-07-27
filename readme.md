# write secrets and policies 

## purpose
easy semi-automatic way of writing secrets to vault and creating policies for those secrets on the fly in vault,
the script will spit out a file as an hcl policy read from vault after writing to be version controlled.

script will check if there are values at the destination path and will NOT overwrite them.
## getting started
- fill out the ```config.json``` file with the appropriate vault address and token
- fill out ```secrets.json``` file with desired secrets to be in vault, respecting the json structure.
- run the script as ```python3 main.py -t TOPIC```
- DONE!


### to do
- check for duplicate key names in secrets dict.
- add checking against https certificates.
- add option to skip/force  writing policies/secrets.
- add flag to write policy file or do ```STDOUT```.
- add dry-run mode.
- check json input.



### Usage

- ```git clone https://github.com/h4m24/secretpolicy.git ~/```
- ``` sudo ln -s ~/secretpolicy /usr/local/bin/secpoly```
- ``` mkdir ~/{env1,env2,env3}```
- ``` touch ~/{env1,env2,env3}/config.json```
- fill out config files per env
- use the symlink in relation to your current directory


### more
- PRs are welcome!.
- please check headers of the script for the shebang that contains python bin path.