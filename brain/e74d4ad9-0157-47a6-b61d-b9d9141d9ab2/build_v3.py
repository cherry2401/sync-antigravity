import json
import copy

# Load v3_CLEAN to extract working nodes
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3_CLEAN.json', 'r', encoding='utf-8') as f:
    v3_clean = json.load(f)

# Find nodes by name
def find_node(nodes, name):
    for node in nodes:
        if node.get('name') == name:
            return copy.deepcopy(node)
    return None

nodes_v3 = v3_clean['nodes']

# Extract working nodes
schedule_trigger = find_node(nodes_v3, 'Schedule Trigger - Every 4,9,13,15,20h')
read_posts = find_node(nodes_v3, 'Read Posts Schedule')
split_posts = find_node(nodes_v3, 'Split Posts Batch')
parse_media = find_node(nodes_v3, 'Parse Media & Groups')
read_groups = find_node(nodes_v3, 'Read Groups Config')
combine_data = find_node(nodes_v3, 'Combine Post + Groups Data')
split_groups = find_node(nodes_v3, 'Split Groups Batch')
wait_group = find_node(nodes_v3, 'Wait Group Delay')
log_success = find_node(nodes_v3, 'Log Success to Sheet')
telegram_success = find_node(nodes_v3, 'Telegram Notify Success')
log_error = find_node(nodes_v3, 'Log Error to Sheet')
telegram_error = find_node(nodes_v3, 'Telegram Notify Error')
wait_between = find_node(nodes_v3, 'Wait Between Groups')
update_complete = find_node(nodes_v3, 'Update Post Completed')
facebook_post = find_node(nodes_v3, 'Create Group Post using Page')

# Rename schedule trigger
schedule_trigger['name'] = 'Schedule Trigger'
schedule_trigger['position'] = [1000, 300]

# Update positions
read_posts['position'] = [1200, 300]
split_posts['position'] = [1600, 300]
parse_media['position'] = [1800, 300]
read_groups['position'] = [2000, 300]
combine_data['position'] = [2200, 300]
split_groups['position'] = [2400, 300]
wait_group['position'] = [2600, 300]

# Modify Parse Media & Groups to add has_media
parse_media['parameters']['jsCode'] = """// Parse Media URLs and Group IDs from post
const postData = $input.item.json;

const mediaUrls = String(postData['Media URLs'] || '').split('|')
  .map(url => url.trim())
  .filter(url => url);

const groupIds = String(postData['Groups'] || '').split('|')
  .map(id => id.trim())
  .filter(id => id);

return {
  json: {
    post_id: postData['Post ID'],
    content: postData['Content'],
    media_urls: mediaUrls,
    has_media: mediaUrls.length > 0,
    group_ids: groupIds
  }
};
"""

# Modify Combine to pass has_media
combine_data['parameters']['jsCode'] = combine_data['parameters']['jsCode'].replace(
    'has_media: (postData.media_urls || []).length > 0,',
    'has_media: postData.has_media,'
)

# Create Filter Pending node
filter_pending = {
    "parameters": {
        "conditions": {
            "conditions": [{
                "id": "filter-pending",
                "leftValue": "={{ $json['Status'] }}",
                "rightValue": "Pending",
                "operator": {
                    "type": "string",
                    "operation": "equals"
                }
            }]
        }
    },
    "id": "filter-pending-id",
    "name": "Filter Pending",
    "type": "n8n-nodes-base.filter",
    "typeVersion": 2.3,
    "position": [1400, 300]
}

# Create Switch node
switch_node = {
    "parameters": {
        "rules": {
            "rules": [
                {
                    "id": "rule-text",
                    "output": 0,
                    "conditions": {
                        "conditions": [{
                            "leftValue": "={{ $json.has_media }}",
                            "rightValue": False,
                            "operator": {
                                "type": "boolean",
                                "operation": "equals"
                            }
                        }]
                    }
                },
                {
                    "id": "rule-media",
                    "output": 1,
                    "conditions": {
                        "conditions": [{
                            "leftValue": "={{ $json.has_media }}",
                            "rightValue": True,
                            "operator": {
                                "type": "boolean",
                                "operation": "equals"
                            }
                        }]
                    }
                }
            ]
        },
        "options": {}
    },
    "id": "switch-media-id",
    "name": "Switch Media Type",
    "type": "n8n-nodes-base.switch",
    "typeVersion": 3.2,
    "position": [2800, 300]
}

# Create Post Text Only (copy from facebook_post)
post_text = copy.deepcopy(facebook_post)
post_text['name'] = 'Post Text Only'
post_text['id'] = 'post-text-id'
post_text['position'] = [3000, 200]
post_text['parameters']['contentType'] = 'text'
# Remove mediaIds parameter
if 'mediaIds' in post_text['parameters']:
    del post_text['parameters']['mediaIds']

# Create other media branch nodes...
prepare_media = {
    "parameters": {
        "jsCode": """const groupData = $input.first().json;
const mediaUrls = groupData.media_urls || [];

return mediaUrls.map((url, index) => ({
  json: {
    media_url: url,
    media_index: index,
    page_id: groupData.page_id,
    access_token: groupData.access_token,
    _group_data: groupData
  }
}));"""
    },
    "id": "prep-media-id",
    "name": "Prepare Media Items",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [3000, 400]
}

# Build complete workflow
workflow = {
    "name": "Scheduled_Group_Post_v3_FINAL",
    "nodes": [
        schedule_trigger,
        read_posts,
        filter_pending,
        split_posts,
        parse_media,
        read_groups,
        combine_data,
        split_groups,
        wait_group,
        switch_node,
        post_text,
        prepare_media,
        # ... more nodes
    ],
    "connections": {
        "Schedule Trigger": {
            "main": [[{"node": "Read Posts Schedule", "type": "main", "index": 0}]]
        },
        "Read Posts Schedule": {
            "main": [[{"node": "Filter Pending", "type": "main", "index": 0}]]
        },
        "Filter Pending": {
            "main": [[{"node": "Split Posts Batch", "type": "main", "index": 0}]]
        },
        # ... more connections
    },
    "pinData": {},
    "active": False,
    "settings": {"executionOrder": "v1"},
    "id": "sched-group-v3-final",
    "tags": []
}

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3_FINAL.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print("✅ Created Scheduled_Group_Post_v3_FINAL.json")
