# Shop Features Tasks

## Product Listing Page ✅
- [x] `getFilteredProducts(params)` server action
- [x] `useProductFilter` hook with debounce
- [x] `ProductFilters` sidebar component
- [x] `ProductGrid` with pagination
- [x] Mobile filter drawer
- [x] URL-based filtering

## Live Search ✅
- [x] `searchProducts(keyword)` server action
- [x] Vietnamese normalization search
- [x] 300ms debounce
- [x] 5 result limit
- [x] Sale price display (red + strikethrough)
- [x] Keyboard navigation (↑↓ Enter)
- [x] Recent searches localStorage

## User Authentication 🔒
- [x] Install dependencies (`next-auth`, `bcryptjs`) & Update Schema
- [x] Configure NextAuth (`auth.ts`, `auth.config.ts`)
- [x] Implement Server Actions (`register`, `login`)
- [x] Update Login/Register UI
- [x] Link Order to User

## Wishlist Feature ❤️
- [x] Database Schema (`Wishlist` model)
- [x] Server Actions (`toggleWishlist`, `getWishlistIds`)
- [x] `WishlistButton` component (Optimistic UI)
- [x] Wishlist Page (`/tai-khoan/yeu-thich`)
- [x] Integrate with `ProductCard` & Listing Pages

## Address Book Feature 📍
- [x] Database Schema (`Address` model)
- [x] Server Actions (`CRUD Address`)
- [x] `AddressForm` component (Reuse location selectors)
- [x] Address Book Page (`/tai-khoan/dia-chi`)

## Checkout Address Integration 🛒
- [x] Fetch saved addresses in Checkout page
- [x] Display address selection in CheckoutForm
- [x] Auto-fill form with selected address
- [x] Default selection for isDefault address
- [x] Shopee-style Address UI (Compact Card + Modal)

## Payment Flow Integration 💸
- [x] VietQR Bank Config (`src/lib/bank-config.ts`)
- [x] Payment Page with QR (`/thanh-toan/payment/[id]`)
- [x] Redirect Checkout -> Payment Page
- [x] Clean Success Page (Pure Thank You)

## Create Product Feature (Admin) 📦
- [x] Update Schema (`Product`, `Wishlist` relations)
- [x] Cloudinary Config (`.env.local`)
- [x] Server Action (`createProduct`)
- [x] Client Form Integration (`ProductForm.tsx` + Cloudinary Upload)
- [x] Fix Prisma Types & Relation Errors

## Bug Fixes & Refinement 🐛
- [x] Fix PrismaClient types
- [x] Fix TypeScript errors in Product pages (rating/toast)
- [x] Fix TypeScript errors in Product pages (rating/toast)
- [x] Fix Login Redirect Issue (Server Component Refactor)
- [x] Secure Admin Routes (Middleware Protection)

## Category & Brand CRUD Sync 🏷️
- [x] Add `Category` and `Brand` models to schema
- [x] Add `/san-pham` revalidation to `lib/actions/categories.ts`
- [x] Add `/san-pham` revalidation to `lib/actions/brands.ts`
- [x] Add `router.refresh()` to admin danh-muc page
- [x] Add `router.refresh()` to admin thuong-hieu page
- [x] Sync ProductForm dropdowns with dynamic server data
