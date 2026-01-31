# Rebuild Plan: Workflow V3 with Switch Architecture

## Strategy
Copy proven-working nodes from V3_CLEAN, but reorganize into clean Switch-based flow.

## Nodes to COPY EXACTLY (already working):
1. ✅ Schedule Trigger (lines 233-251)
2. ✅ Read Posts Schedule (lines 253-284)
3. ✅ Split Posts Batch (lines 286-297)
4. ✅ Parse Media & Groups (lines 299-310) - MODIFY to add has_media
5. ✅ Read Groups Config (lines 312-343)
6. ✅ Combine Post + Groups (lines 345-356) - MODIFY to pass has_media
7. ✅ Split Groups Batch (lines 358-369)
8. ✅ Wait Group Delay (lines 371-383)
9. ✅ Log Success (lines 385-496)
10. ✅ Log Error (lines 522-634)
11. ✅ Telegram Notify (lines 498-520, 636-658)
12. ✅ Update Post Completed (lines 672-812)
13. ✅ Create Group Post using Page (lines 195-218) - will use 2x for text/media

## Nodes to CREATE NEW:
1. 🆕 Filter Pending (type: filter, check Status = "Pending")
2. 🆕 Switch Media Type (type: switch, check has_media boolean)
3. 🆕 Post Text Only (copy from Create Group Post, set contentType="text", no mediaIds)
4. 🆕 Prepare Media Items (split media_urls array)
5. 🆕 Split Media Batch (loop per media)
6. 🆕 Convert File ID (Telegram API)
7. 🆕 Format Media URL (construct download URL)
8. 🆕 Upload to Facebook (graph API /photos)
9. 🆕 Wait After Upload
10. 🆕 Collect Media IDs (aggregate all IDs)
11. 🆕 Post With Media (copy from Create Group Post, with mediaIds)
12. 🆕 Wait Between Groups (both branches)

## Changes to existing nodes:

### Parse Media & Groups
Add `has_media` flag:
```javascript
return {
  json: {
    post_id: postData['Post ID'],
    content: postData['Content'],
    media_urls: mediaUrls,
    has_media: mediaUrls.length > 0,  // ← ADD THIS
    group_ids: groupIds,
    //...
  }
};
```

### Combine Post + Groups  
Pass `has_media` through:
```javascript
return targetGroups.map((group, index) => ({
  json: {
    //...
    has_media: postData.has_media,  // ← ADD THIS
    //...
  }
}));
```

## Next Step
Build complete JSON file with all 28 nodes properly connected.
