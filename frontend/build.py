#!/usr/bin/env python3
"""Generate the full Siddeshwor School static website."""
from pathlib import Path

ROOT = Path(__file__).parent

def page(title, page_id, depth, main, extra_head=""):
    base = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="Shree Siddeshwor Secondary School is a leading educational institution dedicated to providing quality education and nurturing future leaders.">
  <link rel="icon" href="{base}assets/img/favicon.ico">
  <link rel="icon" href="{base}assets/img/SiddeshworLogo.png">
  <link rel="stylesheet" href="{base}assets/css/style.css">
  {extra_head}
</head>
<body data-base="{base}" data-page="{page_id}">
  <div class="page">
    <div id="site-header"></div>
    <main>{main}</main>
    <div id="site-footer"></div>
  </div>
  <script src="{base}assets/js/config.js"></script>
  <script src="{base}assets/js/main.js"></script>
</body>
</html>
"""

def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print("wrote", rel)

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
HERO_IMGS = [
    ("https://i.ibb.co/9DJpB0X/IMG-20260801-WA0138.jpg", "Siddeshwor School Building"),
    ("https://i.ibb.co/0p6vsq8R/IMG-20260801-WA0051.jpg", "Siddeshwor School"),
    ("https://i.ibb.co/39hhxtzv/IMG-20260801-WA0089.jpg", "Siddeshwor School"),
    ("https://i.ibb.co/kVGrDDsT/IMG-20260801-WA0026.jpg", "Siddeshwor School"),
]

FACILITIES = [
    ("💻", "Computer Education", "State-of-the-art computer labs with latest technology and software to prepare students for the digital age."),
    ("👔", "School Uniform", "Professional dress code that instills discipline and creates a sense of unity among students."),
    ("📚", "Library & Resources", "Extensive library with thousands of books, journals and digital resources for comprehensive learning."),
    ("🎓", "Student Counseling", "Dedicated counselors to help students with academic guidance and personal development."),
    ("🔬", "Science Labs", "Well-equipped physics, chemistry and biology labs with modern apparatus for hands-on experiments."),
    ("⚽", "Sports Facilities", "Comprehensive sports facilities including courts and fields for physical development."),
    ("📱", "Smart Classrooms", "Modern classrooms with projectors and smart boards for interactive learning."),
    ("📡", "Wi-Fi Campus", "Complete campus Wi-Fi coverage for digital learning and online resources."),
]

NEWS = [
    ("see-farewell-program-2082", "Jestha, 2083", "SEE Farewell Program 2082 Batch",
     "An emotional and memorable farewell program was organized to bid goodbye to the SEE 2082 batch students, celebrating their journey and wishing them success in their future endeavors.",
     "https://i.ibb.co/RT86YvgS/IMG-20260803-WA0177.jpg"),
    ("teachers-day-celebration-2083", "Shrawan 13, 2083", "Teacher's Day Celebration 2083",
     "Shree Siddeshwor Secondary School celebrated Teacher's Day 2083 with great enthusiasm, honoring teachers for their invaluable contributions to education and student development.",
     "https://i.ibb.co/V0RRPLL1/IMG-20260803-WA0044.jpg"),
    ("teacher-appreciation-jestha-2083", "Jestha, 2083", "Teacher Appreciation Patra for Best Results in Kathmandu Metropolitan City",
     "Teachers were honored with appreciation certificates recognizing their dedication and achievements in producing outstanding academic results in Kathmandu Metropolitan City.",
     "https://i.ibb.co/MDGjpq5t/IMG-20260803-WA0133.jpg"),
    ("school-picnic-godavari-2083", "Ashar 4, 2083", "School Picnic to Godavari, Kathmandu",
     "Students and teachers enjoyed a memorable school picnic at the beautiful Godavari Botanical Garden in Kathmandu, filled with fun activities, nature exploration, and bonding.",
     "https://i.ibb.co/Mx1kQwDX/IMG-20260803-WA0102.jpg"),
    ("hamro-palo-10-years", "Ashadh 27, 2083", "Celebration of 10 Years of Hamro Palo",
     "10 Years of Hamro Palo | A Decade of Believing in Girls — Celebrating Girls' Leadership, Learning, and Social Change.",
     "https://i.ibb.co/0ynjGf7f/IMG-20260801-WA0004.jpg"),
    ("lions-club-cash-distribution", "Ashadh 23, 2083", "Lion's Club Cash Distribution",
     "Lion's Club organized a cash distribution program at Shree Siddeshwor Secondary School, supporting students in need.",
     "https://i.ibb.co/L3ZwFVm/IMG-20260801-WA0136.jpg"),
    ("award-distribution-sports-2083", "Ashadh 27, 2083", "Award Distribution Program for Sports Winner Students",
     "Students are awarded by different prizes of sports like Scout hiking, ward chair person football tournament and other different events.",
     "https://i.ibb.co/cKkbBLWP/IMG-20260801-WA0045.jpg"),
]

hero_slides = "".join(
    f'<div class="hero-slide{" active" if i==0 else ""}"><img src="{src}" alt="{alt}"><div class="shade"></div></div>'
    for i,(src,alt) in enumerate(HERO_IMGS)
)
hero_dots = "".join(
    f'<button class="{"active" if i==0 else ""}" aria-label="Slide {i+1}"></button>'
    for i in range(len(HERO_IMGS))
)
fac_slides = "".join(
    f'''<div class="slide-item">
      <div class="fac-card">
        <div class="fac-emoji">{emo}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
        <a class="link-red" href="facilities/index.html">Read More →</a>
      </div>
    </div>'''
    for emo,title,desc in FACILITIES
)
news_slides = "".join(
    f'''<div class="slide-item">
      <a class="news-card" href="news/{slug}/index.html">
        <div class="thumb"><img src="{img}" alt="{title}"></div>
        <div class="body">
          <p class="small">{date}</p>
          <h3>{title}</h3>
          <p>{excerpt}</p>
          <span class="link-red">Read More →</span>
        </div>
      </a>
    </div>'''
    for slug,date,title,excerpt,img in NEWS
)

home_main = f'''
<section class="hero">
  {hero_slides}
  <div class="hero-copy">
    <div>
      <h2>Welcome To</h2>
      <h1>Siddeshwor School</h1>
      <p>Shree Siddeshwor Secondary School</p>
    </div>
  </div>
  <div class="dots">{hero_dots}</div>
</section>

<section class="section gray">
  <div class="container">
    <div class="center" style="margin-bottom:40px">
      <h2 class="h2">THE LEADING INSTITUTION IN SHANTINAGAR</h2>
    </div>
    <div class="grid-2">
      <div class="reveal">
        <p class="muted" style="margin-bottom:14px">Shree Siddeshwor Secondary School is a public school located in Shantinagar, New Baneshwor, Kathmandu Metropolitan City, Kathmandu district, within Bagmati Province. The school provides education from Early Childhood Development (ECD) to Grade 10.</p>
        <p class="muted" style="margin-bottom:14px">As per the 2081 IEMIS report published by the Center for Education and Human Resource Development, Siddeshwor Secondary School has 506 enrolled students. The school operates as a co-educational day school, welcoming students from nursery through Grade 10.</p>
        <p class="muted" style="margin-bottom:18px">With an ERO score of 72.58, SSN is committed to maintaining high educational standards and creating a supportive learning environment that helps every student discover their potential and build a strong foundation for their future.</p>
        <div class="stats-row">
          <div class="stat-card"><strong>Nursery–10</strong><span>Level</span></div>
          <div class="stat-card"><strong>506</strong><span>Total Students</span></div>
          <div class="stat-card"><strong>72.58</strong><span>ERO Score</span></div>
          <div class="stat-card"><strong>Co-ed / Day</strong><span>Status</span></div>
        </div>
        <a class="btn" href="about/index.html">Read More</a>
      </div>
      <div class="photo-frame reveal">
        <img src="https://i.ibb.co/9HsQG2pY/School.png" alt="Siddeshwar School Building">
      </div>
    </div>
  </div>
</section>

<section class="section white">
  <div class="container">
    <div class="center reveal" style="margin-bottom:36px"><h2 class="h2">ACADEMICS AT SIDDESHWOR</h2></div>
    <div class="grid-3">
      <a class="acad-card reveal" href="academics/index.html">
        <div class="thumb"><img src="https://i.ibb.co/YTwWhYBf/IMG-20260803-WA0043.jpg" alt="ECD / Nursery"></div>
        <div class="cap b1">ECD / Nursery</div>
      </a>
      <a class="acad-card reveal" href="academics/index.html">
        <div class="thumb"><img src="https://i.ibb.co/s9MQDZmn/basic.jpg" alt="Basic Level (1-8)"></div>
        <div class="cap b2">Basic Level (1-8)</div>
      </a>
      <a class="acad-card reveal" href="academics/index.html">
        <div class="thumb"><img src="https://i.ibb.co/4RNfnpy2/secondary.jpg" alt="Secondary (9-10)"></div>
        <div class="cap b3">Secondary (9-10)</div>
      </a>
    </div>
  </div>
</section>

<section class="mid-banner">
  <img src="https://i.ibb.co/rGBWKd5G/IMG-20260803-WA0095.jpg" alt="Students at SSN">
  <div class="shade"></div>
  <div class="copy">
    <div class="logo-circle"><img src="assets/img/SiddeshworLogo.png" alt="Logo"></div>
    <h2>WELCOME TO SIDDESHWOR</h2>
    <p>Building Future Leaders</p>
  </div>
</section>

<section class="section gray">
  <div class="container">
    <div class="center reveal" style="margin-bottom:32px"><h2 class="h2">SIDDESHWOR SCHOOL'S FACILITIES</h2></div>
    <div class="carousel-wrap reveal" data-carousel data-per="4">
      <div class="carousel"><div class="carousel-track">{fac_slides}</div></div>
      <button class="car-btn prev" aria-label="Previous"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>
      <button class="car-btn next" aria-label="Next"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>
    </div>
  </div>
</section>

<section class="section white">
  <div class="container">
    <div class="section-head reveal">
      <h2 class="h2" style="margin:0">LATEST NEWS</h2>
      <a class="link-red" href="news/index.html">View All News →</a>
    </div>
    <div class="carousel-wrap reveal" data-carousel data-per="4">
      <div class="carousel"><div class="carousel-track">{news_slides}</div></div>
      <button class="car-btn prev" aria-label="Previous"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>
      <button class="car-btn next" aria-label="Next"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>
    </div>
  </div>
</section>

<section class="section gray">
  <div class="container">
    <div class="officer reveal">
      <img src="https://i.ibb.co/1Gj2WDyG/information-officer.jpg" alt="Information Officer">
      <h3>Information Officer</h3>
      <p class="muted" style="margin-bottom:10px">Shree Siddeshwor Secondary School</p>
      <p class="muted">For any information or inquiries, please contact our Information Officer who will be happy to assist you with admissions, school programs, and general information.</p>
    </div>
  </div>
</section>
'''
write("index.html", page(
    "Shree Siddeshwor Secondary School - Dedicated to Excellence in Education",
    "home", 0, home_main
))

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
values = [
    ("📚","Excellence","Striving for the highest standards in education and student achievement"),
    ("🤝","Integrity","Upholding honesty, ethics, and moral values in all our actions"),
    ("💡","Innovation","Embracing modern teaching methods and continuous improvement"),
    ("❤️","Compassion","Creating a caring and supportive environment for all students"),
    ("🎯","Discipline","Fostering self-discipline and responsibility in our students"),
    ("🌟","Respect","Valuing diversity and treating everyone with dignity"),
    ("🚀","Growth","Encouraging personal and academic development for all"),
    ("🏆","Achievement","Celebrating success and motivating students to reach their potential"),
]
val_html = "".join(
    f'<div class="value-card"><div class="emo">{e}</div><h3>{t}</h3><p class="small">{d}</p></div>'
    for e,t,d in values
)
about_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1600&q=80" alt="Students at Siddeshwar School">
  <div class="shade"></div>
  <div class="copy"><h1>About Siddeshwar School</h1><p>Excellence in Secondary Education Since 2008</p></div>
</div>
<section class="section white">
  <div class="container">
    <p class="lead">Siddeshwar School stands as a beacon of quality education in Nepal, committed to nurturing young minds and preparing them for a bright future through academic excellence and character development.</p>
    <div class="circles">
      <div class="circle-stat"><div class="circle red"><span data-count="15" data-suffix="+">0+</span></div><h3>Years of Excellence</h3><p class="muted">Serving the community since 2008</p></div>
      <div class="circle-stat"><div class="circle blue"><span data-count="500" data-suffix="+">0+</span></div><h3>Successful Students</h3><p class="muted">Proud alumni across the nation</p></div>
      <div class="circle-stat"><div class="circle green"><span data-count="25" data-suffix="+">0+</span></div><h3>Expert Teachers</h3><p class="muted">Dedicated and qualified faculty</p></div>
    </div>
  </div>
</section>
<section class="section gray">
  <div class="container">
    <div class="grid-2">
      <div>
        <h2 class="h2">Our History</h2>
        <p class="muted" style="margin-bottom:14px">Siddeshwar School was established in 2008 with a vision to provide quality secondary education to students in Nepal. Founded by a group of dedicated educators and community leaders, our institution was born out of a commitment to create a learning environment that nurtures both academic excellence and moral values.</p>
        <p class="muted" style="margin-bottom:14px">Over the past 15 years, we have grown from a small institution to one of the most trusted secondary schools in the region. Our journey has been marked by consistent academic achievements, infrastructure development, and a growing reputation for producing well-rounded students.</p>
        <p class="muted">Today, Siddeshwar School stands as a testament to the power of quality education and the dedication of our teachers, students, and supporters who have contributed to our success.</p>
      </div>
      <div class="photo-frame"><img src="https://i.ibb.co/9HsQG2pY/School.png" alt="Siddeshwar School Building"></div>
    </div>
  </div>
</section>
<section class="section white">
  <div class="container">
    <div class="mv-grid">
      <div class="mv-card mission">
        <div class="mv-head"><div class="icon-round">⚡</div><h2>Our Mission</h2></div>
        <p class="muted">To provide comprehensive secondary education from Grade 1 to Grade 10 through innovative teaching methods, strong academic fundamentals, and character-building programs that prepare students for success in their SEE examinations and future academic pursuits. We are committed to creating lifelong learners who are confident, compassionate, and capable of contributing positively to society.</p>
      </div>
      <div class="mv-card vision">
        <div class="mv-head"><div class="icon-round">👁</div><h2>Our Vision</h2></div>
        <p class="muted">To be recognized as a leading secondary school that transforms students into dedicated, disciplined, and capable individuals who excel academically and are ready to face the challenges of higher education and life with confidence. We envision creating future leaders who uphold strong moral values and contribute meaningfully to the development of our nation.</p>
      </div>
    </div>
  </div>
</section>
<section class="section gray">
  <div class="container">
    <div class="center" style="margin-bottom:32px">
      <h2 class="h2">Our Core Values</h2>
      <p class="muted">The principles that guide everything we do</p>
    </div>
    <div class="grid-4">{val_html}</div>
  </div>
</section>
<section class="cta">
  <h2>Join Our Learning Community</h2>
  <p>Discover how Siddeshwar School can help your child achieve their full potential</p>
  <div class="cta-btns">
    <a class="btn white" href="../apply/index.html">Apply for Admission</a>
    <a class="btn outline" href="../contact/index.html">Contact Us</a>
  </div>
</section>
'''
write("about/index.html", page("About Us | Shree Siddeshwor Secondary School", "about", 1, about_main))

# ---------------------------------------------------------------------------
# ACADEMICS
# ---------------------------------------------------------------------------
progs = [
    ("https://i.ibb.co/YTwWhYBf/IMG-20260803-WA0043.jpg","ECD / Nursery","ECD / Nursery",
     "Early Childhood Development program nurturing curiosity, creativity and social skills through play-based learning in a warm, caring environment.",
     ["Play-based learning","Social skill development","Creative arts & crafts","Phonics & early literacy"]),
    ("https://i.ibb.co/s9MQDZmn/basic.jpg","Basic Level","Grade 1 to Grade 8",
     "Foundation years focusing on holistic development and learning through interactive methods, covering Grade 1 to Grade 8 as per Nepal's updated education structure.",
     ["Activity-based learning","Individual attention","Science practicals","Basic computer skills"]),
    ("https://i.ibb.co/4RNfnpy2/secondary.jpg","Secondary Education","Grade 9 to Grade 10",
     "Comprehensive preparation for SEE board examination and future academic pursuits.",
     ["SEE board preparation","Advanced lab work","Career counseling","Project-based learning"]),
]
prog_html = ""
for img,title,tag,desc,items in progs:
    lis = "".join(f'<li><span style="color:#c41e3a;margin-right:8px">✓</span>{it}</li>' for it in items)
    prog_html += f'''<div class="prog-card">
      <div class="thumb"><img src="{img}" alt="{title}"></div>
      <div class="pad">
        <h3>{title}</h3>
        <p class="tag">{tag}</p>
        <p class="muted">{desc}</p>
        <ul>{lis}</ul>
      </div>
    </div>'''

acad_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1600&q=80" alt="Academic Programs">
  <div class="shade"></div>
  <div class="copy"><h1>Our Academic Programs</h1><p>Quality Education at Every Level</p></div>
</div>
<section class="section gray">
  <div class="container">
    <div class="grid-3" style="max-width:1040px;margin:0 auto">{prog_html}</div>
  </div>
</section>
'''
write("academics/index.html", page("Academics | Shree Siddeshwor Secondary School", "academics", 1, acad_main))

# ---------------------------------------------------------------------------
# APPLY
# ---------------------------------------------------------------------------
grades = "".join(f'<option value="{g}">{"Nursery / ECD" if g=="Nursery" else "Grade "+g}</option>' for g in ["Nursery","1","2","3","4","5","6","7","8","9","10"])
apply_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1600&q=80" alt="Apply for Admission">
  <div class="shade"></div>
  <div class="copy"><h1>Apply for Admission</h1><p>Join the Siddeshwar Family</p></div>
</div>
<section class="section gray">
  <div class="container">
    <div class="form-card">
      <h2>Admission Form</h2>
      <p class="form-note">Fields marked with <span class="req">*</span> are required.</p>
      <form data-success="Thank you! Your admission application has been received. Our office will contact you shortly.">
        <p class="form-sec">Student Information</p>
        <div class="row-2">
          <div class="field"><label>First Name <span class="req">*</span></label><input type="text" required></div>
          <div class="field"><label>Last Name <span class="req">*</span></label><input type="text" required></div>
        </div>
        <div class="row-2" style="margin-top:12px">
          <div class="field"><label>Date of Birth <span class="req">*</span></label><input type="date" required></div>
          <div class="field"><label>Grade Applying For <span class="req">*</span></label>
            <select required><option value="">Select Grade</option>{grades}</select>
          </div>
        </div>
        <div class="field" style="margin-top:12px"><label>Previous School (if any)</label><input type="text"></div>
        <div style="border-top:1px solid #f3f4f6;margin-top:22px;padding-top:8px">
          <p class="form-sec">Parent / Guardian Information</p>
          <div class="row-2">
            <div class="field"><label>Full Name <span class="req">*</span></label><input type="text" required></div>
            <div class="field"><label>Relationship <span class="req">*</span></label>
              <select required><option value="">Select</option><option>Father</option><option>Mother</option><option>Guardian</option></select>
            </div>
          </div>
          <div class="row-2" style="margin-top:12px">
            <div class="field"><label>Contact Number <span class="req">*</span></label><input type="tel" required></div>
            <div class="field"><label>Email Address <span class="req">*</span></label><input type="email" required></div>
          </div>
          <div class="field" style="margin-top:12px"><label>Address <span class="req">*</span></label><textarea rows="2" required></textarea></div>
        </div>
        <div style="border-top:1px solid #f3f4f6;margin-top:22px;padding-top:16px">
          <div class="field"><label>Additional Information</label><textarea rows="3" placeholder="Any special requirements or additional information"></textarea></div>
        </div>
        <label class="check"><input type="checkbox" required> I agree to the terms and conditions and confirm that the information provided is accurate.</label>
        <button class="btn" type="submit" style="width:100%">Submit Application</button>
        <div class="alert"></div>
      </form>
    </div>
  </div>
</section>
'''
write("apply/index.html", page("Apply for Admission | Shree Siddeshwor Secondary School", "apply", 1, apply_main))

# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------
contact_main = '''
<div class="page-hero short">
  <img src="https://images.unsplash.com/photo-1423666639041-f56000c27a9a?w=1600&q=80" alt="Contact Us">
  <div class="shade dark"></div>
  <div class="copy"><h1>Contact Us</h1><p>We'd Love to Hear From You</p></div>
</div>
<section class="section white">
  <div class="container">
    <div class="contact-grid">
      <div>
        <h2 class="h2">Get In Touch</h2>
        <div style="display:flex;flex-direction:column;gap:20px">
          <div><h3>Address</h3><p class="muted">Shantinagar, New Baneshwor, Kathmandu</p></div>
          <div><h3>Phone</h3><p class="muted">01-4622730</p></div>
          <div><h3>Email</h3><p><a class="link-red" href="mailto:mail@siddeshwor.edu.np">mail@siddeshwor.edu.np</a></p></div>
          <div><h3>Office Hours</h3><p class="muted">Sunday - Friday: 7:00 AM - 4:00 PM</p><p class="muted">Saturday: Closed</p></div>
        </div>
      </div>
      <div>
        <h2 class="h2">Send Us a Message</h2>
        <form data-success="Message sent! We will get back to you soon.">
          <div class="field"><label>Full Name <span class="req">*</span></label><input type="text" required placeholder="Your name"></div>
          <div class="field" style="margin-top:12px"><label>Email <span class="req">*</span></label><input type="email" required placeholder="your@email.com"></div>
          <div class="field" style="margin-top:12px"><label>Phone</label><input type="tel" placeholder="Your phone number"></div>
          <div class="field" style="margin-top:12px"><label>Message <span class="req">*</span></label><textarea rows="5" required placeholder="Your message"></textarea></div>
          <button class="btn" type="submit" style="margin-top:14px">Send Message</button>
          <div class="alert"></div>
        </form>
      </div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <h2 class="h2">Find Us</h2>
    <div class="map-wrap">
      <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.3!2d85.3358!3d27.6942!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb199a06c2eaf9%3A0xc5f361ab580a1f6b!2sM8PV%2BPFX%2C%20Kathmandu%2044600!5e0!3m2!1sen!2snp!4v1700000000000!5m2!1sen!2snp" allowfullscreen loading="lazy" title="Shree Siddeshwor Secondary School Location"></iframe>
    </div>
  </div>
</section>
'''
write("contact/index.html", page("Contact Us | Shree Siddeshwor Secondary School", "contact", 1, contact_main))

# ---------------------------------------------------------------------------
# FACILITIES
# ---------------------------------------------------------------------------
FAC_FULL = [
    ("💻","Computer Education","State-of-the-art computer labs with latest technology and software to prepare students for the digital age. Each lab is equipped with modern computers, high-speed internet, and specialized software for various courses."),
    ("🔬","Science Laboratories","Well-equipped physics, chemistry, and biology labs with modern apparatus and safety equipment. Students get hands-on experience conducting experiments under expert supervision."),
    ("📚","Library & Resources","Extensive library with thousands of books, journals, and digital resources. A quiet environment for study and research with professional librarian assistance."),
    ("⚽","Sports Facilities","Comprehensive sports facilities including basketball court, football field, and indoor games. Regular physical education classes and inter-school competitions."),
    ("🎓","Student Counseling","Dedicated counselors to help students with academic guidance, career planning, and personal development. Regular sessions for stress management and goal setting."),
    ("📱","Smart Classrooms","Modern classrooms equipped with projectors, smart boards, and audio-visual systems for interactive learning. Air-conditioned and well-ventilated spaces."),
    ("🍽️","Cafeteria","Hygienic cafeteria serving nutritious meals and snacks. Clean environment with seating capacity for students and staff. Regular health inspections maintained."),
    ("🚌","Transportation","Safe and reliable school bus service covering various routes across the city. Trained drivers and attendants ensure student safety during commute."),
    ("⚕️","Medical Facility","On-campus medical room with trained nurse for immediate health care. Regular health checkups and first aid facilities available."),
    ("🎨","Art & Music Room","Dedicated spaces for creative expression through art, music, and drama. Professional instructors guide students in developing their artistic talents."),
    ("🎭","Auditorium","Large auditorium with seating capacity of 500+ for events, seminars, and cultural programs. Equipped with modern sound and lighting systems."),
    ("📡","Wi-Fi Campus","Complete campus Wi-Fi coverage enabling students and teachers to access online resources and digital learning materials anytime."),
]
fac_cards = "".join(
    f'''<div class="fac-big">
      <div class="bar"></div>
      <div class="pad">
        <div class="fac-ico">{e}</div>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>
    </div>''' for e,t,d in FAC_FULL
)
fac_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1600&q=80" alt="School Facilities">
  <div class="shade"></div>
  <div class="copy"><h1>Our Facilities</h1><p>World-Class Infrastructure for Excellence</p></div>
</div>
<section class="section gray">
  <div class="container">
    <p class="lead">Siddeshwar School provides state-of-the-art facilities to ensure comprehensive development of every student. Our infrastructure supports both academic excellence and extracurricular growth.</p>
    <div class="fac-grid">{fac_cards}</div>
  </div>
</section>
<section class="section white">
  <div class="container center">
    <h2 class="h2">Experience Our Campus</h2>
    <p class="lead">We invite prospective students and parents to visit our campus and experience our facilities firsthand. Schedule a campus tour to see how we create an environment that nurtures excellence.</p>
    <a class="btn" href="../contact/index.html">Schedule a Campus Tour</a>
  </div>
</section>
'''
write("facilities/index.html", page("Facilities | Shree Siddeshwor Secondary School", "facilities", 1, fac_main))

# ---------------------------------------------------------------------------
# WHY US
# ---------------------------------------------------------------------------
WHYS = [
    ("Experienced Faculty","Our highly qualified and experienced teachers are dedicated to providing personalized attention and quality education to every student."),
    ("Proven Track Record","Consistently excellent results in SEE board examinations with students securing top positions and distinctions year after year."),
    ("Holistic Development","Focus on overall personality development through academics, sports, arts, and cultural activities."),
    ("Modern Infrastructure","State-of-the-art facilities including smart classrooms, well-equipped labs, library, and sports facilities."),
    ("Individual Attention","Small class sizes ensure that each student receives personal attention and guidance from teachers."),
    ("Career Guidance","Comprehensive counseling and career guidance to help students make informed decisions about their future."),
    ("Value-Based Education","Strong emphasis on moral values, ethics, and character building alongside academic excellence."),
    ("Safe Environment","Secure and nurturing campus with CCTV surveillance, trained security staff, and strict safety protocols."),
]
why_items = "".join(
    f'''<div class="why-item">
      <div class="num">{i}</div>
      <div><h3>{t}</h3><p class="muted">{d}</p></div>
    </div>''' for i,(t,d) in enumerate(WHYS,1)
)
why_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1522661067900-ab829854a57f?w=1600&q=80" alt="Why Choose Siddeshwar School">
  <div class="shade"></div>
  <div class="copy"><h1>Why Choose Siddeshwar School?</h1><p>Committed to Excellence in Education</p></div>
</div>
<section class="section white">
  <div class="container">
    <div class="why-stats">
      <div class="center"><div class="n" data-count="15" data-suffix="+">0+</div><div>Years of Excellence</div></div>
      <div class="center"><div class="n" data-count="500" data-suffix="+">0+</div><div>Successful Students</div></div>
      <div class="center"><div class="n" data-count="100" data-suffix="%">0%</div><div>SEE Success Rate</div></div>
      <div class="center"><div class="n" data-count="25" data-suffix="+">0+</div><div>Expert Teachers</div></div>
    </div>
  </div>
</section>
<section class="section gray">
  <div class="container">
    <div class="center" style="margin-bottom:36px">
      <h2 class="h2">What Sets Us Apart</h2>
      <p class="lead">Siddeshwar School stands out as a premier educational institution dedicated to nurturing future leaders through quality education and holistic development.</p>
    </div>
    <div class="grid-2" style="max-width:1100px;margin:0 auto;align-items:stretch">{why_items}</div>
  </div>
</section>
<section class="section white">
  <div class="container">
    <div class="commit">
      <h2 class="h2 center">Our Commitment</h2>
      <p>At Siddeshwar School, we are committed to providing secondary education (Grade 1-10) that goes beyond textbooks. We believe in nurturing confident, compassionate, and capable students who are prepared to excel in their SEE examinations and beyond.</p>
      <p>Our curriculum is designed to build strong fundamentals, develop critical thinking, and foster problem-solving skills while maintaining strong emphasis on moral values and discipline.</p>
      <p>Join us in our mission to create well-rounded individuals who are ready for the challenges of higher education and life.</p>
    </div>
  </div>
</section>
<section class="cta">
  <h2>Ready to Join Our Community?</h2>
  <p>Take the first step towards a brighter future for your child.</p>
  <div class="cta-btns">
    <a class="btn white" href="../apply/index.html">Apply Now</a>
    <a class="btn outline" href="../contact/index.html">Contact Us</a>
  </div>
</section>
'''
write("why-us/index.html", page("Why Us? | Shree Siddeshwor Secondary School", "why-us", 1, why_main))

# ---------------------------------------------------------------------------
# FAMILY / ORG CHART
# ---------------------------------------------------------------------------
PEOPLE = [
    dict(id="smb", name="School Management Committee", role="Governing Body", image="https://i.ibb.co/9HsQG2pY/School.png", level="principal", department="Management"),
    dict(id="principal", name="Basu Dev Dawadi", role="School Principal", image="https://i.ibb.co/Kz9gsdrM/princial.png", level="principal"),
    dict(id="vp", name="Parvati Devi Adhikari", role="Vice Principal", image="https://i.ibb.co/0H8kSfN/vice-Principal.jpg", level="vp"),
    dict(id="accountant", name="Shyam Bhakta Basu Shrestha", role="Accountant", image="https://i.ibb.co/84GWJqcX/shyam-shrestha.png", level="staff", department="Administration"),
    dict(id="ecd", name="Shova Lama", role="ECD Incharge", image="https://i.ibb.co/gL1kBjHd/shova.jpg", level="coord", department="Academic"),
    dict(id="primary", name="Kamala Devi Mainali", role="Primary Incharge", image="https://i.ibb.co/YFvB46Fr/kamala.jpg", level="coord", department="Academic"),
    dict(id="lowersec", name="Sumitra Sigdel", role="Lower Secondary Incharge", image="https://i.ibb.co/27GcYNB9/sumitra-sigdel-low-sec-inc.jpg", level="coord", department="Academic"),
    dict(id="sec", name="Rajan Kila Shrestha", role="Secondary Level Coordinator", image="https://i.ibb.co/b5pZDvqb/rajan-kila.jpg", level="coord", department="Academic"),
    dict(id="help1", name="Aakash Kumari", role="School Helper", image="https://i.ibb.co/k6wp12HZ/aakash-kumari.jpg", level="staff", department="Support"),
    dict(id="help", name="Manju Kami Sunar", role="Kitchen Staff", image="https://images.unsplash.com/photo-1556157382-97eda2d62296?w=120&h=120&fit=crop&crop=faces", level="staff", department="Support"),
    dict(id="cook", name="Bimala Budathoki", role="Kitchen Staff", image="https://images.unsplash.com/photo-1583394293214-28ded15ee548?w=120&h=120&fit=crop&crop=faces", level="staff", department="Support"),
    dict(id="ecd1", name="Kabita Dhungana", role="Teacher", image="https://i.ibb.co/zVQcDCJb/Kabita-Dhungana.jpg", level="faculty", department="ECD"),
    dict(id="ecd2", name="Nirmala Kumari Chaudhary", role="ECD Aaya", image="https://i.ibb.co/VpcvycX3/nirmala-kumari-chaudhary.jpg", level="faculty", department="ECD"),
    dict(id="pf0", name="Parvati Devi Adhikari", role="Teacher", image="https://i.ibb.co/0H8kSfN/vice-Principal.jpg", level="faculty", department="Primary"),
    dict(id="pf1", name="Rohini Shilakar", role="Nepal Bhasa Trainee", image="https://i.ibb.co/jvJPQgcL/rohini-shilakar.jpg", level="faculty", department="Primary"),
    dict(id="pf2", name="Smjhana Dhungel", role="Teacher", image="https://i.ibb.co/4RJKBydH/smjhana-Dhungel.jpg", level="faculty", department="Primary"),
    dict(id="pf3", name="Durga Devi Basnet", role="Teacher", image="https://i.ibb.co/9kF84M0g/durga-devi-basnet.jpg", level="faculty", department="Primary"),
    dict(id="pf4", name="Mina Parajuli", role="Teacher", image="https://i.ibb.co/Hfpq0xBR/mina-parajuli-2.jpg", level="faculty", department="Primary"),
    dict(id="pf5", name="Sunita Kumari Pahadi Dhakal", role="Teacher", image="https://i.ibb.co/jZgRvMWv/sunita-kumari-pahadi-dhakal.jpg", level="faculty", department="Primary"),
    dict(id="pf6", name="Srijana Maharjan", role="Nepal Bhasa Trainee", image="https://i.ibb.co/CKL2RrBQ/srijana-maharjan.jpg", level="faculty", department="Primary"),
    dict(id="pf7", name="Shova Timalsina", role="Teacher", image="https://i.ibb.co/SwpRmBF7/shova-timalsina.jpg", level="faculty", department="Primary"),
    dict(id="pf8", name="Prabhakar Neupane", role="Teacher / Former-principal", image="https://i.ibb.co/jZPjR65S/prabhakar-neupane.jpg", level="faculty", department="Primary"),
    dict(id="pf9", name="Ganga Prasain", role="Teacher", image="https://i.ibb.co/m5v8sXHr/ganga-prasain.jpg", level="faculty", department="Primary"),
    dict(id="pf10", name="Badrika Devi Kafle", role="Teacher", image="https://i.ibb.co/4wNvW7pf/badrika-devi-Kafle.jpg", level="faculty", department="Primary"),
    dict(id="ls1", name="Rajan Kila", role="Teacher", subject="Math", image="https://i.ibb.co/b5pZDvqb/rajan-kila.jpg", level="faculty", department="LowerSec"),
    dict(id="ls2", name="Bhesraj Neupane", role="Teacher", subject="Science", image="https://i.ibb.co/FLXtd7QV/bhesraj-neupane.jpg", level="faculty", department="LowerSec"),
    dict(id="ls3", name="Dhurba Kumar Basnet Chhetri", role="Teacher", subject="Social Studies", image="https://i.ibb.co/21yd4X22/dhurba-kumar-basnet-chhetri.jpg", level="faculty", department="LowerSec"),
    dict(id="ls4", name="Jyotsana Khadka", role="Teacher", subject="English", image="https://i.ibb.co/21PnxNhq/jyotsana-khadka.jpg", level="faculty", department="LowerSec"),
    dict(id="ls5", name="Shrijana Budhathoki", role="Teacher", subject="Nepali", image="https://i.ibb.co/m5rtykpw/shrijana-budhathoki.png", level="faculty", department="LowerSec"),
    dict(id="ls6", name="Krisha Bhattarai", role="Teacher", subject="Computer Science", image="https://i.ibb.co/k6HX6RxW/krisha-bhattarai.jpg", level="faculty", department="LowerSec"),
    dict(id="s0", name="Basu Dev Dawadi", role="Teacher", subject="Math", image="https://i.ibb.co/Kz9gsdrM/princial.png", level="faculty", department="Secondary"),
    dict(id="s2", name="Seeta Basnet", role="Teacher", subject="Social Studies", image="https://i.ibb.co/PvSx643x/seeta-basnet.jpg", level="faculty", department="Secondary"),
    dict(id="s1", name="Prakash Bhattarai", role="Teacher", subject="English", image="https://i.ibb.co/jtKkjQY/Prakash-bhattarai.jpg", level="faculty", department="Secondary"),
    dict(id="s4", name="Hemalata Dangi", role="Teacher", subject="Science", image="https://i.ibb.co/xS6qG7pL/hemalata-dangi-sec.jpg", level="faculty", department="Secondary"),
]

def person_card(p):
    sub = f'<div class="sub">{p["subject"]}</div>' if p.get("subject") else ""
    return f'''<div class="person {p["level"]}">
      <img src="{p["image"]}" alt="{p["name"]}">
      <h4>{p["name"]}</h4>
      <div class="role">{p["role"]}</div>
      {sub}
    </div>'''

def people_by(*ids):
    m = {p["id"]: p for p in PEOPLE}
    return "".join(person_card(m[i]) for i in ids if i in m)

def people_dept(dept):
    return "".join(person_card(p) for p in PEOPLE if p.get("department")==dept)

family_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80" alt="Siddeshwor School Team">
  <div class="shade"></div>
  <div class="copy"><h1>Siddeshwor Family</h1><p>Meet Our Dedicated Team</p></div>
</div>
<div class="breadcrumb-bar"><div class="container"><a href="../index.html">Home</a> › <span>Administrative Department</span></div></div>
<div class="section white" style="padding-bottom:10px">
  <div class="container">
    <h2 class="h2" style="margin-bottom:4px">Administrative Department</h2>
    <p class="muted">Organizational Structure of Siddeshwor School</p>
  </div>
</div>
<section class="section gray" style="padding-top:20px">
  <div class="container">
    <div class="org-wrap">
      <h2 class="h2 center">ORGANIZATIONAL STRUCTURE CHART</h2>
      <div class="hierarchy">
        <div class="hier-row">{people_by("smb")}</div>
        <div class="connector"></div>
        <div class="hier-row">{people_by("principal")}</div>
        <div class="connector"></div>
        <div class="hier-row">{people_by("vp")}</div>
      </div>

      <h3 class="dept-title">Academic Coordinators</h3>
      <div class="people-grid">{people_by("ecd","primary","lowersec","sec")}</div>

      <h3 class="dept-title">Administration & Support</h3>
      <div class="people-grid">{people_by("accountant","help1","help","cook")}</div>

      <h3 class="dept-title">ECD Faculty</h3>
      <div class="people-grid">{people_dept("ECD")}</div>

      <h3 class="dept-title">Primary Faculty</h3>
      <div class="people-grid">{people_dept("Primary")}</div>

      <h3 class="dept-title">Lower Secondary Faculty</h3>
      <div class="people-grid">{people_dept("LowerSec")}</div>

      <h3 class="dept-title">Secondary Faculty</h3>
      <div class="people-grid">{people_dept("Secondary")}</div>

      <div class="legend">
        <span><i class="dot" style="background:#ff007f"></i> Principal</span>
        <span><i class="dot" style="background:#0066cc"></i> Vice Principal</span>
        <span><i class="dot" style="background:#10b981"></i> Coordinator</span>
        <span><i class="dot" style="background:#8b5cf6"></i> Staff</span>
        <span><i class="dot" style="background:#f59e0b"></i> Faculty</span>
      </div>
      <div style="margin-top:18px;padding:18px;background:#eff6ff;border-radius:12px;text-align:center;font-size:14px;color:#374151">
        <strong>Note:</strong> This organizational chart represents the administrative structure of Siddeshwor School. Each member plays a vital role in ensuring quality education and smooth operations.
      </div>
    </div>
  </div>
</section>
'''
write("family/index.html", page("Siddeshwor Family | Shree Siddeshwor Secondary School", "family", 1, family_main))

# ---------------------------------------------------------------------------
# NEWS LIST
# ---------------------------------------------------------------------------
news_tiles = "".join(
    f'''<a class="news-tile" href="{slug}/index.html">
      <div class="thumb"><img src="{img}" alt="{title}"></div>
      <div class="pad">
        <p class="date-red">{date}</p>
        <h3>{title}</h3>
        <p class="muted">{excerpt}</p>
        <span class="link-red">Read More →</span>
      </div>
    </a>'''
    for slug,date,title,excerpt,img in NEWS
)
pop = "".join(
    f'''<a class="pop-item" href="{slug}/index.html">
      <img src="{img}" alt="{title}">
      <h4>{title if len(title)<40 else title[:38]+"…"}</h4>
    </a>'''
    for slug,date,title,excerpt,img in NEWS[:3]
)
news_list_main = f'''
<div class="page-hero">
  <img src="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1600&q=80" alt="Latest News & Events">
  <div class="shade"></div>
  <div class="copy"><h1>Latest News & Events</h1><p>Stay Updated with Shree Siddeshwor Secondary School</p></div>
</div>
<section class="section gray">
  <div class="container">
    <div class="news-layout">
      <div class="news-list">{news_tiles}</div>
      <aside>
        <div class="side-card">
          <h2 style="margin-bottom:16px">Popular Posts</h2>
          {pop}
        </div>
        <div class="admit-card">
          <div class="logo"><img src="../assets/img/SiddeshworLogo.png" alt="Logo"></div>
          <h2>ADMISSION OPEN!</h2>
          <p style="margin:8px 0 14px">Academic Year 2082/83</p>
          <p style="font-size:14px;margin-bottom:18px">Enrolling students for ECD / Nursery through Grade 10. Limited seats available — secure your child's future at Shree Siddeshwor Secondary School today.</p>
          <a class="btn white" href="../apply/index.html">Apply Now</a>
        </div>
      </aside>
    </div>
  </div>
</section>
'''
write("news/index.html", page("News & Events | Shree Siddeshwor Secondary School", "news", 1, news_list_main))

# ---------------------------------------------------------------------------
# NEWS ARTICLES
# ---------------------------------------------------------------------------
ARTICLES = {
    "see-farewell-program-2082": {
        "date": "Jestha, 2083",
        "title": "SEE Farewell Program 2082 Batch",
        "body": "Shree Siddeshwor Secondary School organized a heartfelt SEE Farewell Program in Jestha 2083 to bid goodbye to the graduating batch of 2082. The emotional event celebrated the journey of Grade 10 students with cultural performances, speeches, and award ceremonies recognizing achievements in academics, sports, and leadership. Teachers shared words of wisdom and encouragement while students expressed gratitude for the guidance and support they received. Juniors honored their seniors with special performances, and the program emphasized values of friendship, perseverance, and lifelong learning. As the SEE 2082 batch steps into their next chapter, the school wishes them success and reminds them they will always be part of the Siddeshwor family.",
        "images": [
            ("https://i.ibb.co/0pggL0wM/IMG-20260803-WA0111.jpg","SEE Farewell Program 2082 Batch"),
            ("https://i.ibb.co/8nF17kt3/IMG-20260803-WA0112.jpg","Students celebrating farewell"),
            ("https://i.ibb.co/KzVFT3m5/IMG-20260803-WA0118.jpg","Farewell ceremony moments"),
            ("https://i.ibb.co/fYcN8tmb/IMG-20260803-WA0140.jpg","Graduating students with teachers"),
            ("https://i.ibb.co/RT86YvgS/IMG-20260803-WA0177.jpg","SEE 2082 batch farewell"),
            ("https://i.ibb.co/G4FVT5y0/IMG-20260803-WA0178.jpg","Students enjoying farewell program"),
            ("https://i.ibb.co/p68VNXY7/IMG-20260803-WA0180.jpg","Farewell celebration"),
            ("https://i.ibb.co/fzC1Xdz2/IMG-20260803-WA0181.jpg","Students and teachers together"),
            ("https://i.ibb.co/35BTtq30/IMG-20260803-WA0182.jpg","Memorable farewell moments"),
            ("https://i.ibb.co/zhL3qzBZ/IMG-20260803-WA0183.jpg","Farewell program highlights"),
            ("https://i.ibb.co/zHNrtF02/IMG-20260803-WA0184.jpg","Graduating students"),
            ("https://i.ibb.co/hxF5n4NG/IMG-20260803-WA0185.jpg","Farewell ceremony"),
            ("https://i.ibb.co/KxYyN9wF/IMG-20260803-WA0186.jpg","Students celebrating together"),
            ("https://i.ibb.co/bjP9v7Yt/IMG-20260803-WA0188.jpg","Farewell event memories"),
            ("https://i.ibb.co/QvKxdSvH/IMG-20260803-WA0189.jpg","SEE 2082 batch students"),
        ],
    },
    "teachers-day-celebration-2083": {
        "date": "Shrawan 13, 2083",
        "title": "Teacher's Day Celebration 2083",
        "body": "On Shrawan 13, 2083 BS, Shree Siddeshwor Secondary School celebrated Teacher's Day with great enthusiasm and heartfelt appreciation for the dedicated educators who shape the future of our students. The celebration was filled with joy and gratitude as students, staff, and administration came together to honor the teaching community. Students organized special programs including cultural performances, speeches, and presentations highlighting the profound impact teachers have on their lives. Teachers were greeted with warm wishes, flowers, and tokens of appreciation, emphasizing their crucial role not just as educators but as mentors, role models, and guides. The event reinforced the special bond between teachers and students, creating an atmosphere of mutual respect and appreciation while celebrating teaching as a noble calling that shapes minds, builds character, and transforms lives.",
        "images": [
            ("https://i.ibb.co/V0RRPLL1/IMG-20260803-WA0044.jpg","Teacher's Day Celebration 2083 at Shree Siddeshwor Secondary School"),
        ],
    },
    "teacher-appreciation-jestha-2083": {
        "date": "Jestha, 2083",
        "title": "Teacher Appreciation Patra for Best Results in Kathmandu Metropolitan City",
        "body": "Shree Siddeshwor Secondary School organized a Teacher Appreciation Certificate Distribution Program in Jestha 2083 to honor teachers for achieving outstanding results in Kathmandu Metropolitan City. In a special ceremony attended by school administration, students, and community members, appreciation certificates (Patra) were presented to teachers for their exceptional dedication, hard work, and intellectual contributions to student development and academic excellence. Each teacher was individually recognized for their specific achievements in producing excellent academic results, innovative teaching methods, student mentorship, and overall commitment to quality education. The program celebrated the passion and professionalism that teachers bring to the classroom every day, emphasizing their crucial role in building students' future success and maintaining the school's reputation for educational excellence in Kathmandu Metropolitan City.",
        "images": [
            ("https://i.ibb.co/MDGjpq5t/IMG-20260803-WA0133.jpg","Teacher appreciation ceremony"),
            ("https://i.ibb.co/kgGcQNS9/IMG-20260803-WA0134.jpg","Teachers receiving appreciation certificates"),
            ("https://i.ibb.co/ZRbMjkv8/IMG-20260803-WA0135.jpg","Certificate distribution program"),
            ("https://i.ibb.co/bgsH2tjT/IMG-20260803-WA0136.jpg","Honoring dedicated teachers"),
            ("https://i.ibb.co/PGnjBfJP/IMG-20260803-WA0137.jpg","Recognition ceremony"),
            ("https://i.ibb.co/JwhM7RKv/IMG-20260803-WA0138.jpg","Teachers with appreciation letters"),
            ("https://i.ibb.co/zWGcQfDW/IMG-20260803-WA0139.jpg","School administration honoring teachers"),
            ("https://i.ibb.co/fYcN8tmb/IMG-20260803-WA0140.jpg","Certificate presentation"),
            ("https://i.ibb.co/ksNm1Mz5/IMG-20260803-WA0141.jpg","Teachers gathering for ceremony"),
            ("https://i.ibb.co/WNG7bq58/IMG-20260803-WA0142.jpg","Appreciation program"),
            ("https://i.ibb.co/6R08g59p/IMG-20260803-WA0143.jpg","Teachers receiving recognition"),
            ("https://i.ibb.co/FLH1L37w/IMG-20260803-WA0144.jpg","Certificate distribution"),
            ("https://i.ibb.co/jvPNXX0Z/IMG-20260803-WA0145.jpg","Teachers honored for dedication"),
            ("https://i.ibb.co/qLB9b2m8/IMG-20260803-WA0146.jpg","Appreciation ceremony moments"),
            ("https://i.ibb.co/tMhJ925G/IMG-20260803-WA0147.jpg","Teachers with certificates"),
            ("https://i.ibb.co/Xx2xqPYW/IMG-20260803-WA0148.jpg","Recognition program"),
            ("https://i.ibb.co/Nn2bdbBN/IMG-20260803-WA0149.jpg","Teachers celebration"),
            ("https://i.ibb.co/zTKjZS7K/IMG-20260803-WA0150.jpg","Certificate ceremony"),
            ("https://i.ibb.co/xSMqnL5B/IMG-20260803-WA0151.jpg","Honoring teaching excellence"),
            ("https://i.ibb.co/7N4yrHG9/IMG-20260803-WA0152.jpg","Appreciation event"),
            ("https://i.ibb.co/4RFBkwkf/IMG-20260803-WA0153.jpg","Teachers with appreciation patra"),
            ("https://i.ibb.co/PZxFb82S/IMG-20260803-WA0154.jpg","Recognition ceremony highlights"),
            ("https://i.ibb.co/4gg6JXrD/IMG-20260803-WA0155.jpg","Teachers gathering"),
            ("https://i.ibb.co/ks7RFYrz/IMG-20260803-WA0156.jpg","Certificate presentation moments"),
            ("https://i.ibb.co/ZR8B6xcz/IMG-20260803-WA0157.jpg","Teachers honored"),
            ("https://i.ibb.co/sdk3FBBg/IMG-20260803-WA0158.jpg","Appreciation program event"),
            ("https://i.ibb.co/W9NcbyC/IMG-20260803-WA0159.jpg","Teachers with recognition"),
            ("https://i.ibb.co/CKxM4jYX/IMG-20260803-WA0160.jpg","Appreciation highlights"),
            ("https://i.ibb.co/CK78jWNR/IMG-20260803-WA0161.jpg","Teachers at ceremony"),
            ("https://i.ibb.co/RTv2YYmx/IMG-20260803-WA0162.jpg","Certificate moments"),
            ("https://i.ibb.co/9mpLWyZv/IMG-20260803-WA0163.jpg","Honoring teachers"),
            ("https://i.ibb.co/jvx4kdK4/IMG-20260803-WA0164.jpg","School ceremony"),
            ("https://i.ibb.co/Vp3W4x5D/IMG-20260803-WA0165.jpg","Teachers together"),
            ("https://i.ibb.co/27Ws25R1/IMG-20260803-WA0166.jpg","Recognition day"),
            ("https://i.ibb.co/gZzv1NFT/IMG-20260803-WA0167.jpg","Appreciation gathering"),
            ("https://i.ibb.co/b5hYs3kr/IMG-20260803-WA0168.jpg","Teachers honored at school"),
            ("https://i.ibb.co/fVj01px1/IMG-20260803-WA0169.jpg","Certificate event"),
            ("https://i.ibb.co/n8DzmvKv/IMG-20260803-WA0170.jpg","Teaching excellence"),
            ("https://i.ibb.co/v7W14z3/IMG-20260803-WA0171.jpg","School recognition"),
            ("https://i.ibb.co/fYRpNg2N/IMG-20260803-WA0172.jpg","Teachers celebration day"),
            ("https://i.ibb.co/JWz5pc00/IMG-20260803-WA0173.jpg","Patra distribution"),
            ("https://i.ibb.co/QvwZC8Sn/IMG-20260803-WA0174.jpg","Honoring faculty"),
            ("https://i.ibb.co/jPPqtn7y/IMG-20260803-WA0175.jpg","Appreciation close"),
        ],
    },
    "school-picnic-godavari-2083": {
        "date": "Ashar 4, 2083",
        "title": "School Picnic to Godavari, Kathmandu",
        "body": "On Ashar 4, 2083 BS, Shree Siddeshwor Secondary School organized a delightful school picnic to the picturesque Godavari Botanical Garden in Kathmandu. Students from various grades, along with teachers and staff, embarked on this exciting journey filled with joy, laughter, and memorable experiences. Godavari, known for its lush greenery, diverse plant species, and serene environment, provided the perfect setting for a day of fun and learning outside the classroom. Students enjoyed nature walks, explored the botanical garden, participated in group games, and bonded with their peers and teachers in a relaxed atmosphere. The picnic included recreational activities, team-building exercises, and opportunities for students to appreciate the beauty of nature and understand the importance of environmental conservation. Everyone savored delicious food, captured cherished moments through photographs, and created lasting memories. The event reinforced the school's commitment to holistic education, promoting not just academic excellence but also social interaction, physical activities, and appreciation for the natural world. It was a day full of smiles, adventures, and togetherness that strengthened the school community bond.",
        "images": [
            ("https://i.ibb.co/hnFbN5L/IMG-20260803-WA0094.jpg","Students enjoying the picnic at Godavari"),
            ("https://i.ibb.co/rGBWKd5G/IMG-20260803-WA0095.jpg","Group activities and games"),
            ("https://i.ibb.co/Xf78SnKw/IMG-20260803-WA0096.jpg","Exploring Godavari Botanical Garden"),
            ("https://i.ibb.co/TMyczLcx/IMG-20260803-WA0097.jpg","Students posing for photos"),
            ("https://i.ibb.co/R4kDymSQ/IMG-20260803-WA0098.jpg","Fun moments with friends"),
            ("https://i.ibb.co/SX1Rqc3m/IMG-20260803-WA0099.jpg","Nature walk in the garden"),
            ("https://i.ibb.co/zVn40Pp8/IMG-20260803-WA0100.jpg","Students and teachers together"),
            ("https://i.ibb.co/j9gkRvFZ/IMG-20260803-WA0101.jpg","Picnic activities"),
            ("https://i.ibb.co/Mx1kQwDX/IMG-20260803-WA0102.jpg","Group photo at Godavari"),
            ("https://i.ibb.co/jvqNQWkR/IMG-20260803-WA0103.jpg","Enjoying the scenic beauty"),
            ("https://i.ibb.co/dwK0hjpK/IMG-20260803-WA0104.jpg","Team building exercises"),
            ("https://i.ibb.co/tpCjv0Kd/IMG-20260803-WA0105.jpg","Students bonding with peers"),
            ("https://i.ibb.co/ZpP3QsP1/IMG-20260803-WA0106.jpg","Recreational activities"),
            ("https://i.ibb.co/x8jyXpsk/IMG-20260803-WA0107.jpg","Picnic fun and laughter"),
            ("https://i.ibb.co/mFgHLHj4/IMG-20260803-WA0108.jpg","Memorable moments"),
            ("https://i.ibb.co/nszngwcs/IMG-20260803-WA0109.jpg","School community at Godavari"),
        ],
    },
    "hamro-palo-10-years": {
        "date": "Ashadh 27, 2083",
        "title": "Celebration of 10 Years of Hamro Palo",
        "body": "Shree Siddeshwor Secondary School proudly participated in the grand celebration of 10 Years of Hamro Palo — A Decade of Believing in Girls. This milestone event celebrated a decade of empowering girls through leadership, learning, and social change. The program brought together students, teachers, parents, and community leaders to reflect on the journey of girls' education and the transformative impact of the Hamro Palo initiative. Students showcased their leadership skills, shared their experiences, and inspired the community with their stories of resilience and achievement. The school reaffirms its commitment to supporting girls' education and creating an inclusive environment where every girl can thrive.",
        "images": [
            ("https://i.ibb.co/pGbK5PK/IMG-20260801-WA0000.jpg","10 Years of Hamro Palo Celebration"),
            ("https://i.ibb.co/8qzz6Z0/IMG-20260801-WA0001.jpg","Girls' Leadership Program"),
            ("https://i.ibb.co/KpQ72Lx4/IMG-20260801-WA0002.jpg","Cultural performances"),
            ("https://i.ibb.co/LdGnbBpj/IMG-20260801-WA0003.jpg","Students showcasing their achievements"),
            ("https://i.ibb.co/0ynjGf7f/IMG-20260801-WA0004.jpg","Community gathering"),
            ("https://i.ibb.co/sS7d4W2/IMG-20260801-WA0005.jpg","A decade of believing in girls"),
            ("https://i.ibb.co/sdJrcvKh/IMG-20260801-WA0006.jpg","Girls' empowerment program"),
            ("https://i.ibb.co/3mQtfpr0/IMG-20260801-WA0009.jpg","Leadership and learning"),
            ("https://i.ibb.co/XrHL6v6S/IMG-20260801-WA0010.jpg","Celebrating social change"),
        ],
    },
    "lions-club-cash-distribution": {
        "date": "Ashadh 23, 2083",
        "title": "Lion's Club Cash Distribution",
        "body": "Shree Siddeshwor Secondary School was honored to host a Cash Distribution Program organized by Lion's Club. The program aimed to provide financial support to underprivileged and deserving students, helping them continue their education without financial burden. Representatives from Lion's Club personally handed over cash assistance to selected students in the presence of school administration, teachers, and parents. The school expresses heartfelt gratitude to Lion's Club for their generous contribution towards the education and welfare of our students. Such initiatives inspire the school community and motivate students to strive for excellence despite challenges.",
        "images": [
            ("https://i.ibb.co/9RbMgWR/IMG-20260801-WA0135.jpg","Lion's Club Cash Distribution Program"),
            ("https://i.ibb.co/L3ZwFVm/IMG-20260801-WA0136.jpg","Students receiving financial assistance"),
            ("https://i.ibb.co/xKs4qsc2/IMG-20260801-WA0137.jpg","School administration with Lion's Club representatives"),
        ],
    },
    "award-distribution-sports-2083": {
        "date": "Ashadh 27, 2083",
        "title": "Award Distribution Program for Sports Winner Students",
        "body": "On 10th July 2026 (Ashadh 27, 2083 BS), Shree Siddeshwor Secondary School proudly organized an Award Distribution Program to honor students who excelled in various sports and extracurricular events. Students were awarded prizes for their outstanding achievements in Scout hiking, the Ward Chairperson Football Tournament, and several other competitive events. The program celebrated the spirit of sportsmanship, teamwork, and dedication shown by our students throughout the year. School administration, teachers, parents, and community members gathered to cheer and appreciate the hard work and talent of our young champions. The school remains committed to nurturing not just academic excellence but also physical fitness and leadership through sports.",
        "images": [
            ("https://i.ibb.co/1JfRs78n/IMG-20260801-WA0011.jpg","Award Distribution Program"),
            ("https://i.ibb.co/9HFv9zML/IMG-20260801-WA0013.jpg","Sports winners"),
            ("https://i.ibb.co/7xKfTnxR/IMG-20260801-WA0014.jpg","Prize ceremony"),
            ("https://i.ibb.co/dJWybdbL/IMG-20260801-WA0016.jpg","Scout hiking winners"),
            ("https://i.ibb.co/ym94sL9B/IMG-20260801-WA0018.jpg","Football tournament winners"),
            ("https://i.ibb.co/JR2jtv2b/IMG-20260801-WA0019.jpg","Award ceremony"),
            ("https://i.ibb.co/3mdFsyvx/IMG-20260801-WA0021.jpg","Students receiving awards"),
            ("https://i.ibb.co/bg4zdSbt/IMG-20260801-WA0022.jpg","Proud achievers"),
            ("https://i.ibb.co/kVGrDDsT/IMG-20260801-WA0026.jpg","Sports champions"),
            ("https://i.ibb.co/zVdqCbs2/IMG-20260801-WA0029.jpg","Prize distribution"),
            ("https://i.ibb.co/HTKL8kZ6/IMG-20260801-WA0034.jpg","Award winners"),
            ("https://i.ibb.co/jvybVLKW/IMG-20260801-WA0035.jpg","Celebrating achievements"),
            ("https://i.ibb.co/0Rzq9Kzv/IMG-20260801-WA0036.jpg","Students with prizes"),
            ("https://i.ibb.co/nspgfhcm/IMG-20260801-WA0038.jpg","Sports event highlights"),
            ("https://i.ibb.co/KBwjFLk/IMG-20260801-WA0040.jpg","Ward chairperson football tournament"),
            ("https://i.ibb.co/bMgTxbCc/IMG-20260801-WA0041.jpg","Trophy presentation"),
            ("https://i.ibb.co/dwTkSdQm/IMG-20260801-WA0042.jpg","Sportsmanship"),
            ("https://i.ibb.co/gbGYfPzd/IMG-20260801-WA0044.jpg","Community support"),
            ("https://i.ibb.co/cKkbBLWP/IMG-20260801-WA0045.jpg","Proud students"),
            ("https://i.ibb.co/jkxrgPmm/IMG-20260801-WA0048.jpg","Award ceremony moments"),
            ("https://i.ibb.co/TDqs1drJ/IMG-20260801-WA0049.jpg","Prize winners"),
            ("https://i.ibb.co/h1dL9Zsq/IMG-20260801-WA0050.jpg","Celebrating together"),
            ("https://i.ibb.co/0p6vsq8R/IMG-20260801-WA0051.jpg","Sports achievements"),
            ("https://i.ibb.co/c7F73V9/IMG-20260801-WA0054.jpg","Student champions"),
            ("https://i.ibb.co/k25tWKCN/IMG-20260801-WA0056.jpg","Award distribution"),
            ("https://i.ibb.co/m1MvnQy/IMG-20260801-WA0062.jpg","Sports day memories"),
            ("https://i.ibb.co/rGtYwCsB/IMG-20260801-WA0064.jpg","Winners on stage"),
            ("https://i.ibb.co/RkCCSK1V/IMG-20260801-WA0065.jpg","Proud moments"),
            ("https://i.ibb.co/d41s8bPz/IMG-20260801-WA0067.jpg","Scout hiking award"),
            ("https://i.ibb.co/93td8cTg/IMG-20260801-WA0068.jpg","Football champions"),
            ("https://i.ibb.co/xqF3qj04/IMG-20260801-WA0072.jpg","Group celebration"),
            ("https://i.ibb.co/RTnx9bGx/IMG-20260801-WA0073.jpg","Award recipients"),
            ("https://i.ibb.co/xtffbbLj/IMG-20260801-WA0076.jpg","Ceremony highlights"),
            ("https://i.ibb.co/KpVrMXpy/IMG-20260801-WA0078.jpg","Students and teachers"),
            ("https://i.ibb.co/1G1KFqn4/IMG-20260801-WA0082.jpg","Joyful winners"),
            ("https://i.ibb.co/5hKdGX4m/IMG-20260801-WA0088.jpg","Sports excellence"),
            ("https://i.ibb.co/39hhxtzv/IMG-20260801-WA0089.jpg","Prize giving"),
            ("https://i.ibb.co/Hf8t9NCz/IMG-20260801-WA0096.jpg","Award program"),
            ("https://i.ibb.co/yn0T5CsY/IMG-20260801-WA0112.jpg","Winning moments"),
            ("https://i.ibb.co/HD6CVYxp/IMG-20260801-WA0115.jpg","Champions celebrated"),
            ("https://i.ibb.co/ZRfzDQxs/IMG-20260801-WA0128.jpg","Sports award ceremony"),
            ("https://i.ibb.co/L3ZwFVm/IMG-20260801-WA0136.jpg","Closing ceremony"),
        ],
    },
}

for slug, art in ARTICLES.items():
    gallery = "".join(
        f'''<a href="{src}" data-lb>
          <figure>
            <img src="{src}" alt="{alt}">
            <figcaption>{alt}</figcaption>
          </figure>
        </a>'''
        for src, alt in art["images"]
    )
    main = f'''
    <section class="section white">
      <div class="container">
        <div class="article">
          <p class="crumbs"><a href="../../index.html">Home</a> › <a href="../index.html">News</a> › {art["title"]}</p>
          <p class="date-red">{art["date"]}</p>
          <h1>{art["title"]}</h1>
          <p class="body">{art["body"]}</p>
          <h2 class="h2">Photo Gallery</h2>
          <div class="gallery">{gallery}</div>
          <p style="margin-top:28px"><a class="link-red" href="../index.html">← Back to All News</a></p>
        </div>
      </div>
    </section>
    '''
    write(f"news/{slug}/index.html", page(f'{art["title"]} | Shree Siddeshwor Secondary School', "news", 2, main))

# ---------------------------------------------------------------------------
# NOTICE
# ---------------------------------------------------------------------------
notice_main = '''
<div class="page-hero short">
  <img src="https://images.unsplash.com/photo-1568667256549-094345857637?w=1600&q=80" alt="Notice Board">
  <div class="shade"></div>
  <div class="copy"><h1>Notice Board</h1><p>Official Announcements — Shree Siddeshwor Secondary School</p></div>
</div>
<section class="section gray">
  <div class="container" style="max-width:900px">
    <div class="notice-banner">
      <span style="font-size:28px">📢</span>
      <div>
        <h2>School Routine</h2>
        <p style="color:#dbeafe;margin-top:4px">Below are the official school routine pages for Shree Siddeshwor Secondary School, listed in order. All students and staff are requested to follow the schedule accordingly.</p>
      </div>
    </div>
    <div id="noticeRoot">
    <!-- Fallback routine pages: replaced by /api/notices when the backend is reachable -->
    <div class="routine"><h3>Page 1</h3><img src="https://i.ibb.co/LzqBhQ2P/page-2.png" alt="Routine Page 1"></div>
    <div class="routine"><h3>Page 2</h3><img src="https://i.ibb.co/sp6ZSd82/page-3.png" alt="Routine Page 2"></div>
    <div class="routine"><h3>Page 3</h3><img src="https://i.ibb.co/gL9zz8p1/page-4.png" alt="Routine Page 3"></div>
    <div class="routine"><h3>Page 4</h3><img src="https://i.ibb.co/wN5tj2mb/page-5.png" alt="Routine Page 4"></div>
    </div>
  </div>
</section>
'''
write("notice/index.html", page("Notice Board | Shree Siddeshwor Secondary School", "notice", 1, notice_main))

# ---------------------------------------------------------------------------
# PRIVACY
# ---------------------------------------------------------------------------
privacy_main = '''
<div class="page-hero short">
  <img src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1600&q=80" alt="Privacy Policy">
  <div class="shade"></div>
  <div class="copy"><h1>Privacy Policy</h1><p>Shree Siddeshwor Secondary School</p></div>
</div>
<section class="section gray">
  <div class="container">
    <div class="prose">
      <p class="small" style="margin-bottom:18px">Last updated: Mangsir 2082</p>
      <p>Shree Siddeshwor Secondary School ("we", "our", or "the school") is committed to protecting the privacy of students, parents, staff, and visitors who interact with our website. This Privacy Policy explains what information we collect, how we use it, and how we protect it.</p>
      <h2>1. Information We Collect</h2>
      <p>We may collect personal information such as names, email addresses, phone numbers, and student details when you fill out admission forms, contact forms, or subscribe to our newsletter. We also collect non-personal data such as browser type, pages visited, and time spent on the site through standard web analytics tools.</p>
      <h2>2. How We Use Your Information</h2>
      <p>Information collected is used solely for school-related purposes including: processing admission applications, responding to inquiries, sending newsletters and school updates, improving our website and services, and communicating important school announcements to parents and students.</p>
      <h2>3. Data Sharing</h2>
      <p>We do not sell, trade, or rent your personal information to third parties. Information may be shared with government education authorities (such as CEHRD/ERO) as required by law, or with trusted service providers who assist in operating our website, provided they agree to keep the information confidential.</p>
      <h2>4. Cookies</h2>
      <p>Our website may use cookies to enhance your browsing experience. Cookies are small files stored on your device that help us understand how visitors use our site. You may choose to disable cookies through your browser settings, though this may affect some functionality of the website.</p>
      <h2>5. Children's Privacy</h2>
      <p>We are a school and understand the importance of protecting children's privacy. We do not knowingly collect personal information directly from children under 13 without parental consent. All student data is handled with strict confidentiality in accordance with applicable education laws.</p>
      <h2>6. Data Security</h2>
      <p>We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet is 100% secure, and we cannot guarantee absolute security.</p>
      <h2>7. Your Rights</h2>
      <p>You have the right to access, correct, or request deletion of your personal information held by us. To exercise these rights, please contact us at the details provided below. We will respond to your request within a reasonable timeframe.</p>
      <h2>8. Changes to This Policy</h2>
      <p>We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated date. We encourage you to review this policy periodically.</p>
      <h2>9. Contact Us</h2>
      <p>If you have any questions about this Privacy Policy, please contact us at: Shree Siddeshwor Secondary School, Shantinagar, New Baneshwor, Kathmandu. Email: mail@siddeshwor.edu.np | Phone: 01-4622730</p>
    </div>
  </div>
</section>
'''
write("privacy/index.html", page("Privacy Policy | Shree Siddeshwor Secondary School", "privacy", 1, privacy_main))

# ---------------------------------------------------------------------------
# SITEMAP
# ---------------------------------------------------------------------------
def slink(href, label):
    return f'<li><a href="{href}"><span class="bullet"></span>{label}</a></li>'

sitemap_main = f'''
<div class="page-hero short">
  <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?w=1600&q=80" alt="Sitemap">
  <div class="shade"></div>
  <div class="copy"><h1>Sitemap</h1><p>All pages of Shree Siddeshwor Secondary School</p></div>
</div>
<section class="section gray">
  <div class="container" style="max-width:1000px">
    <div class="site-cols">
      <div class="site-box">
        <h2>🏠 Main Pages</h2>
        <ul>
          {slink("../index.html","Home")}
          {slink("../about/index.html","About Us")}
          {slink("../why-us/index.html","Why Choose Us")}
          {slink("../contact/index.html","Contact Us")}
          {slink("../apply/index.html","Apply / Admission")}
        </ul>
      </div>
      <div class="site-box">
        <h2>📚 Academics</h2>
        <ul>
          {slink("../academics/index.html","Academics Overview")}
          {slink("../academics/index.html","ECD / Nursery")}
          {slink("../academics/index.html","Primary Level (1–5)")}
          {slink("../academics/index.html","Lower Secondary (6–8)")}
          {slink("../academics/index.html","Secondary (9–10)")}
        </ul>
      </div>
      <div class="site-box">
        <h2>🎓 School Life</h2>
        <ul>
          {slink("../facilities/index.html","Facilities")}
          {slink("../news/index.html","News & Events")}
          {slink("../family/index.html","Siddeshwor Family")}
          {slink("../notice/index.html","Notice Board")}
        </ul>
      </div>
      <div class="site-box">
        <h2>ℹ️ Information</h2>
        <ul>
          {slink("../privacy/index.html","Privacy Policy")}
          {slink("../sitemap/index.html","Sitemap")}
        </ul>
      </div>
    </div>
  </div>
</section>
'''
write("sitemap/index.html", page("Sitemap | Shree Siddeshwor Secondary School", "sitemap", 1, sitemap_main))

print("DONE")
