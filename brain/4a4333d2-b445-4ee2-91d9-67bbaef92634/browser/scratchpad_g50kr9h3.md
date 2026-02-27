# Task: Capture PDF Template Screenshot

## Plan
- [x] Navigate to `file:///i:/Workflow/n8n/Workflow/New/final.pdf`
- [x] Resize window to roughly 750x1100
- [x] Inject JS/Click controls to hide toolbars and zoom PDF to fit viewport
- [ ] Take a clean screenshot of the PDF content
- [ ] Save screenshot and return path

## Notes
- Current Page ID: `17578734863AF4D0E3AD302CA95A94AE`
- Standard JS selectors (#toolbar) didn't work (internal PDF viewer).
- Used pixel clicking to zoom in. Currently at 90%.
- Next: Zoom to 100%, then try to capture a screenshot and inform the user if the toolbar is still visible.
