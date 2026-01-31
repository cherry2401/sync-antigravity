import json

# Load v3_CLEAN as base (đã working)
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3_CLEAN.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

wf['name'] = 'Scheduled_Group_Post_v3'

# Find key nodes
combine_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Combine Post + Groups Data')
split_groups_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Split Groups Batch')

# INSERT Switch BEFORE Split Groups Batch
switch_node = {
    "parameters": {
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                        "conditions": [{
                            "leftValue": "={{ $first().has_media }}",  # Check first item
                            "rightValue": False,
                            "operator": {"type": "boolean", "operation": "equals"},
                            "id": "text-rule"
                        }],
                        "combinator": "and"
                    },
                    "renameOutput": True,
                    "outputKey": "text_only"
                },
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                        "conditions": [{
                            "leftValue": "={{ $first().has_media }}",  # Check first item
                            "rightValue": True,
                            "operator": {"type": "boolean", "operation": "equals"},
                            "id": "media-rule"
                        }],
                        "combinator": "and"
                    },
                    "renameOutput": True,
                    "outputKey": "has_media"
                }
            ]
        },
        "options": {}
    },
    "type": "n8n-nodes-base.switch",
    "typeVersion": 3.4,
    "position": [7400, 2240],
    "id": "switch-post-type-final",
    "name": "Switch Post Type"
}

wf['nodes'].insert(split_groups_idx, switch_node)

# Update connections
wf['connections']['Combine Post + Groups Data'] = {
    "main": [[{"node": "Switch Post Type", "type": "main", "index": 0}]]
}

wf['connections']['Switch Post Type'] = {
    "main": [
        [{"node": "Split Groups Batch", "type": "main", "index": 0}],  # Text → Split Groups
        [{"node": "Split Groups Batch", "type": "main", "index": 0}]   # Media → Split Groups (same)
    ]
}

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("✅ ĐÃ SỬA ĐÚNG!")
print(f"Switch Post Type inserted BEFORE Split Groups Batch")
print(f"Total nodes: {len(wf['nodes'])}")
