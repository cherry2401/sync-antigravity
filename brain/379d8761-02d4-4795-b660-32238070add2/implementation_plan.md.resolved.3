# Implement Admin Page ID for Group Posting

To resolve the permission error when posting videos to Groups as a Page, we need to distinguish between the acting Page (Admin) and the target Group.

## User Review Required
> [!IMPORTANT]
> You must add a new column **`Admin Page ID`** to your `Config_Pages` Google Sheet.
> - For Group rows: Fill this with the ID of the Page that is the Admin of that Group.
> - For Page rows: You can leave it blank or fill it with the Page ID.

## Proposed Changes

### Workflow
#### [MODIFY] [REPOST FACEBOOK_v2.json](file:///c:/Users/Cherry/Clone_facebook/Test%20WF/REPOST%20FACEBOOK_v2.json)
- **Combine Data Node**: Updated to extract `Admin Page ID` from the Google Sheet input and pass it as `admin_page_id`.
- **Upload Video Node**: Updated URL to `https://graph.facebook.com/v22.0/{{ $json.admin_page_id }}/videos`. This ensures the video is uploaded to the Admin Page's library.
- **Publish Video Group Node**: Replaced the n8n native Facebook node with a generic **HTTP Request** node.
    - **Reason**: The native node forced the use of the default n8n credential (User Token), ignoring the dynamic Page Token we provided.
    - **Configuration**:
        - URL: `https://graph.facebook.com/v24.0/{{target_page_id}}/feed`
        - Method: POST
        - Body: `message`, `attached_media` (referencing the uploaded video ID), and `access_token` (from the Admin Page).

## Verification Plan

### Manual Verification
1.  **Update Sheet**: User adds `Admin Page ID` column and fills it.
2.  **Run Workflow**: Trigger the workflow for a Group post.
3.  **Check Facebook**: Verify the video is posted to the Group *by the Page*.
4.  **Check Logs**: Verify the workflow completes successfully without permission errors.
