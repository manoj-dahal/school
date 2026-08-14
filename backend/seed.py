"""Seed the Siddeshwor school database with live-site content."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from db import get_db, hash_password, init_db

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

SETTINGS = {
    "school_name": "Shree Siddeshwor Secondary School",
    "short_name": "Siddeshwor School",
    "estd": "2047",
    "established_ad": "2008",
    "tagline": "Dedicated to Excellence in Education",
    "phone": "01-4622730",
    "email": "mail@siddeshwor.edu.np",
    "address": "Shantinagar, New Baneshwor, Kathmandu",
    "office_hours": "Sunday - Friday: 7:00 AM - 4:00 PM",
    "office_closed": "Saturday: Closed",
    "students": "506",
    "ero_score": "72.58",
    "level": "Nursery–10",
    "status": "Co-ed / Day",
    "years": "15",
    "teachers": "25",
    "see_rate": "100",
    "map_embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.3!2d85.3358!3d27.6942!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb199a06c2eaf9%3A0xc5f361ab580a1f6b!2sM8PV%2BPFX%2C%20Kathmandu%2044600!5e0!3m2!1sen!2snp!4v1700000000000!5m2!1sen!2snp",
    "about": "Shree Siddeshwor Secondary School is a public school located in Shantinagar, New Baneshwor, Kathmandu Metropolitan City, Kathmandu district, within Bagmati Province. The school provides education from Early Childhood Development (ECD) to Grade 10.",
    "mission": "To provide comprehensive secondary education from Grade 1 to Grade 10 through innovative teaching methods, strong academic fundamentals, and character-building programs that prepare students for success in their SEE examinations and future academic pursuits.",
    "vision": "To be recognized as a leading secondary school that transforms students into dedicated, disciplined, and capable individuals who excel academically and are ready to face the challenges of higher education and life with confidence.",
}

HERO = [
    ("https://i.ibb.co/9DJpB0X/IMG-20260801-WA0138.jpg", "Siddeshwor School Building"),
    ("https://i.ibb.co/0p6vsq8R/IMG-20260801-WA0051.jpg", "Siddeshwor School"),
    ("https://i.ibb.co/39hhxtzv/IMG-20260801-WA0089.jpg", "Siddeshwor School"),
    ("https://i.ibb.co/kVGrDDsT/IMG-20260801-WA0026.jpg", "Siddeshwor School"),
]

FACILITIES = [
    ("💻", "Computer Education",
     "State-of-the-art computer labs with latest technology and software to prepare students for the digital age.",
     "State-of-the-art computer labs with latest technology and software to prepare students for the digital age. Each lab is equipped with modern computers, high-speed internet, and specialized software for various courses."),
    ("👔", "School Uniform",
     "Professional dress code that instills discipline and creates a sense of unity among students.",
     "Professional dress code that instills discipline and creates a sense of unity among students."),
    ("📚", "Library & Resources",
     "Extensive library with thousands of books, journals and digital resources for comprehensive learning.",
     "Extensive library with thousands of books, journals, and digital resources. A quiet environment for study and research with professional librarian assistance."),
    ("🎓", "Student Counseling",
     "Dedicated counselors to help students with academic guidance and personal development.",
     "Dedicated counselors to help students with academic guidance, career planning, and personal development. Regular sessions for stress management and goal setting."),
    ("🔬", "Science Labs",
     "Well-equipped physics, chemistry and biology labs with modern apparatus for hands-on experiments.",
     "Well-equipped physics, chemistry, and biology labs with modern apparatus and safety equipment. Students get hands-on experience conducting experiments under expert supervision."),
    ("⚽", "Sports Facilities",
     "Comprehensive sports facilities including courts and fields for physical development.",
     "Comprehensive sports facilities including basketball court, football field, and indoor games. Regular physical education classes and inter-school competitions."),
    ("📱", "Smart Classrooms",
     "Modern classrooms with projectors and smart boards for interactive learning.",
     "Modern classrooms equipped with projectors, smart boards, and audio-visual systems for interactive learning. Air-conditioned and well-ventilated spaces."),
    ("📡", "Wi-Fi Campus",
     "Complete campus Wi-Fi coverage for digital learning and online resources.",
     "Complete campus Wi-Fi coverage enabling students and teachers to access online resources and digital learning materials anytime."),
    ("🍽️", "Cafeteria",
     "Hygienic cafeteria serving nutritious meals and snacks.",
     "Hygienic cafeteria serving nutritious meals and snacks. Clean environment with seating capacity for students and staff. Regular health inspections maintained."),
    ("🚌", "Transportation",
     "Safe and reliable school bus service covering various routes across the city.",
     "Safe and reliable school bus service covering various routes across the city. Trained drivers and attendants ensure student safety during commute."),
    ("⚕️", "Medical Facility",
     "On-campus medical room with trained nurse for immediate health care.",
     "On-campus medical room with trained nurse for immediate health care. Regular health checkups and first aid facilities available."),
    ("🎨", "Art & Music Room",
     "Dedicated spaces for creative expression through art, music, and drama.",
     "Dedicated spaces for creative expression through art, music, and drama. Professional instructors guide students in developing their artistic talents."),
    ("🎭", "Auditorium",
     "Large auditorium with seating capacity of 500+ for events and cultural programs.",
     "Large auditorium with seating capacity of 500+ for events, seminars, and cultural programs. Equipped with modern sound and lighting systems."),
]

ACADEMICS = [
    ("ECD / Nursery", "ECD / Nursery",
     "Early Childhood Development program nurturing curiosity, creativity and social skills through play-based learning in a warm, caring environment.",
     "https://i.ibb.co/YTwWhYBf/IMG-20260803-WA0043.jpg",
     ["Play-based learning", "Social skill development", "Creative arts & crafts", "Phonics & early literacy"]),
    ("Basic Level", "Grade 1 to Grade 8",
     "Foundation years focusing on holistic development and learning through interactive methods, covering Grade 1 to Grade 8 as per Nepal's updated education structure.",
     "https://i.ibb.co/s9MQDZmn/basic.jpg",
     ["Activity-based learning", "Individual attention", "Science practicals", "Basic computer skills"]),
    ("Secondary Education", "Grade 9 to Grade 10",
     "Comprehensive preparation for SEE board examination and future academic pursuits.",
     "https://i.ibb.co/4RNfnpy2/secondary.jpg",
     ["SEE board preparation", "Advanced lab work", "Career counseling", "Project-based learning"]),
]

NOTICES = [
    (1, "Routine Page 1", "https://i.ibb.co/LzqBhQ2P/page-2.png"),
    (2, "Routine Page 2", "https://i.ibb.co/sp6ZSd82/page-3.png"),
    (3, "Routine Page 3", "https://i.ibb.co/gL9zz8p1/page-4.png"),
    (4, "Routine Page 4", "https://i.ibb.co/wN5tj2mb/page-5.png"),
]

STAFF = [
    ("smb", "School Management Committee", "Governing Body", None, "Management", "principal", "https://i.ibb.co/9HsQG2pY/School.png", 1),
    ("principal", "Basu Dev Dawadi", "School Principal", None, "Leadership", "principal", "https://i.ibb.co/Kz9gsdrM/princial.png", 2),
    ("vp", "Parvati Devi Adhikari", "Vice Principal", None, "Leadership", "vp", "https://i.ibb.co/0H8kSfN/vice-Principal.jpg", 3),
    ("accountant", "Shyam Bhakta Basu Shrestha", "Accountant", None, "Administration", "staff", "https://i.ibb.co/84GWJqcX/shyam-shrestha.png", 10),
    ("ecd", "Shova Lama", "ECD Incharge", None, "Academic", "coord", "https://i.ibb.co/gL1kBjHd/shova.jpg", 20),
    ("primary", "Kamala Devi Mainali", "Primary Incharge", None, "Academic", "coord", "https://i.ibb.co/YFvB46Fr/kamala.jpg", 21),
    ("lowersec", "Sumitra Sigdel", "Lower Secondary Incharge", None, "Academic", "coord", "https://i.ibb.co/27GcYNB9/sumitra-sigdel-low-sec-inc.jpg", 22),
    ("sec", "Rajan Kila Shrestha", "Secondary Level Coordinator", None, "Academic", "coord", "https://i.ibb.co/b5pZDvqb/rajan-kila.jpg", 23),
    ("help1", "Aakash Kumari", "School Helper", None, "Support", "staff", "https://i.ibb.co/k6wp12HZ/aakash-kumari.jpg", 30),
    ("help", "Manju Kami Sunar", "Kitchen Staff", None, "Support", "staff", "https://images.unsplash.com/photo-1556157382-97eda2d62296?w=120&h=120&fit=crop&crop=faces", 31),
    ("cook", "Bimala Budathoki", "Kitchen Staff", None, "Support", "staff", "https://images.unsplash.com/photo-1583394293214-28ded15ee548?w=120&h=120&fit=crop&crop=faces", 32),
    ("ecd1", "Kabita Dhungana", "Teacher", None, "ECD", "faculty", "https://i.ibb.co/zVQcDCJb/Kabita-Dhungana.jpg", 40),
    ("ecd2", "Nirmala Kumari Chaudhary", "ECD Aaya", None, "ECD", "faculty", "https://i.ibb.co/VpcvycX3/nirmala-kumari-chaudhary.jpg", 41),
    ("pf0", "Parvati Devi Adhikari", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/0H8kSfN/vice-Principal.jpg", 50),
    ("pf1", "Rohini Shilakar", "Nepal Bhasa Trainee", None, "Primary", "faculty", "https://i.ibb.co/jvJPQgcL/rohini-shilakar.jpg", 51),
    ("pf2", "Smjhana Dhungel", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/4RJKBydH/smjhana-Dhungel.jpg", 52),
    ("pf3", "Durga Devi Basnet", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/9kF84M0g/durga-devi-basnet.jpg", 53),
    ("pf4", "Mina Parajuli", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/Hfpq0xBR/mina-parajuli-2.jpg", 54),
    ("pf5", "Sunita Kumari Pahadi Dhakal", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/jZgRvMWv/sunita-kumari-pahadi-dhakal.jpg", 55),
    ("pf6", "Srijana Maharjan", "Nepal Bhasa Trainee", None, "Primary", "faculty", "https://i.ibb.co/CKL2RrBQ/srijana-maharjan.jpg", 56),
    ("pf7", "Shova Timalsina", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/SwpRmBF7/shova-timalsina.jpg", 57),
    ("pf8", "Prabhakar Neupane", "Teacher / Former-principal", None, "Primary", "faculty", "https://i.ibb.co/jZPjR65S/prabhakar-neupane.jpg", 58),
    ("pf9", "Ganga Prasain", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/m5v8sXHr/ganga-prasain.jpg", 59),
    ("pf10", "Badrika Devi Kafle", "Teacher", None, "Primary", "faculty", "https://i.ibb.co/4wNvW7pf/badrika-devi-Kafle.jpg", 60),
    ("ls1", "Rajan Kila", "Teacher", "Math", "LowerSec", "faculty", "https://i.ibb.co/b5pZDvqb/rajan-kila.jpg", 70),
    ("ls2", "Bhesraj Neupane", "Teacher", "Science", "LowerSec", "faculty", "https://i.ibb.co/FLXtd7QV/bhesraj-neupane.jpg", 71),
    ("ls3", "Dhurba Kumar Basnet Chhetri", "Teacher", "Social Studies", "LowerSec", "faculty", "https://i.ibb.co/21yd4X22/dhurba-kumar-basnet-chhetri.jpg", 72),
    ("ls4", "Jyotsana Khadka", "Teacher", "English", "LowerSec", "faculty", "https://i.ibb.co/21PnxNhq/jyotsana-khadka.jpg", 73),
    ("ls5", "Shrijana Budhathoki", "Teacher", "Nepali", "LowerSec", "faculty", "https://i.ibb.co/m5rtykpw/shrijana-budhathoki.png", 74),
    ("ls6", "Krisha Bhattarai", "Teacher", "Computer Science", "LowerSec", "faculty", "https://i.ibb.co/k6HX6RxW/krisha-bhattarai.jpg", 75),
    ("s0", "Basu Dev Dawadi", "Teacher", "Math", "Secondary", "faculty", "https://i.ibb.co/Kz9gsdrM/princial.png", 80),
    ("s2", "Seeta Basnet", "Teacher", "Social Studies", "Secondary", "faculty", "https://i.ibb.co/PvSx643x/seeta-basnet.jpg", 81),
    ("s1", "Prakash Bhattarai", "Teacher", "English", "Secondary", "faculty", "https://i.ibb.co/jtKkjQY/Prakash-bhattarai.jpg", 82),
    ("s4", "Hemalata Dangi", "Teacher", "Science", "Secondary", "faculty", "https://i.ibb.co/xS6qG7pL/hemalata-dangi-sec.jpg", 83),
]

NEWS = [
    {
        "slug": "see-farewell-program-2082",
        "title": "SEE Farewell Program 2082 Batch",
        "date_bs": "Jestha, 2083",
        "excerpt": "An emotional and memorable farewell program was organized to bid goodbye to the SEE 2082 batch students, celebrating their journey and wishing them success in their future endeavors.",
        "body": "Shree Siddeshwor Secondary School organized a heartfelt SEE Farewell Program in Jestha 2083 to bid goodbye to the graduating batch of 2082. The emotional event celebrated the journey of Grade 10 students with cultural performances, speeches, and award ceremonies recognizing achievements in academics, sports, and leadership. Teachers shared words of wisdom and encouragement while students expressed gratitude for the guidance and support they received. Juniors honored their seniors with special performances, and the program emphasized values of friendship, perseverance, and lifelong learning. As the SEE 2082 batch steps into their next chapter, the school wishes them success and reminds them they will always be part of the Siddeshwor family.",
        "cover": "https://i.ibb.co/RT86YvgS/IMG-20260803-WA0177.jpg",
        "images": [
            ["https://i.ibb.co/0pggL0wM/IMG-20260803-WA0111.jpg", "SEE Farewell Program 2082 Batch"],
            ["https://i.ibb.co/8nF17kt3/IMG-20260803-WA0112.jpg", "Students celebrating farewell"],
            ["https://i.ibb.co/KzVFT3m5/IMG-20260803-WA0118.jpg", "Farewell ceremony moments"],
            ["https://i.ibb.co/fYcN8tmb/IMG-20260803-WA0140.jpg", "Graduating students with teachers"],
            ["https://i.ibb.co/RT86YvgS/IMG-20260803-WA0177.jpg", "SEE 2082 batch farewell"],
            ["https://i.ibb.co/G4FVT5y0/IMG-20260803-WA0178.jpg", "Students enjoying farewell program"],
            ["https://i.ibb.co/p68VNXY7/IMG-20260803-WA0180.jpg", "Farewell celebration"],
            ["https://i.ibb.co/fzC1Xdz2/IMG-20260803-WA0181.jpg", "Students and teachers together"],
            ["https://i.ibb.co/35BTtq30/IMG-20260803-WA0182.jpg", "Memorable farewell moments"],
            ["https://i.ibb.co/zhL3qzBZ/IMG-20260803-WA0183.jpg", "Farewell program highlights"],
            ["https://i.ibb.co/zHNrtF02/IMG-20260803-WA0184.jpg", "Graduating students"],
            ["https://i.ibb.co/hxF5n4NG/IMG-20260803-WA0185.jpg", "Farewell ceremony"],
            ["https://i.ibb.co/KxYyN9wF/IMG-20260803-WA0186.jpg", "Students celebrating together"],
            ["https://i.ibb.co/bjP9v7Yt/IMG-20260803-WA0188.jpg", "Farewell event memories"],
            ["https://i.ibb.co/QvKxdSvH/IMG-20260803-WA0189.jpg", "SEE 2082 batch students"],
        ],
    },
    {
        "slug": "teachers-day-celebration-2083",
        "title": "Teacher's Day Celebration 2083",
        "date_bs": "Shrawan 13, 2083",
        "excerpt": "Shree Siddeshwor Secondary School celebrated Teacher's Day 2083 with great enthusiasm, honoring teachers for their invaluable contributions to education and student development.",
        "body": "On Shrawan 13, 2083 BS, Shree Siddeshwor Secondary School celebrated Teacher's Day with great enthusiasm and heartfelt appreciation for the dedicated educators who shape the future of our students. The celebration was filled with joy and gratitude as students, staff, and administration came together to honor the teaching community.",
        "cover": "https://i.ibb.co/V0RRPLL1/IMG-20260803-WA0044.jpg",
        "images": [["https://i.ibb.co/V0RRPLL1/IMG-20260803-WA0044.jpg", "Teacher's Day Celebration 2083"]],
    },
    {
        "slug": "teacher-appreciation-jestha-2083",
        "title": "Teacher Appreciation Patra for Best Results in Kathmandu Metropolitan City",
        "date_bs": "Jestha, 2083",
        "excerpt": "Teachers were honored with appreciation certificates recognizing their dedication and achievements in producing outstanding academic results in Kathmandu Metropolitan City.",
        "body": "Shree Siddeshwor Secondary School organized a Teacher Appreciation Certificate Distribution Program in Jestha 2083 to honor teachers for achieving outstanding results in Kathmandu Metropolitan City. Appreciation certificates (Patra) were presented to teachers for their exceptional dedication, hard work, and contributions to student development.",
        "cover": "https://i.ibb.co/MDGjpq5t/IMG-20260803-WA0133.jpg",
        "images": [
            ["https://i.ibb.co/MDGjpq5t/IMG-20260803-WA0133.jpg", "Teacher appreciation ceremony"],
            ["https://i.ibb.co/kgGcQNS9/IMG-20260803-WA0134.jpg", "Teachers receiving appreciation certificates"],
            ["https://i.ibb.co/ZRbMjkv8/IMG-20260803-WA0135.jpg", "Certificate distribution program"],
            ["https://i.ibb.co/bgsH2tjT/IMG-20260803-WA0136.jpg", "Honoring dedicated teachers"],
            ["https://i.ibb.co/PGnjBfJP/IMG-20260803-WA0137.jpg", "Recognition ceremony"],
        ],
    },
    {
        "slug": "school-picnic-godavari-2083",
        "title": "School Picnic to Godavari, Kathmandu",
        "date_bs": "Ashar 4, 2083",
        "excerpt": "Students and teachers enjoyed a memorable school picnic at the beautiful Godavari Botanical Garden in Kathmandu, filled with fun activities, nature exploration, and bonding.",
        "body": "On Ashar 4, 2083 BS, Shree Siddeshwor Secondary School organized a delightful school picnic to the picturesque Godavari Botanical Garden in Kathmandu. Students from various grades, along with teachers and staff, embarked on this exciting journey filled with joy, laughter, and memorable experiences.",
        "cover": "https://i.ibb.co/Mx1kQwDX/IMG-20260803-WA0102.jpg",
        "images": [
            ["https://i.ibb.co/hnFbN5L/IMG-20260803-WA0094.jpg", "Students enjoying the picnic at Godavari"],
            ["https://i.ibb.co/rGBWKd5G/IMG-20260803-WA0095.jpg", "Group activities and games"],
            ["https://i.ibb.co/Mx1kQwDX/IMG-20260803-WA0102.jpg", "Group photo at Godavari"],
            ["https://i.ibb.co/TMyczLcx/IMG-20260803-WA0097.jpg", "Students posing for photos"],
        ],
    },
    {
        "slug": "hamro-palo-10-years",
        "title": "Celebration of 10 Years of Hamro Palo",
        "date_bs": "Ashadh 27, 2083",
        "excerpt": "10 Years of Hamro Palo | A Decade of Believing in Girls — Celebrating Girls' Leadership, Learning, and Social Change.",
        "body": "Shree Siddeshwor Secondary School proudly participated in the grand celebration of 10 Years of Hamro Palo — A Decade of Believing in Girls. This milestone event celebrated a decade of empowering girls through leadership, learning, and social change.",
        "cover": "https://i.ibb.co/0ynjGf7f/IMG-20260801-WA0004.jpg",
        "images": [
            ["https://i.ibb.co/pGbK5PK/IMG-20260801-WA0000.jpg", "10 Years of Hamro Palo Celebration"],
            ["https://i.ibb.co/0ynjGf7f/IMG-20260801-WA0004.jpg", "Community gathering"],
            ["https://i.ibb.co/8qzz6Z0/IMG-20260801-WA0001.jpg", "Girls' Leadership Program"],
        ],
    },
    {
        "slug": "lions-club-cash-distribution",
        "title": "Lion's Club Cash Distribution",
        "date_bs": "Ashadh 23, 2083",
        "excerpt": "Lion's Club organized a cash distribution program at Shree Siddeshwor Secondary School, supporting students in need.",
        "body": "Shree Siddeshwor Secondary School was honored to host a Cash Distribution Program organized by Lion's Club. The program aimed to provide financial support to underprivileged and deserving students, helping them continue their education without financial burden.",
        "cover": "https://i.ibb.co/L3ZwFVm/IMG-20260801-WA0136.jpg",
        "images": [
            ["https://i.ibb.co/9RbMgWR/IMG-20260801-WA0135.jpg", "Lion's Club Cash Distribution Program"],
            ["https://i.ibb.co/L3ZwFVm/IMG-20260801-WA0136.jpg", "Students receiving financial assistance"],
            ["https://i.ibb.co/xKs4qsc2/IMG-20260801-WA0137.jpg", "School administration with Lion's Club representatives"],
        ],
    },
    {
        "slug": "award-distribution-sports-2083",
        "title": "Award Distribution Program for Sports Winner Students",
        "date_bs": "Ashadh 27, 2083",
        "excerpt": "Students are awarded by different prizes of sports like Scout hiking, ward chair person football tournament and other different events.",
        "body": "On 10th July 2026 (Ashadh 27, 2083 BS), Shree Siddeshwor Secondary School proudly organized an Award Distribution Program to honor students who excelled in various sports and extracurricular events. Students were awarded prizes for Scout hiking, the Ward Chairperson Football Tournament, and several other competitive events.",
        "cover": "https://i.ibb.co/cKkbBLWP/IMG-20260801-WA0045.jpg",
        "images": [
            ["https://i.ibb.co/1JfRs78n/IMG-20260801-WA0011.jpg", "Award Distribution Program"],
            ["https://i.ibb.co/cKkbBLWP/IMG-20260801-WA0045.jpg", "Proud students"],
            ["https://i.ibb.co/kVGrDDsT/IMG-20260801-WA0026.jpg", "Sports champions"],
            ["https://i.ibb.co/ym94sL9B/IMG-20260801-WA0018.jpg", "Football tournament winners"],
        ],
    },
]


def seed(reset: bool = False):
    init_db()
    with get_db() as conn:
        if reset:
            for table in [
                "subscribers", "contacts", "applications", "suggestions",
                "activity", "faqs", "hero_slides", "notices", "academics",
                "facilities", "staff", "news", "gallery", "sessions", "settings", "users",
            ]:
                conn.execute(f"DELETE FROM {table}")

        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO users (username, password_hash, name, role, created_at) VALUES (?,?,?,?,?)",
                ("admin", hash_password("Siddeshwor@2047"), "School Administrator", "admin", NOW),
            )

        if conn.execute("SELECT COUNT(*) FROM settings").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO settings (key, value) VALUES (?,?)",
                list(SETTINGS.items()),
            )

        if conn.execute("SELECT COUNT(*) FROM hero_slides").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO hero_slides (url, alt, sort_order) VALUES (?,?,?)",
                [(u, a, i) for i, (u, a) in enumerate(HERO)],
            )

        if conn.execute("SELECT COUNT(*) FROM facilities").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO facilities (icon, title, short_desc, long_desc, sort_order) VALUES (?,?,?,?,?)",
                [(ic, t, s, lg, i) for i, (ic, t, s, lg) in enumerate(FACILITIES)],
            )

        if conn.execute("SELECT COUNT(*) FROM academics").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO academics (title, tag, description, image, items, sort_order) VALUES (?,?,?,?,?,?)",
                [(t, tag, d, img, json.dumps(items), i) for i, (t, tag, d, img, items) in enumerate(ACADEMICS)],
            )

        if conn.execute("SELECT COUNT(*) FROM notices").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO notices (title, page_num, image, sort_order) VALUES (?,?,?,?)",
                [(title, n, img, n) for n, title, img in NOTICES],
            )

        if conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO staff (staff_key, name, role, subject, department, level, image, sort_order) VALUES (?,?,?,?,?,?,?,?)",
                STAFF,
            )

        if conn.execute("SELECT COUNT(*) FROM news").fetchone()[0] == 0:
            for item in NEWS:
                conn.execute(
                    """INSERT INTO news (slug, title, date_bs, date_ad, excerpt, body, cover, images, published, created_at)
                       VALUES (?,?,?,?,?,?,?,?,1,?)""",
                    (
                        item["slug"], item["title"], item["date_bs"], None,
                        item["excerpt"], item["body"], item["cover"],
                        json.dumps([{"url": u, "alt": a} for u, a in item["images"]]),
                        NOW,
                    ),
                )

        faqs = [
            ("Which grades do you offer?", "We offer education from Early Childhood Development (ECD / Nursery) through Grade 10 (SEE)."),
            ("What are the office hours?", "Sunday to Friday, 7:00 AM – 4:00 PM. The school is closed on Saturday."),
            ("How do I apply for admission?", "Fill the online admission form on the Apply page, or visit the school office at Shantinagar, New Baneshwor with the student and a parent/guardian."),
            ("Is transport available?", "Yes. A school bus service covers several routes across Kathmandu. Ask the office for the current route list."),
            ("What documents are needed?", "Birth certificate, previous school transfer certificate (if any), two passport photos, and a parent/guardian citizenship copy."),
            ("Who should I contact for information?", "Call 01-4622730, email mail@siddeshwor.edu.np, or speak with our Information Officer at the school."),
        ]
        if conn.execute("SELECT COUNT(*) FROM faqs").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO faqs (question, answer, sort_order) VALUES (?,?,?)",
                [(q, a, i) for i, (q, a) in enumerate(faqs)],
            )

    print("Database seeded at data/siddeshwor.db")


if __name__ == "__main__":
    import sys
    seed(reset="--reset" in sys.argv)
