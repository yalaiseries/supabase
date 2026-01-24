-- Update 2023 YouTube Videos with detailed session recordings

-- Delete the old generic 2023 entry
DELETE FROM video_recordings WHERE year = 2023;

-- Insert detailed 2023 sessions
INSERT INTO video_recordings (year, date_text, title, url, sort_order) VALUES
(2023, '13 Sep 2023, 7:30pm - 8:30pm', 'Taking Control of AI in Architecture by Mr Luke Tan, Lendlease, moderated by Ar William Lau', 'https://www.youtube.com/watch?v=8Bc1gY8rnVU', 1),
(2023, '16 Aug 2023, 7:30pm - 8:30pm', 'Navigating Exponential Change by Mr Luke Tan, Lendlease, moderated by Ar William Lau', 'https://www.youtube.com/watch?v=rfhaHj_sU7c', 2),
(2023, '13 Jul 2023, 7:30pm - 8:30pm', 'Blockchain for Architectural Services and Consultancy? by Mr Edmund Ng, DOXA, moderated by Ar William Lau', 'https://www.youtube.com/watch?v=hbqL4gY63XM', 3),
(2023, '21 Jun 2023, 7:30pm - 8:30pm', 'Using Sketchup with Ruby for Architectural Design, Data Manipulation and Documentation by Mr Jason Li, M Moses, moderated by Ar William Lau', 'https://youtu.be/YSoLgLKRUn4', 4),
(2023, '7 Jun 2023, 7:30pm - 8:30pm', 'AI for Architectural Design by Ar. Razvan I. Ghilic-Micu, Hassell, moderated by Ar William Lau & Mr Alvan NG', 'https://youtu.be/hwsdcgbNaZo', 5),
(2023, '17 May 2023, 7:30pm - 8:30pm', 'Computational BIM with AI for Architectural Design by Giovanni Vigano, Assoc. Director and Samuel Previano Halim, Snr Computational Designer, Ramboll，moderated by Mr Alvan NG', 'https://youtu.be/OsYXB2jGD3Y', 6),
(2023, '28 Apr 2023, 7:30pm - 8:30pm', 'Immersive Experience with AI for Architectural Design by Mr Gerard Teo, CTO, IDA Tech, moderated by Ar William Lau & Mr Alvan NG', 'https://youtu.be/cmTlGZCOt0Y', 7);

-- Verify the update
SELECT * FROM video_recordings WHERE year = 2023 ORDER BY sort_order;

-- Check total count (should be 17 now: 2 from 2025 + 8 from 2024 + 7 from 2023)
SELECT year, COUNT(*) as count FROM video_recordings GROUP BY year ORDER BY year DESC;
