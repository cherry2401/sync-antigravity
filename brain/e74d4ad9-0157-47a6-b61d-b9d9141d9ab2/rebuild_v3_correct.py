import json
import copy

# Load v3_CLEAN as base
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3_CLEAN.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

wf['name'] = 'Scheduled_Group_Post_v3'

# 1. Find "Combine Post + Groups Data" node
combine_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Combine Post + Groups Data')

# 2. Insert Switch AFTER Combine
switch_node = {
    "parameters": {
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                        "conditions": [{
                            "leftValue": "={{ $json.has_media }}",
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
                            "leftValue": "={{ $json.has_media }}",
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
    "id": "switch-post-type",
    "name": "Switch Post Type"
}

wf['nodes'].insert(combine_idx + 1, switch_node)

# 3. Update connections: Combine → Switch → Split Groups
wf['connections']['Combine Post + Groups Data'] = {
    "main": [[{"node": "Switch Post Type", "type": "main", "index": 0}]]
}
wf['connections']['Switch Post Type'] = {
    "main": [
        [{"node": "Split Groups Batch", "type": "main", "index": 0}],  # Text branch
        [{"node": "Split Groups Batch", "type": "main", "index": 0}]   # Media branch - same for now
    ]
}

# Remove old "Wait Group Delay" → "IF Group Has Media" connection
# Keep: Split Groups → Wait Group Delay → (rest of flow)

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("✅ Switch moved to AFTER Combine Post + Groups!")
print(f"Total nodes: {len(wf['nodes'])}")
