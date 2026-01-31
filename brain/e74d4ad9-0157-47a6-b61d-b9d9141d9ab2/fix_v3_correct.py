import json

# Load v3_CLEAN
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3_CLEAN.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

wf['name'] = 'Scheduled_Group_Post_v3'

# 1. ADD Filter Pending node
filter_node = {
    "parameters": {
        "conditions": {
            "conditions": [
                {
                    "id": "filter-pending",
                    "leftValue": "={{ $json['Status'] }}",
                    "rightValue": "Pending",
                    "operator": {"type": "string", "operation": "equals"}
                }
            ]
        },
        "options": {}
    },
    "id": "filter-pending-posts",
    "name": "Filter Pending",
    "type": "n8n-nodes-base.filter",
    "typeVersion": 2.3,
    "position": [6400, 2240]
}

# 2. ADD Switch node
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

# Insert nodes
combine_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Combine Post + Groups Data')
wf['nodes'].insert(combine_idx + 1, switch_node)

read_idx = next(i for i, n in enumerate(wf['nodes']) if n.get('name') == 'Read Posts Schedule')
wf['nodes'].insert(read_idx + 1, filter_node)

# Update connections
wf['connections']['Read Posts Schedule'] = {
    "main": [[{"node": "Filter Pending", "type": "main", "index": 0}]]
}

wf['connections']['Filter Pending'] = {
    "main": [[{"node": "Split Posts Batch", "type": "main", "index": 0}]]
}

wf['connections']['Combine Post + Groups Data'] = {
    "main": [[{"node": "Switch Post Type", "type": "main", "index": 0}]]
}

wf['connections']['Switch Post Type'] = {
    "main": [
        [{"node": "Split Groups Batch", "type": "main", "index": 0}],  # Text → Split Groups
        [{"node": "Split Groups Batch", "type": "main", "index": 0}]   # Media → Split Groups (same flow!)
    ]
}

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("✅ ĐÃ THÊM:")
print("   - Filter Pending")
print("   - Switch Post Type")
print(f"   - Total nodes: {len(wf['nodes'])}")
