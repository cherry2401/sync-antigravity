import json

# Load workflow
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Find "Post Text Only" node index
text_post_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Post Text Only')

# Nodes to duplicate for TEXT branch
text_nodes = [
    {"old_name": "Construct Facebook URL", "new_name": "Construct URL (Text)", "new_id": "construct-text", "pos": [8200, 2000]},
    {"old_name": "If", "new_name": "If Success (Text)", "new_id": "if-text", "pos": [8400, 2000]},
    {"old_name": "Log Success to Sheet", "new_name": "Log Success (Text)", "new_id": "log-text", "pos": [8600, 1900]},
    {"old_name": "Telegram Notify Success", "new_name": "Telegram Success (Text)", "new_id": "tg-text", "pos": [8800, 1900]},
    {"old_name": "Wait Between Groups", "new_name": "Wait (Text)", "new_id":"wait-text", "pos": [9000, 2000]}
]

# Add duplicated nodes after Post Text Only
insert_pos = text_post_idx + 1
for spec in text_nodes:
    # Find original
    orig = next(n for n in wf['nodes'] if n.get('name') == spec['old_name'])
    # Copy
    new_node = json.loads(json.dumps(orig))
    new_node['name'] = spec['new_name']
    new_node['id'] = spec['new_id']
    new_node['position'] = spec['pos']
    if 'webhookId' in new_node:
        new_node['webhookId'] = f"{spec['new_id']}-webhook"
    # Insert
    wf['nodes'].insert(insert_pos, new_node)
    insert_pos += 1

# Update connections
wf['connections']['Post Text Only'] = {
    "main": [[{"node": "Construct URL (Text)", "type": "main", "index": 0}]]
}
wf['connections']['Construct URL (Text)'] = {
    "main": [[{"node": "If Success (Text)", "type": "main", "index": 0}]]
}
wf['connections']['If Success (Text)'] = {
    "main": [
        [{"node": "Log Success (Text)", "type": "main", "index": 0}],
        []  # Error branch - add later if needed
    ]
}
wf['connections']['Log Success (Text)'] = {
    "main": [[{"node": "Telegram Success (Text)", "type": "main", "index": 0}]]
}
wf['connections']['Telegram Success (Text)'] = {
    "main": [[{"node": "Wait (Text)", "type": "main", "index": 0}]]
}
wf['connections']['Wait (Text)'] = {
    "main": [[{"node": "Split Groups Batch", "type": "main", "index": 0}]]
}

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("✅ Added text-only branch nodes!")
print(f"Total nodes: {len(wf['nodes'])}")
