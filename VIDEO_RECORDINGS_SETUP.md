# YouTube Video Recordings Setup

## Overview
Added a new "YouTube Video Recordings" section to members.html that displays past session recordings from 2023-2025.

## What Was Done
1. ✅ Added new section in members.html (below "AI Sharing Sessions")
2. ✅ Created JavaScript to fetch and display videos from Supabase
3. ✅ Styled video cards with collapsible year grouping
4. ✅ Pushed code to GitHub

## What You Need to Do (Supabase Setup)

### Step 1: Create the Table
1. Go to Supabase Dashboard: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly
2. Click "SQL Editor" in the left sidebar
3. Open the file: `SETUP_VIDEO_RECORDINGS.sql`
4. Copy ALL the SQL content
5. Paste it into the Supabase SQL Editor
6. Click "Run" to execute

This will:
- Create the `video_recordings` table
- Enable Row Level Security (RLS)
- Insert all 11 video recordings (2 from 2025, 8 from 2024, 1 from 2023)
- Create indexes for performance

### Step 2: Verify
1. In Supabase, go to "Table Editor"
2. Select "video_recordings" table
3. You should see 11 rows grouped by year (2025, 2024, 2023)

## How It Works
- **Section appears only for logged-in registered members** (same access control as other members-only content)
- **Videos are grouped by year** (2025 → 2024 → 2023)
- **Each video shows**:
  - Date/session time
  - Speaker names
  - "Watch Recording →" link
- **Data is stored in Supabase** (not in git) - you can update videos via SQL without code changes

## Future Updates
To add new videos, just run SQL in Supabase:
```sql
INSERT INTO video_recordings (year, date_text, title, url, sort_order) VALUES
(2026, '15 Jan: Hybrid Session', 'Speaker name and topic', 'https://youtu.be/...', 1);
```

The webpage will automatically display the new videos!
