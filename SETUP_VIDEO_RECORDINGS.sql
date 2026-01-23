-- ============================================================================
-- STEP 1: Run this SQL in Supabase SQL Editor to create the table
-- ============================================================================

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

-- Policy: Anyone can read video recordings (authenticated users only via Edge Function)
CREATE POLICY "Anyone can read video recordings"
  ON video_recordings
  FOR SELECT
  USING (true);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_video_recordings_year ON video_recordings(year DESC);
CREATE INDEX IF NOT EXISTS idx_video_recordings_sort ON video_recordings(sort_order);

-- ============================================================================
-- STEP 2: Insert the video recordings data
-- ============================================================================

INSERT INTO video_recordings (year, date_text, title, url, sort_order) VALUES
-- 2025
(2025, '13 Mar: Hybrid Session', '7:30pm - 8:00pm: Sharing by Bob LEE, DPA
8:00pm - 8:30pm: Sharing by Ar PAN Yi Cheng, Type0 Architecture', 'https://youtu.be/FYu6R862JBw?si=ih4aOLEOKlGOkpQ2', 1),

(2025, '10 Apr: Hybrid Session', '7:15pm - 7:30pm: Sharing by Jia Ming OW, BETA, BCA
7:30pm - 8:00pm: Sharing by Dr Ferdin Joe John Joseph, AliBaba Cloud Singapore
8:00pm - 8:30pm: Sharing by Anders ANG, WOHA', 'https://youtu.be/C6wzCtttBw4?si=SUCGWIamt3_523ON', 2),

-- 2024
(2024, '19 Feb, 6:30-8:30pm', 'Ideation Meetup, by Mr SIM Quentin and Mr PONG Woon Wei', 'https://youtu.be/sZozlwV43_Y?si=_Rvn8ZCBoAZwwv_X', 1),

(2024, '26 Feb, 6:30-8:30pm', 'Autodesk Solutions, by Mr Sagar Thorat & Mr Ken Soh', 'https://youtu.be/1ZicaJF-oCY?si=mzAidFlZboDW-Jss', 2),

(2024, '28 Feb, 6:30-8:30pm', 'Trimble Sketchup & LLM, by Mr Jason Li, M.Msoer', 'https://youtu.be/JFfh_w_9H5k?si=64rwLv3Scau4SSb4', 3),

(2024, '29 Feb, 6:30-8:30pm', 'Stable Diffusion & ControlNet AI Workshop, by Ar SIM Quentin, Limau Studio', 'https://youtu.be/768VFGncyp8?si=-Wuf-0CEdACQH0oR', 4),

(2024, '4 Mar, 6:30-7:15pm', 'AI Solutions Development, by Mr FENG Weihan, AISG Apprentice Graduate', 'https://youtu.be/RmX4OyQYSK8?si=RTXKnvnmsnJsyRDE', 5),

(2024, '11 Mar, 6:30-8:30pm', 'Graphisoft AI Solutions, by Mr Vimal Kumar', 'https://youtu.be/jNQTUvcdcJU?si=TFpGmfoGL2sCe3LF', 6),

(2024, '18 Mar, 6:30-8:15pm', 'Podium & AI Solutions, by Mr Luke TAN, Lendlease
Sketchup Solutions by Michael WONG, Warehouse Blueprint', 'https://youtu.be/SSGnfunclew?si=nDUUJowg14cGSra4', 7),

(2024, '25 Mar, 6:30-7:15pm', 'AI and GenAI Solutions, by Vignesh Kaushik, Gensler', 'https://www.youtube.com/watch?v=7GmNuGpTLF0', 8),

-- 2023 and earlier
(2023, '2023 and earlier', 'YAL AI Talks and earlier computational BIM workshops', 'https://www.integrations.space/p/past-workshops.html', 1);

-- ============================================================================
-- Done! The video_recordings table is now ready
-- ============================================================================
