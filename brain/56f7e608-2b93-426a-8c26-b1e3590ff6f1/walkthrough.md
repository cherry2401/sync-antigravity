# Authentication & Order Linking Walkthrough

## Overview
We have successfully implemented a complete authentication system using **NextAuth v5** and connected it to the Order system. Users can now Register, Login, and view their personal Order History.

## Changes Implemented

### 1. Database Schema (`prisma/schema.prisma`)
- Added `User` model to store account information.
- Updated `Order` model to include a `userId` field, linking orders to users.

### 2. Authentication System
- **Configuration**:
    - `src/auth.ts`: Main Auth.js initialization with Credentials provider.
    - `src/auth.config.ts`: Edge-compatible configuration.
    - `src/app/api/auth/[...nextauth]/route.ts`: API route for Auth handlers.
- **Server Actions** (`src/actions/auth-actions.ts`):
    - `register`: Handles user registration, password hashing (bcrypt), and DB creation.
    - `login`: Handles user login using NextAuth's `signIn`.

### 3. User Interface
- **Login/Register Page** (`src/app/tai-khoan/page.tsx`):
    - **Refactored**: Split into `AuthForm` (Client) and `page.tsx` (Server).
    - **Logic**: Server component checks `auth()`. If logged in, redirects immediately to `/tai-khoan/don-hang`.
    - Integrated real `register` and `login` server actions.
    - Added error handling and success notifications (Sonner toast).
    - Auto-redirect to order history upon successful login.

### 4. Order System Integration
- **Order Creation** (`src/app/api/order/route.ts`):
    - Now retrieves the session using `auth()`.
    - Automatically attaches `userId` to the new order if the user is logged in.
- **Order History** (`src/app/tai-khoan/don-hang/page.tsx`):
    - Converted to a **Server Component** to securely fetch orders for the logged-in user.
    - Created `OrderListClient` component for rendering the UI.

## Verification Steps
To verify the implementation:

1.  **Register**: Go to `/tai-khoan` -> Select "Đăng ký ngay" -> Create an account.
2.  **Login**: Log in with the new account.
3.  **Order**: Add items to cart and checkout (`/thanh-toan`).
4.  **Verify**:
    - Go to `/tai-khoan/don-hang`.
    - You should see the order you just placed.

> [!NOTE]
> Database commands (`prisma generate`, `prisma db push`) have been executed to apply the schema changes.
