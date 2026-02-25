# Task: Re-Audit Before Deployment

## Previous Fixes (Done)
- [x] Remove `VITE_API_KEY` from frontend `.env`
- [x] Generate strong JWT_SECRET
- [x] Remove hardcoded admin password fallback in `config.ts`
- [x] Update bcrypt to fix dependency vulnerabilities
- [x] Add email/phone validation in registration
- [x] Fix CORS config for production
- [x] Sanitize `object_id` in orders and `link` in convert-uid
- [x] Add price caching for BaoStar API

## Current Re-Audit
- [/] Security scan (remaining gaps)
- [/] Code quality & maintainability
- [/] Performance & UX
- [/] Production readiness checklist
- [ ] Generate updated audit report
