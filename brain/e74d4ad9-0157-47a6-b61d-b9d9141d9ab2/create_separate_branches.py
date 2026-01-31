import json
import copy

# Load workflow
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Nodes to duplicate for EACH branch (text + media)
nodes_to_duplicate = [
    "Split Groups Batch",
    "Wait Group Delay",
    "Prepare Group Media Items",
    "Split Group Media Batch",
    "Convert Group File ID to URL",
    "Format Group File URL",
    "Upload Group Media to Facebook",
    "Wait After Group Media Upload",
    "Prepare Post Data with Media",
    "Prepare Post Data without Media",
    "Create Group Post using Page",
    "Construct Facebook URL",
    "If",
    "Log Success to Sheet",
    "Telegram Notify Success",
    "Log Error to Sheet",
    "Telegram Notify Error",
    "Wait Between Groups",
    "Update Post Completed",
    "Wait Between Posts",
    "IF Skip Upload",
    "IF Group Has Media"
]

# Create TEXT branch (suffix: _Text)
text_nodes = []
for node_name in nodes_to_duplicate:
    orig_node = next((n for n in wf['nodes'] if n.get('name') == node_name), None)
    if orig_node:
        new_node = copy.deepcopy(orig_node)
        new_node['name'] = f"{node_name} (Text)"
        new_node['id'] = f"{orig_node['id']}-text"
        # Adjust position (move left)
        new_node['position'][0] -= 500
        new_node['position'][1] -= 400
        text_nodes.append(new_node)

# Create MEDIA branch (suffix: _Media)  
media_nodes = []
for node_name in nodes_to_duplicate:
    orig_node = next((n for n in wf['nodes'] if n.get('name') == node_name), None)
    if orig_node:
        new_node = copy.deepcopy(orig_node)
        new_node['name'] = f"{node_name} (Media)"
        new_node['id'] = f"{orig_node['id']}-media"
        # Adjust position (move right)
        new_node['position'][0] += 500
        new_node['position'][1] += 400
        media_nodes.append(new_node)

# Add nodes to workflow
wf['nodes'].extend(text_nodes)
wf['nodes'].extend(media_nodes)

# Update connections for TEXT branch
wf['connections']['Switch Post Type']['main'][0] = [
    {"node": "Split Groups Batch (Text)", "type": "main", "index": 0}
]

# Update connections for MEDIA branch
wf['connections']['Switch Post Type']['main'][1] = [
    {"node": "Split Groups Batch (Media)", "type": "main", "index": 0}
]

# Duplicate all internal connections for TEXT branch
def update_connections_for_branch(suffix):
    for node_name in nodes_to_duplicate:
        new_name = f"{node_name} ({suffix})"
        if node_name in wf['connections']:
            orig_conns = wf['connections'][node_name]
            new_conns = copy.deepcopy(orig_conns)
            
            # Update target node names
            for output_type in new_conns:
                for output_list in new_conns[output_type]:
                    for conn in output_list:
                        if 'node' in conn:
                            # Update to branch-specific node
                            conn['node'] = f"{conn['node']} ({suffix})"
            
            wf['connections'][new_name] = new_conns

update_connections_for_branch('Text')
update_connections_for_branch('Media')

# Save
with open(r'i:\Workflow\n8n\Workflow\Backups\Scheduled_Group_Post_v3.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print(f"✅ Đã tạo 2 nhánh riêng biệt!")
print(f"Text nodes: {len(text_nodes)}")
print(f"Media nodes: {len(media_nodes)}")
print(f"Total nodes: {len(wf['nodes'])}")
