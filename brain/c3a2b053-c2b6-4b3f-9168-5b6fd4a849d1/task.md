# Backup Credentials Workflow Fix

## Problem
- Original workflow used `n8n-nodes-base.n8n` API node which returns 404 error due to hosting API configuration issues
- Need to adapt workflow to use custom `n8n-nodes-backup-credentials` node instead

## Tasks

### Main Workflow
- [x] Replace "Get many workflows" node with "Backup credentials" custom node
- [x] Add Code node to parse binary data into JSON array (29 credentials parsed)
- [x] Update connections: triggers → Backup credentials → Code parser → Loop Over Items
- [x] Remove obsolete nodes (Get many workflows, JSON formatting)

### Subworkflow  
- [x] Update "isDiffOrNew" Code node to compare credentials instead of workflows
- [x] Update GitHub "Create new file" commit message to handle credential names
- [x] Update GitHub "Edit existing file" commit message to handle credential names
- [ ] Test single credential backup to verify subworkflow works correctly

### Testing
- [ ] Test workflow execution with manual trigger
- [ ] Verify GitHub files are created with correct structure
- [ ] Test schedule trigger (optional)
