import datetime, json, os, time, uuid, ast


songs = []

with open('data.json', 'r', encoding='UTF-8') as f:
    new_streamings = ast.literal_eval(f.read())
    songs += [streaming for streaming 
                    in new_streamings]



for item in songs:
    features=[]
    features.append(item)
    print(features)

for item in songs:
    print(item['name'])
    