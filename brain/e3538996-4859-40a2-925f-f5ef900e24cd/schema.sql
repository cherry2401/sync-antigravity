-- ⚠️ QUAN TRỌNG: Lệnh này sẽ xóa bảng cũ để tạo lại từ đầu (đảm bảo sạch lỗi Permission)
DROP TABLE IF EXISTS analytics_events CASCADE;

-- Create the analytics_events table
CREATE TABLE analytics_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    event_name TEXT NOT NULL,
    session_id TEXT,
    metadata JSONB DEFAULT '{}'::JSONB
);

-- Enable Row Level Security (RLS)
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- Policy 1: Allow Anonymous/Unauthenticated users to INSERT data (Log events)
CREATE POLICY "Allow Anon Insert"
ON analytics_events
FOR INSERT
TO anon
WITH CHECK (true);

-- Policy 2: Allow Anonymous/Unauthenticated users to READ data (Verify connection)
CREATE POLICY "Allow Anon Read"
ON analytics_events
FOR SELECT
TO anon
USING (true);

-- Policy 3: Service Role (Admin)
CREATE POLICY "Allow Service Role"
ON analytics_events
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
