-- Create table for YouTube video recordings
CREATE TABLE IF NOT EXISTS video_recordings (
  id BIGSERIAL PRIMARY KEY,
  year INTEGER NOT NULL,
  date_text TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE video_recordings ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read video recordings
CREATE POLICY "Anyone can read video recordings"
  ON video_recordings
  FOR SELECT
  USING (true);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_video_recordings_year ON video_recordings(year DESC);
CREATE INDEX IF NOT EXISTS idx_video_recordings_sort ON video_recordings(sort_order);
