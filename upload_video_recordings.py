#!/usr/bin/env python3
"""Upload YouTube video recordings to Supabase"""
import os
from supabase import create_client

# Supabase credentials
url = os.environ.get("SUPABASE_URL", "https://xcctqbamimafkkamuwly.supabase.co")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not key:
    print("❌ Error: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

supabase = create_client(url, key)

# Video recordings data
videos = [
    # 2025
    {
        "year": 2025,
        "date_text": "13 Mar: Hybrid Session",
        "title": "7:30pm - 8:00pm: Sharing by Bob LEE, DPA\n8:00pm - 8:30pm: Sharing by Ar PAN Yi Cheng, Type0 Architecture",
        "url": "https://youtu.be/FYu6R862JBw?si=ih4aOLEOKlGOkpQ2",
        "sort_order": 1
    },
    {
        "year": 2025,
        "date_text": "10 Apr: Hybrid Session",
        "title": "7:15pm - 7:30pm: Sharing by Jia Ming OW, BETA, BCA\n7:30pm - 8:00pm: Sharing by Dr Ferdin Joe John Joseph, AliBaba Cloud Singapore\n8:00pm - 8:30pm: Sharing by Anders ANG, WOHA",
        "url": "https://youtu.be/C6wzCtttBw4?si=SUCGWIamt3_523ON",
        "sort_order": 2
    },
    # 2024
    {
        "year": 2024,
        "date_text": "19 Feb, 6:30-8:30pm",
        "title": "Ideation Meetup, by Mr SIM Quentin and Mr PONG Woon Wei",
        "url": "https://youtu.be/sZozlwV43_Y?si=_Rvn8ZCBoAZwwv_X",
        "sort_order": 1
    },
    {
        "year": 2024,
        "date_text": "26 Feb, 6:30-8:30pm",
        "title": "Autodesk Solutions, by Mr Sagar Thorat & Mr Ken Soh",
        "url": "https://youtu.be/1ZicaJF-oCY?si=mzAidFlZboDW-Jss",
        "sort_order": 2
    },
    {
        "year": 2024,
        "date_text": "28 Feb, 6:30-8:30pm",
        "title": "Trimble Sketchup & LLM, by Mr Jason Li, M.Msoer",
        "url": "https://youtu.be/JFfh_w_9H5k?si=64rwLv3Scau4SSb4",
        "sort_order": 3
    },
    {
        "year": 2024,
        "date_text": "29 Feb, 6:30-8:30pm",
        "title": "Stable Diffusion & ControlNet AI Workshop, by Ar SIM Quentin, Limau Studio",
        "url": "https://youtu.be/768VFGncyp8?si=-Wuf-0CEdACQH0oR",
        "sort_order": 4
    },
    {
        "year": 2024,
        "date_text": "4 Mar, 6:30-7:15pm",
        "title": "AI Solutions Development, by Mr FENG Weihan, AISG Apprentice Graduate",
        "url": "https://youtu.be/RmX4OyQYSK8?si=RTXKnvnmsnJsyRDE",
        "sort_order": 5
    },
    {
        "year": 2024,
        "date_text": "11 Mar, 6:30-8:30pm",
        "title": "Graphisoft AI Solutions, by Mr Vimal Kumar",
        "url": "https://youtu.be/jNQTUvcdcJU?si=TFpGmfoGL2sCe3LF",
        "sort_order": 6
    },
    {
        "year": 2024,
        "date_text": "18 Mar, 6:30-8:15pm",
        "title": "Podium & AI Solutions, by Mr Luke TAN, Lendlease\nSketchup Solutions by Michael WONG, Warehouse Blueprint",
        "url": "https://youtu.be/SSGnfunclew?si=nDUUJowg14cGSra4",
        "sort_order": 7
    },
    {
        "year": 2024,
        "date_text": "25 Mar, 6:30-7:15pm",
        "title": "AI and GenAI Solutions, by Vignesh Kaushik, Gensler",
        "url": "https://www.youtube.com/watch?v=7GmNuGpTLF0",
        "sort_order": 8
    },
    # 2023 and earlier
    {
        "year": 2023,
        "date_text": "2023 and earlier",
        "title": "YAL AI Talks and earlier computational BIM workshops",
        "url": "https://www.integrations.space/p/past-workshops.html",
        "sort_order": 1
    }
]

try:
    # Delete existing records
    supabase.table("video_recordings").delete().neq("id", 0).execute()
    print("✅ Cleared existing video recordings")
    
    # Insert new records
    result = supabase.table("video_recordings").insert(videos).execute()
    print(f"✅ Uploaded {len(videos)} video recordings")
    print(f"   - 2025: 2 videos")
    print(f"   - 2024: 8 videos")
    print(f"   - 2023: 1 link")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
