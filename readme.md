# write secrets and policies 

## purpose
easy semi-automatic way of writing secrets to vault and creating policies for those secrets on the fly in vault,
the script will spit out a file as an hcl policy read from vault after writing to be version controlled.

## getting started
- fill out the ```config.json``` file with the appropriate vault address and token
- fill out ```secrets.json``` file with desired secrets to be in vault, respecting the json structure.
- run the script as ```python3 main.py -t TOPIC```
- DONE!


### to do
- fix duplicate key names overwrite in secrets dict
- enforce requiring  ```-t```
- add https support.

### more
- PRs are welcome!.
