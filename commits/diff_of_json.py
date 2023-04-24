import os
import json

folder_path = '../data/depends_output_json'

for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)
    # print(item_path)
    if os.path.isdir(item_path):
        json_old_path = os.path.join(item_path, 'old.json')
        json_new_path = os.path.join(item_path, 'new.json')

        with open(json_old_path, 'r') as f:
            json_old = json.load(f)
        with open(json_new_path, 'r') as f:
            json_new = json.load(f)

        diff_json_name = '../data/json_diff/' + os.path.basename(item_path) + '.txt'
        diff_json = open(diff_json_name,"w")
        # print(json_old['variables'],file=diff_json)
        i=0
        for line in json_old['variables']:
            print(i,end='.',file=diff_json)
            i = i + 1
            print(os.path.basename(line),file=diff_json)

        for cell1, cell2 in zip(json_old['cells'], json_new['cells']):
            if cell1 != cell2:
                print(f"  old: {cell1}",file=diff_json)
                print(f"  new: {cell2}",file=diff_json)