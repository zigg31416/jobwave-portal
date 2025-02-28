import streamlit as st
import streamlit_lottie as st_lottie
import requests
import json
from streamlit_option_menu import option_menu
from supabase import create_client
from streamlit_clerk_auth import authenticate

# Page Configuration
st.set_page_config(
    page_title="JobWave Portal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    css = """
    <style>
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #13293D, #006494);
        color: white;
    }
    
    .block-container {
        padding-top: 2rem;
    }
    
    /* Card styling */
    .card {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00A8E8, transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        50% { left: 100%; }
        100% { left: 100%; }
    }
    
    /* Custom styling for job cards */
    .job-card {
        border-radius: 10px;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        background-color: rgba(255, 255, 255, 0.15);
    }
    
    .job-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
    }
    
    .company-name {
        font-size: 1.1rem;
        color: #00A8E8;
        margin-bottom: 0.5rem;
    }
    
    .job-details {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .detail-item {
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        background-color: rgba(0, 168, 232, 0.2);
        font-size: 0.8rem;
    }
    
    .job-description {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }
    
    .apply-button {
        background-color: #00A8E8;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .apply-button:hover {
        background-color: #0077B6;
    }
    
    /* Search and filter styling */
    .search-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00A8E8;
        box-shadow: 0 0 0 1px #00A8E8;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    
    /* Stats counter styling */
    .stat-counter {
        text-align: center;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .counter-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00A8E8;
        margin-bottom: 0.5rem;
    }
    
    .counter-label {
        font-size: 1rem;
        color: white;
    }
    
    /* Dashboard stats */
    .dashboard-stat {
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        text-align: center;
        height: 100%;
    }
    
    .dashboard-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00A8E8;
    }
    
    .dashboard-label {
        font-size: 1rem;
        color: white;
        opacity: 0.8;
    }
    
    /* Animation for cards */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease forwards;
    }
    
    /* Custom styling for specific elements */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF, #00A8E8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 3rem;
    }
    
    /* Profile section styling */
    .profile-header {
        display: flex;
        align-items: center;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
    
    .profile-picture {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #00A8E8;
    }
    
    .profile-info {
        margin-left: 1.5rem;
    }
    
    .profile-name {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    
    .profile-role {
        color: #00A8E8;
        font-size: 1rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Connect to Supabase
@st.cache_resource
def init_supabase():
    supabase_url = st.secrets.get("SUPABASE_URL", "your_supabase_url")
    supabase_key = st.secrets.get("SUPABASE_KEY", "your_supabase_key")
    return create_client(supabase_url, supabase_key)

# Initialize Supabase client
supabase = init_supabase()

# Apply custom CSS
load_css()

# Authenticate user with Clerk
user = authenticate()

if user:
    # User is authenticated
    st.session_state.user_id = user.get("id")
    st.session_state.user_email = user.get("email_addresses", [{}])[0].get("email_address", "")
    st.session_state.user_name = user.get("first_name", "") + " " + user.get("last_name", "")
    st.session_state.user_role = user.get("public_metadata", {}).get("role", "jobseeker")
    
    # Create sidebar navigation
    with st.sidebar:
        # Logo and app name
        st.markdown("<h1 style='text-align: center; color: #00A8E8;'>JobWave</h1>", unsafe_allow_html=True)
        
        # Load a Lottie animation for the sidebar
        lottie_sidebar = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kkflmtur.json")
        if lottie_sidebar:
            st_lottie.st_lottie(lottie_sidebar, height=200)
        
        # Navigation menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Home", 
                "Jobs", 
                "Companies", 
                "Applications" if st.session_state.user_role == "jobseeker" else "Dashboard", 
                "Profile"
            ],
            icons=["house", "briefcase", "building", "list-check", "person"],
            default_index=0,
        )
        
        st.markdown("---")
        st.markdown(f"<div style='text-align: center;'>Logged in as <br/><b>{st.session_state.user_name}</b><br/><i>({st.session_state.user_role})</i></div>", unsafe_allow_html=True)
        
        # Logout button
        if st.button("Logout"):
            # Reset session state and redirect to login
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content based on navigation selection
    if selected == "Home":
        # Hero section with animation
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<h1 class='main-title'>Find Your Dream Job</h1>", unsafe_allow_html=True)
            st.markdown("<p class='subtitle'>Discover opportunities that match your skills and ambitions</p>", unsafe_allow_html=True)
            
            # Quick search
            st.markdown("<div class='search-container'>", unsafe_allow_html=True)
            search_term = st.text_input("Search for jobs", placeholder="Job title, company, or keywords")
            col1_1, col1_2, col1_3 = st.columns(3)
            
            with col1_1:
                location = st.selectbox("Location", ["Any Location", "Remote", "USA", "Europe", "Asia", "Other"])
            
            with col1_2:
                job_type = st.selectbox("Job Type", ["Any Type", "Full-time", "Part-time", "Contract", "Internship"])
            
            with col1_3:
                experience = st.selectbox("Experience", ["Any Level", "Entry Level", "Mid Level", "Senior", "Executive"])
            
            if st.button("Search Jobs", use_container_width=True):
                st.success("Redirecting to Jobs page with your search criteria")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # Lottie animation
            lottie_url = "https://assets3.lottiefiles.com/packages/lf20_nehbumrv.json"
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie.st_lottie(lottie_json, height=400)
        
        # Stats counters
        st.markdown("<h2 style='text-align: center; margin: 3rem 0 2rem 0;'>JobWave in Numbers</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='stat-counter'>
                <div class='counter-value'>5000+</div>
                <div class='counter-label'>Active Jobs</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='stat-counter'>
                <div class='counter-value'>2M+</div>
                <div class='counter-label'>Job Seekers</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='stat-counter'>
                <div class='counter-value'>10K+</div>
                <div class='counter-label'>Companies</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class='stat-counter'>
                <div class='counter-value'>85%</div>
                <div class='counter-label'>Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Featured jobs section
        st.markdown("<h2 style='text-align: center; margin: 3rem 0 2rem 0;'>Featured Jobs</h2>", unsafe_allow_html=True)
        
        # Get featured jobs from Supabase (placeholder - would be actual Supabase query)
        # featured_jobs = supabase.table("jobs").select("*").eq("featured", True).limit(4).execute()
        
        # Sample featured jobs for demonstration
        featured_jobs = [
            {
                "title": "Senior Full Stack Developer", 
                "company": "TechNova Inc.",
                "location": "Remote",
                "job_type": "Full-time",
                "salary": "$120K - $150K",
                "description": "Join our team to build innovative solutions for enterprise clients."
            },
            {
                "title": "UX/UI Designer", 
                "company": "CreativeMinds",
                "location": "New York, USA",
                "job_type": "Full-time",
                "salary": "$90K - $110K",
                "description": "We're looking for a talented designer to create beautiful interfaces."
            },
            {
                "title": "Data Scientist", 
                "company": "DataFlow Analytics",
                "location": "San Francisco, USA",
                "job_type": "Full-time",
                "salary": "$130K - $160K",
                "description": "Build ML models and analyze large datasets to extract valuable insights."
            },
            {
                "title": "DevOps Engineer", 
                "company": "CloudSphere",
                "location": "Remote",
                "job_type": "Contract",
                "salary": "$100K - $130K",
                "description": "Improve our cloud infrastructure and implement CI/CD pipelines."
            }
        ]
        
        # Display featured jobs in a grid
        col1, col2 = st.columns(2)
        
        for i, job in enumerate(featured_jobs):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class='job-card animated' style='animation-delay: {i*0.1}s'>
                    <div class='job-title'>{job["title"]}</div>
                    <div class='company-name'>{job["company"]}</div>
                    <div class='job-details'>
                        <span class='detail-item'>{job["location"]}</span>
                        <span class='detail-item'>{job["job_type"]}</span>
                        <span class='detail-item'>{job["salary"]}</span>
                    </div>
                    <div class='job-description'>{job["description"]}</div>
                    <button class='apply-button'>View Details</button>
                </div>
                """, unsafe_allow_html=True)
                
    elif selected == "Jobs":
        st.markdown("<h1 class='main-title'>Job Listings</h1>", unsafe_allow_html=True)
        
        # Search and filter section
        st.markdown("<div class='search-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input("Search jobs", placeholder="Job title, skills, or keywords")
        
        with col2:
            sort_by = st.selectbox("Sort by", ["Newest First", "Salary: High to Low", "Relevance", "Company Rating"])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            location = st.selectbox("Location", ["Any Location", "Remote", "USA", "Europe", "Asia", "Other"])
        
        with col2:
            job_type = st.selectbox("Job Type", ["Any Type", "Full-time", "Part-time", "Contract", "Internship"])
        
        with col3:
            experience = st.selectbox("Experience Level", ["Any Level", "Entry Level", "Mid Level", "Senior", "Executive"])
        
        with col4:
            salary = st.selectbox("Salary Range", ["Any Range", "Under $50K", "$50K - $100K", "$100K - $150K", "Over $150K"])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Get jobs from Supabase (placeholder - would be actual Supabase query)
        # jobs = supabase.table("jobs").select("*").execute()
        
        # Sample jobs for demonstration
        jobs = [
            {
                "title": "Senior Full Stack Developer", 
                "company": "TechNova Inc.",
                "location": "Remote",
                "job_type": "Full-time",
                "salary": "$120K - $150K",
                "posted": "2 days ago",
                "description": "Join our team to build innovative solutions for enterprise clients using React, Node.js, and AWS."
            },
            {
                "title": "UX/UI Designer", 
                "company": "CreativeMinds",
                "location": "New York, USA",
                "job_type": "Full-time",
                "salary": "$90K - $110K",
                "posted": "5 days ago",
                "description": "We're looking for a talented designer to create beautiful interfaces. Experience with Figma and design systems required."
            },
            {
                "title": "Data Scientist", 
                "company": "DataFlow Analytics",
                "location": "San Francisco, USA",
                "job_type": "Full-time",
                "salary": "$130K - $160K",
                "posted": "1 week ago",
                "description": "Build ML models and analyze large datasets to extract valuable insights. Strong Python and statistics skills required."
            },
            {
                "title": "DevOps Engineer", 
                "company": "CloudSphere",
                "location": "Remote",
                "job_type": "Contract",
                "salary": "$100K - $130K",
                "posted": "2 weeks ago",
                "description": "Improve our cloud infrastructure and implement CI/CD pipelines. Experience with Kubernetes and AWS required."
            },
            {
                "title": "Product Manager", 
                "company": "InnovateCorp",
                "location": "Chicago, USA",
                "job_type": "Full-time",
                "salary": "$110K - $140K",
                "posted": "3 days ago",
                "description": "Lead product development from concept to launch. Strong communication and analytical skills required."
            },
            {
                "title": "Frontend Developer", 
                "company": "WebWizards",
                "location": "Berlin, Germany",
                "job_type": "Full-time",
                "salary": "€60K - €80K",
                "posted": "1 day ago",
                "description": "Create responsive and interactive web applications using modern JavaScript frameworks like React or Vue."
            },
            {
                "title": "AI Research Scientist", 
                "company": "Neural Dynamics",
                "location": "Remote",
                "job_type": "Full-time",
                "salary": "$140K - $180K",
                "posted": "4 days ago",
                "description": "Conduct cutting-edge research in natural language processing and develop novel ML algorithms."
            }
        ]
        
        # Display jobs
        for i, job in enumerate(jobs):
            st.markdown(f"""
            <div class='job-card animated' style='animation-delay: {i*0.1}s'>
                <div class='job-title'>{job["title"]}</div>
                <div class='company-name'>{job["company"]}</div>
                <div class='job-details'>
                    <span class='detail-item'>{job["location"]}</span>
                    <span class='detail-item'>{job["job_type"]}</span>
                    <span class='detail-item'>{job["salary"]}</span>
                    <span class='detail-item'>Posted: {job["posted"]}</span>
                </div>
                <div class='job-description'>{job["description"]}</div>
                <button class='apply-button'>Apply Now</button>
            </div>
            """, unsafe_allow_html=True)
            
    elif selected == "Companies":
        st.markdown("<h1 class='main-title'>Top Companies</h1>", unsafe_allow_html=True)
        
        # Search and filter
        search_company = st.text_input("Search companies", placeholder="Company name or industry")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            industry = st.selectbox("Industry", ["All Industries", "Technology", "Healthcare", "Finance", "Education", "Retail"])
        
        with col2:
            company_size = st.selectbox("Company Size", ["Any Size", "Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1000+)"])
        
        with col3:
            sort_companies = st.selectbox("Sort By", ["Rating", "Most Jobs", "Newest", "Alphabetical"])
        
        # Get companies from Supabase (placeholder - would be actual Supabase query)
        # companies = supabase.table("companies").select("*").execute()
        
        # Sample companies for demonstration
        companies = [
            {
                "name": "TechNova Inc.",
                "industry": "Technology",
                "location": "San Francisco, USA",
                "size": "Medium (201-1000)",
                "rating": "4.8/5",
                "description": "A leading software development company specializing in enterprise solutions.",
                "open_jobs": 15
            },
            {
                "name": "DataFlow Analytics",
                "industry": "Technology",
                "location": "New York, USA",
                "size": "Small (51-200)",
                "rating": "4.6/5",
                "description": "Data science and analytics company helping businesses leverage their data.",
                "open_jobs": 8
            },
            {
                "name": "CloudSphere",
                "industry": "Technology",
                "location": "Seattle, USA",
                "size": "Large (1000+)",
                "rating": "4.5/5",
                "description": "Cloud infrastructure and services provider with global presence.",
                "open_jobs": 23
            },
            {
                "name": "HealthPlus",
                "industry": "Healthcare",
                "location": "Boston, USA",
                "size": "Large (1000+)",
                "rating": "4.4/5",
                "description": "Healthcare technology company improving patient care through innovation.",
                "open_jobs": 12
            },
            {
                "name": "CreativeMinds",
                "industry": "Design",
                "location": "New York, USA",
                "size": "Small (51-200)",
                "rating": "4.7/5",
                "description": "Award-winning design agency creating digital experiences for global brands.",
                "open_jobs": 5
            },
            {
                "name": "GreenEnergy Solutions",
                "industry": "Energy",
                "location": "Austin, USA",
                "size": "Medium (201-1000)",
                "rating": "4.3/5",
                "description": "Sustainable energy company developing renewable energy technologies.",
                "open_jobs": 9
            }
        ]
        
        # Display companies in a grid
        col1, col2 = st.columns(2)
        
        for i, company in enumerate(companies):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class='card animated' style='animation-delay: {i*0.1}s'>
                    <h2>{company["name"]}</h2>
                    <div style='margin-bottom: 1rem;'>
                        <span style='color: #00A8E8;'>{company["industry"]}</span> | {company["location"]} | {company["size"]}
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 1rem;'>
                        <span>⭐ {company["rating"]}</span>
                        <span>{company["open_jobs"]} open positions</span>
                    </div>
                    <p>{company["description"]}</p>
                    <button class='apply-button' style='width: 100%;'>View Company</button>
                </div>
                """, unsafe_allow_html=True)
                
    elif selected == "Applications" and st.session_state.user_role == "jobseeker":
        st.markdown("<h1 class='main-title'>My Applications</h1>", unsafe_allow_html=True)
        
        # Tabs for different application statuses
        tab1, tab2, tab3, tab4 = st.tabs(["All Applications", "In Progress", "Interviews", "Rejected"])
        
        # Get applications from Supabase (placeholder - would be actual Supabase query)
        # applications = supabase.table("applications").select("*").eq("user_id", st.session_state.user_id).execute()
        
        # Sample applications for demonstration
        applications = [
            {
                "job_title": "Senior Full Stack Developer",
                "company": "TechNova Inc.",
                "applied_date": "2023-02-15",
                "status": "Interview Scheduled",
                "next_step": "Technical Interview on March 5, 2023"
            },
            {
                "job_title": "UX/UI Designer",
                "company": "CreativeMinds",
                "applied_date": "2023-02-10",
                "status": "Application Review",
                "next_step": "Waiting for feedback"
            },
            {
                "job_title": "Product Manager",
                "company": "InnovateCorp",
                "applied_date": "2023-02-01",
                "status": "Rejected",
                "next_step": "Try other opportunities"
            },
            {
                "job_title": "Frontend Developer",
                "company": "WebWizards",
                "applied_date": "2023-02-18",
                "status": "Application Submitted",
                "next_step": "Waiting for review"
            }
        ]
        
        # All Applications tab
        with tab1:
            for app in applications:
                status_color = "#00A8E8" if app["status"] == "Interview Scheduled" else "#FFA500" if app["status"] == "Application Review" or app["status"] == "Application Submitted" else "#FF6347"
                
                st.markdown(f"""
                <div class='card animated'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                        <h3 style='margin: 0;'>{app["job_title"]}</h3>
                        <span style='color: {status_color}; font-weight: 600;'>{app["status"]}</span>
                    </div>
                    <div style='margin-bottom: 0.5rem;'>{app["company"]} | Applied on {app["applied_date"]}</div>
                    <div>Next step: {app["next_step"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Filtered tabs
        with tab2:
            in_progress = [app for app in applications if app["status"] in ["Application Review", "Application Submitted"]]
            if in_progress:
                for app in in_progress:
                    st.markdown(f"""
                    <div class='card animated'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                            <h3 style='margin: 0;'>{app["job_title"]}</h3>
                            <span style='color: #FFA500; font-weight: 600;'>{app["status"]}</span>
                        </div>
                        <div style='margin-bottom: 0.5rem;'>{app["company"]} | Applied on {app["applied_date"]}</div>
                        <div>Next step: {app["next_step"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No applications in progress")
        
        with tab3:
            interviews = [app for app in applications if app["status"] == "Interview Scheduled"]
            if interviews:
                for app in interviews:
                    st.markdown(f"""
                    <div class='card animated'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                            <h3 style='margin: 0;'>{app["job_title"]}</h3>
                            <span style='color: #00A8E8; font-weight: 600;'>{app["status"]}</span>
                        </div>
                        <div style='margin-bottom: 0.5rem;'>{app["company"]} | Applied on {app["applied_date"]}</div>
                        <div>Next step: {app["next_step"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No upcoming interviews")
        
        with tab4:
            rejected = [app for app in applications if app["status"] == "Rejected"]
            if rejected:
                for app in rejected:
                    st.markdown(f"""
                    <div class='card animated'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                            <h3 style='margin: 0;'>{app["job_title"]}</h3>
                            <span style='color: #FF6347; font-weight: 600;'>{app["status"]}</span>
                        </div>
                        <div style='margin-bottom: 0.5rem;'>{app["company"]} | Applied on {app["applied_date"]}</div>
                        <div>Next step: {app["next_step"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No rejected applications")
    
    elif selected == "Dashboard" and st.session_state.user_role != "jobseeker":
        st.markdown("<h1 class='main-title'>Employer Dashboard</h1>", unsafe_allow_html=True)
        
        # Dashboard metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='dashboard-stat'>
                <div class='dashboard-value'>12</div>
                <div class='dashboard-label'>Active Jobs</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='dashboard-stat'>
                <div class='dashboard-value'>143</div>
                <div class='dashboard-label'>Applications</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='dashboard-stat'>
                <div class='dashboard-value'>28</div>
                <div class='dashboard-label'>Interviews</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class='dashboard-stat'>
                <div class='dashboard-value'>8</div>
                <div class='dashboard-label'>Hires</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs for different dashboard sections
        tab1, tab2, tab3 = st.tabs(["Posted Jobs", "Applications", "Candidates"])
        
        with tab1:
            # Posted jobs section
            st.subheader("Your Job Listings")
            
            # Add new job button
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("+ Post New Job", use_container_width=True):
                    st.session_state.show_job_form = True
            
            # Show job form if button clicked
            if st.session_state.get("show_job_form", False):
                with st.form("new_job_form"):
                    st.subheader("Create New Job Listing")
                    
                    job_title = st.text_input("Job Title", placeholder="e.g. Senior Developer")
                    job_description = st.text_area("Job Description", placeholder="Describe the job responsibilities and requirements")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        job_location = st.text_input("Location", placeholder="e.g. Remote, New York, etc.")
                        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Internship"])
                    
                    with col2:
                        salary_range = st.text_input("Salary Range", placeholder="e.g. $80K - $100K")
                        experience_level = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior", "Executive"])
                    
                    # Form submission
                    col1, col2 = st.columns(2)
                    with col1:
                        cancel = st.form_submit_button("Cancel")
                    with col2:
                        submit = st.form_submit_button("Create Job")
                    
                    if submit:
                        # Would insert into Supabase here
                        # supabase.table("jobs").insert({
                        #     "title": job_title,
                        #     "description": job_description,
                        #     "location": job_location,
                        #     "job_type": job_type,
                        #     "salary_range": salary_range,
                        #     "experience_level": experience_level,
                        #     "employer_id": st.session_state.user_id,
                        #     "created_at": "now()"
                        # }).execute()
                        st.success("Job posted successfully!")
                        st.session_state.show_job_form = False
                        st.rerun()
                    
                    if cancel:
                        st.session_state.show_job_form = False
                        st.rerun()
            
            # Sample employer job listings
            employer_jobs = [
                {
                    "id": 1,
                    "title": "Senior Full Stack Developer",
                    "posted_date": "2023-02-01",
                    "applications": 45,
                    "status": "Active",
                    "views": 320
                },
                {
                    "id": 2,
                    "title": "UX/UI Designer",
                    "posted_date": "2023-02-10",
                    "applications": 28,
                    "status": "Active",
                    "views": 215
                },
                {
                    "id": 3,
                    "title": "Project Manager",
                    "posted_date": "2023-01-15",
                    "applications": 52,
                    "status": "Closed",
                    "views": 410
                },
                {
                    "id": 4,
                    "title": "Marketing Specialist",
                    "posted_date": "2023-02-20",
                    "applications": 18,
                    "status": "Active",
                    "views": 130
                }
            ]
            
            for job in employer_jobs:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class='card'>
                        <h3>{job["title"]}</h3>
                        <div>Posted on: {job["posted_date"]} | Status: <span style='color: {"#00A8E8" if job["status"] == "Active" else "#FF6347"};'>{job["status"]}</span></div>
                        <div style='margin-top: 0.5rem;'>{job["applications"]} applications | {job["views"]} views</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='height: 100%; display: flex; flex-direction: column; justify-content: center;'>", unsafe_allow_html=True)
                    st.button("View Details", key=f"view_job_{job['id']}")
                    st.button("Edit Job", key=f"edit_job_{job['id']}")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            # Applications management
            st.subheader("Recent Applications")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                job_filter = st.selectbox("Filter by Job", ["All Jobs", "Senior Full Stack Developer", "UX/UI Designer", "Project Manager", "Marketing Specialist"])
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All Statuses", "New", "Reviewed", "Interview", "Rejected", "Hired"])
            with col3:
                date_filter = st.selectbox("Filter by Date", ["All Time", "Today", "This Week", "This Month"])
            
            # Sample applications data
            applications = [
                {
                    "id": 1,
                    "candidate_name": "John Smith",
                    "job_title": "Senior Full Stack Developer",
                    "applied_date": "2023-02-18",
                    "status": "Interview",
                    "resume": "https://example.com/resume1.pdf"
                },
                {
                    "id": 2,
                    "candidate_name": "Emily Johnson",
                    "job_title": "UX/UI Designer",
                    "applied_date": "2023-02-17",
                    "status": "New",
                    "resume": "https://example.com/resume2.pdf"
                },
                {
                    "id": 3,
                    "candidate_name": "Michael Brown",
                    "job_title": "Project Manager",
                    "applied_date": "2023-02-15",
                    "status": "Reviewed",
                    "resume": "https://example.com/resume3.pdf"
                },
                {
                    "id": 4,
                    "candidate_name": "Sarah Williams",
                    "job_title": "Senior Full Stack Developer",
                    "applied_date": "2023-02-10",
                    "status": "Rejected",
                    "resume": "https://example.com/resume4.pdf"
                },
                {
                    "id": 5,
                    "candidate_name": "David Lee",
                    "job_title": "Marketing Specialist",
                    "applied_date": "2023-02-20",
                    "status": "New",
                    "resume": "https://example.com/resume5.pdf"
                }
            ]
            
            # Display applications in a table-like format
            for app in applications:
                status_color = "#00A8E8" if app["status"] == "Interview" else "#4CAF50" if app["status"] == "Hired" else "#FFA500" if app["status"] == "New" or app["status"] == "Reviewed" else "#FF6347"
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class='card'>
                        <h3>{app["candidate_name"]}</h3>
                        <div>Applied for: {app["job_title"]} | Date: {app["applied_date"]}</div>
                        <div style='margin-top: 0.5rem;'>Status: <span style='color: {status_color};'>{app["status"]}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='height: 100%; display: flex; flex-direction: column; justify-content: center;'>", unsafe_allow_html=True)
                    st.button("View Profile", key=f"view_app_{app['id']}")
                    st.button("Change Status", key=f"status_app_{app['id']}")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            # Candidate tracking
            st.subheader("Talent Pool")
            
            # Search candidates
            search_candidates = st.text_input("Search candidates", placeholder="Name or skills")
            
            # Sample candidates
            candidates = [
                {
                    "id": 1,
                    "name": "John Smith",
                    "title": "Senior Developer",
                    "skills": ["React", "Node.js", "AWS", "Python"],
                    "experience": "8 years",
                    "location": "New York, USA",
                    "status": "Active"
                },
                {
                    "id": 2,
                    "name": "Emily Johnson",
                    "title": "UX/UI Designer",
                    "skills": ["Figma", "Adobe XD", "Sketch", "CSS"],
                    "experience": "5 years",
                    "location": "San Francisco, USA",
                    "status": "Interviewing"
                },
                {
                    "id": 3,
                    "name": "Michael Brown",
                    "title": "Project Manager",
                    "skills": ["Agile", "Scrum", "JIRA", "Product Management"],
                    "experience": "10 years",
                    "location": "Chicago, USA",
                    "status": "Contacted"
                },
                {
                    "id": 4,
                    "name": "Sarah Williams",
                    "title": "Full Stack Developer",
                    "skills": ["JavaScript", "React", "MongoDB", "Express"],
                    "experience": "4 years",
                    "location": "Remote",
                    "status": "New"
                }
            ]
            
            # Display candidates in a grid
            col1, col2 = st.columns(2)
            
            for i, candidate in enumerate(candidates):
                with col1 if i % 2 == 0 else col2:
                    skills_html = " ".join([f"<span style='background-color: rgba(0, 168, 232, 0.2); padding: 3px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8rem;'>{skill}</span>" for skill in candidate["skills"]])
                    
                    status_color = "#00A8E8" if candidate["status"] == "Interviewing" else "#4CAF50" if candidate["status"] == "Active" else "#FFA500" if candidate["status"] == "Contacted" else "#6c757d"
                    
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h3>{candidate["name"]}</h3>
                            <span style='color: {status_color}; font-weight: 600;'>{candidate["status"]}</span>
                        </div>
                        <div style='margin-bottom: 0.5rem;'>{candidate["title"]} | {candidate["experience"]} | {candidate["location"]}</div>
                        <div style='margin-bottom: 0.5rem;'>{skills_html}</div>
                        <div style='display: flex; gap: 10px; margin-top: 10px;'>
                            <button style='background-color: #00A8E8; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>View Profile</button>
                            <button style='background-color: rgba(255, 255, 255, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>Contact</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif selected == "Profile":
        st.markdown("<h1 class='main-title'>My Profile</h1>", unsafe_allow_html=True)
        
        # Profile header with user info
        st.markdown(f"""
        <div class='profile-header'>
            <img src="https://via.placeholder.com/150" class="profile-picture">
            <div class='profile-info'>
                <div class='profile-name'>{st.session_state.user_name}</div>
                <div class='profile-role'>{st.session_state.user_role.capitalize()}</div>
                <div style='margin-top: 5px;'>{st.session_state.user_email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different profile sections
        if st.session_state.user_role == "jobseeker":
            tab1, tab2, tab3, tab4 = st.tabs(["Personal Info", "Resume", "Job Preferences", "Account Settings"])
            
            with tab1:
                # Personal information form
                with st.form("personal_info_form"):
                    st.subheader("Personal Information")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", value="John")
                        phone = st.text_input("Phone Number", value="+1 123-456-7890")
                        city = st.text_input("City", value="New York")
                    
                    with col2:
                        last_name = st.text_input("Last Name", value="Smith")
                        website = st.text_input("Website/Portfolio", value="https://johnsmith.dev")
                        country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Germany", "Australia"])
                    
                    about_me = st.text_area("About Me", value="Experienced software developer with a passion for creating clean, efficient, and user-friendly applications. Specialized in full-stack development with expertise in React, Node.js, and cloud technologies.")
                    
                    st.form_submit_button("Save Changes")
            
            with tab2:
                # Resume section
                st.subheader("Resume/CV")
                
                # Upload resume
                uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
                
                if uploaded_file is not None:
                    st.success("Resume uploaded successfully!")
                
                # Experience section
                st.subheader("Work Experience")
                
                # Sample experience
                experiences = [
                    {
                        "title": "Senior Developer",
                        "company": "TechSolutions Inc.",
                        "duration": "Jan 2020 - Present",
                        "description": "Leading the development of web applications using React and Node.js. Managing a team of 5 developers."
                    },
                    {
                        "title": "Frontend Developer",
                        "company": "WebInnovate",
                        "duration": "Mar 2017 - Dec 2019",
                        "description": "Developed responsive web interfaces using React and Redux. Collaborated with designers and backend developers."
                    }
                ]
                
                for exp in experiences:
                    with st.expander(f"{exp['title']} at {exp['company']}"):
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            job_title = st.text_input("Job Title", value=exp["title"], key=f"title_{exp['company']}")
                        with col2:
                            company = st.text_input("Company", value=exp["company"], key=f"company_{exp['company']}")
                        with col3:
                            duration = st.text_input("Duration", value=exp["duration"], key=f"duration_{exp['company']}")
                        
                        description = st.text_area("Description", value=exp["description"], key=f"desc_{exp['company']}")
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.button("Update", key=f"update_{exp['company']}")
                        with col2:
                            st.button("Delete", key=f"delete_{exp['company']}")
                
                # Add new experience button
                if st.button("+ Add Experience"):
                    st.info("Add new experience functionality would be implemented here")
                
                # Education section
                st.subheader("Education")
                
                # Sample education
                education = [
                    {
                        "degree": "Master of Computer Science",
                        "institution": "University of Technology",
                        "years": "2015 - 2017"
                    },
                    {
                        "degree": "Bachelor of Science in Computer Science",
                        "institution": "State University",
                        "years": "2011 - 2015"
                    }
                ]
                
                for edu in education:
                    with st.expander(f"{edu['degree']} - {edu['institution']}"):
                        col1, col2, col3 = st.columns([3, 3, 2])
                        with col1:
                            degree = st.text_input("Degree", value=edu["degree"], key=f"degree_{edu['institution']}")
                        with col2:
                            institution = st.text_input("Institution", value=edu["institution"], key=f"inst_{edu['institution']}")
                        with col3:
                            years = st.text_input("Years", value=edu["years"], key=f"years_{edu['institution']}")
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.button("Update", key=f"update_edu_{edu['institution']}")
                        with col2:
                            st.button("Delete", key=f"delete_edu_{edu['institution']}")
                
                # Add new education button
                if st.button("+ Add Education"):
                    st.info("Add new education functionality would be implemented here")
                
                # Skills section
                st.subheader("Skills")
                
                # Sample skills
                skills = ["Python", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker", "Git"]
                
                # Display skills as chips/tags
                skills_input = st.text_input("Add skills (comma separated)", value=", ".join(skills))
                
                st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;'>", unsafe_allow_html=True)
                for skill in skills:
                    st.markdown(f"""
                    <div style='background-color: rgba(0, 168, 232, 0.2); padding: 5px 15px; border-radius: 20px; display: flex; align-items: center;'>
                        <span>{skill}</span>
                        <span style='margin-left: 5px; cursor: pointer;'>✕</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with tab3:
                # Job preferences
                st.subheader("Job Preferences")
                
                col1, col2 = st.columns(2)
                with col1:
                    job_titles = st.multiselect(
                        "Job Titles",
                        ["Software Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "DevOps Engineer", "Data Scientist"],
                        ["Full Stack Developer", "Frontend Developer"]
                    )
                    
                    job_types = st.multiselect(
                        "Job Types",
                        ["Full-time", "Part-time", "Contract", "Freelance", "Internship"],
                        ["Full-time", "Contract"]
                    )
                
                with col2:
                    locations = st.multiselect(
                        "Preferred Locations",
                        ["Remote", "United States", "Europe", "Asia", "Australia"],
                        ["Remote", "United States"]
                    )
                    
                    salary_expectation = st.select_slider(
                        "Salary Expectation (USD)",
                        options=["$40K - $60K", "$60K - $80K", "$80K - $100K", "$100K - $120K", "$120K - $150K", "$150K+"],
                        value="$100K - $120K"
                    )
                
                relocation = st.checkbox("Open to relocation")
                travel = st.checkbox("Willing to travel")
                
                st.text_area("Additional Preferences", placeholder="Any other job preferences you'd like employers to know")
                
                st.button("Save Preferences")
            
            with tab4:
                # Account settings
                st.subheader("Account Settings")
                
                # Password change
                with st.expander("Change Password"):
                    col1, col2 = st.columns(2)
                    with col1:
                        current_password = st.text_input("Current Password", type="password")
                    with col2:
                        new_password = st.text_input("New Password", type="password")
                    
                    confirm_password = st.text_input("Confirm New Password", type="password")
                    
                    st.button("Update Password")
                
                # Email notifications
                with st.expander("Email Notifications"):
                    st.checkbox("Job recommendations", value=True)
                    st.checkbox("Application updates", value=True)
                    st.checkbox("Profile views", value=False)
                    st.checkbox("Job alerts based on preferences", value=True)
                    
                    st.button("Save Notification Settings")
                
                # Privacy settings
                with st.expander("Privacy Settings"):
                    st.checkbox("Make profile visible to employers", value=True)
                    st.checkbox("Allow employers to contact me", value=True)
                    st.checkbox("Show salary expectations on profile", value=False)
                    
                    st.button("Save Privacy Settings")
                
                # Account deletion
                with st.expander("Delete Account"):
                    st.warning("Warning: Deleting your account will permanently remove all your data. This action cannot be undone.")
                    st.text_input("Type 'DELETE' to confirm", placeholder="DELETE")
                    
                    st.button("Delete My Account", type="primary", help="This action is irreversible")
        else:
            # Employer profile
            tab1, tab2, tab3 = st.tabs(["Company Profile", "Job Postings", "Account Settings"])
            
            with tab1:
                # Company profile form
                with st.form("company_profile_form"):
                    st.subheader("Company Information")
                    
                    # Company logo upload
                    st.file_uploader("Company Logo", type=["png", "jpg", "jpeg"])
                    
                    company_name = st.text_input("Company Name", value="TechNova Inc.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing", "Other"])
                        company_size = st.selectbox("Company Size", ["1-10 employees", "11-50 employees", "51-200 employees", "201-1000 employees", "1000+ employees"])
                    
                    with col2:
                        website = st.text_input("Company Website", value="https://technova.example.com")
                        founded_year = st.number_input("Year Founded", min_value=1900, max_value=2023, value=2010)
                    
                    company_description = st.text_area("Company Description", value="TechNova is a leading software development company specializing in innovative enterprise solutions. We create cutting-edge applications that help businesses streamline operations and enhance customer experiences.")
                    
                    st.subheader("Location")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        address = st.text_input("Address", value="123 Tech Boulevard")
                        city = st.text_input("City", value="San Francisco")
                    
                    with col2:
                        state = st.text_input("State/Province", value="California")
                        country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Germany", "Australia"])
                    
                    st.form_submit_button("Save Company Profile")
            
            with tab2:
                st.subheader("Active Job Postings")
                
                # Job posting stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Active Jobs", "12")
                with col2:
                    st.metric("Applications Received", "143", "+28")
                with col3:
                    st.metric("Jobs Filled", "8", "+2")
                
                # Job listings
                active_jobs = [
                    {
                        "id": 1,
                        "title": "Senior Full Stack Developer",
                        "posted_date": "2023-02-01",
                        "expiry_date": "2023-03-01",
                        "applications": 45,
                        "status": "Active"
                    },
                    {
                        "id": 2,
                        "title": "UX/UI Designer",
                        "posted_date": "2023-02-10",
                        "expiry_date": "2023-03-10",
                        "applications": 28,
                        "status": "Active"
                    },
                    {
                        "id": 4,
                        "title": "Marketing Specialist",
                        "posted_date": "2023-02-20",
                        "expiry_date": "2023-03-20",
                        "applications": 18,
                        "status": "Active"
                    }
                ]
                
                for job in active_jobs:
                    st.markdown(f"""
                    <div class='card animated'>
                        <h3>{job["title"]}</h3>
                        <div>Posted: {job["posted_date"]} | Expires: {job["expiry_date"]}</div>
                        <div style='margin-top: 0.5rem;'>{job["applications"]} applications received</div>
                        <div style='display: flex; gap: 10px; margin-top: 10px;'>
                            <button style='background-color: #00A8E8; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>View Applications</button>
                            <button style='background-color: rgba(255, 255, 255, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>Edit Job</button>
                            <button style='background-color: rgba(255, 0, 0, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>Close Job</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.button("+ Post New Job")
            
            with tab3:
                # Account settings
                st.subheader("Account Settings")
                
                # Subscription plan
                st.markdown("""
                <div class='card'>
                    <h3>Current Plan: Business Pro</h3>
                    <div>Active until: March 15, 2023</div>
                    <div style='margin-top: 1rem;'>
                        <span style='background-color: rgba(0, 168, 232, 0.2); padding: 5px 10px; border-radius: 5px; margin-right: 10px;'>Unlimited job postings</span>
                        <span style='background-color: rgba(0, 168, 232, 0.2); padding: 5px 10px; border-radius: 5px; margin-right: 10px;'>Featured listings</span>
                        <span style='background-color: rgba(0, 168, 232, 0.2); padding: 5px 10px; border-radius: 5px; margin-right: 10px;'>Advanced analytics</span>
                    </div>
                    <div style='margin-top: 1rem;'>
                        <button style='background-color: #00A8E8; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;'>Upgrade Plan</button>
                        <button style='background-color: rgba(255, 255, 255, 0.2); color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer; margin-left: 10px;'>Billing History</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Company users
                st.subheader("Company Users")
                
                # Sample users
                company_users = [
                    {
                        "name": "John Smith",
                        "email": "john@technova.example.com",
                        "role": "Admin",
                        "last_active": "Today"
                    },
                    {
                        "name": "Sarah Johnson",
                        "email": "sarah@technova.example.com",
                        "role": "Recruiter",
                        "last_active": "Yesterday"
                    },
                    {
                        "name": "Michael Brown",
                        "email": "michael@technova.example.com",
                        "role": "Hiring Manager",
                        "last_active": "3 days ago"
                    }
                ]
                
                for user in company_users:
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <h3>{user["name"]}</h3>
                                <div>{user["email"]}</div>
                                <div style='margin-top: 0.5rem;'>Role: {user["role"]} | Last active: {user["last_active"]}</div>
                            </div>
                            <div>
                                <button style='background-color: rgba(255, 255, 255, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>Edit</button>
                                <button style='background-color: rgba(255, 0, 0, 0.2); color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-left: 5px;'>Remove</button>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("+ Add Team Member"):
                    st.info("Invite team member functionality would be implemented here")
                
                # Company settings
                with st.expander("Email Settings"):
                    st.checkbox("New application notifications", value=True)
                    st.checkbox("Daily application summary", value=True)
                    st.checkbox("Job posting expiry reminders", value=True)
                    
                    st.button("Save Email Settings")
                
                # API access
                with st.expander("API Access"):
                    st.text("API Key: ********-****-****-****-************")
                    st.button("Generate New API Key")
                    st.markdown("Use our API to integrate job postings with your company website or ATS.")
else:
    # User is not authenticated
    st.markdown("<h1 class='main-title'>Welcome to JobWave</h1>", unsafe_allow_html=True)
    
    # Create two columns for login and hero image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<p class='subtitle'>The modern job portal for employers and job seekers</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h2>Sign In to Get Started</h2>
            <p>Please use Clerk authentication to sign in or create an account.</p>
            <p>Choose your role when signing up:</p>
            <ul>
                <li>Job Seeker - Find jobs and manage applications</li>
                <li>Employer - Post jobs and find talent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Features list
        st.markdown("""
        <div class='card' style='margin-top: 20px;'>
            <h2>Key Features</h2>
            <ul>
                <li><strong>For Job Seekers:</strong> Easy application process, personalized job recommendations, application tracking</li>
                <li><strong>For Employers:</strong> Post unlimited jobs, manage applications, search talent pool</li>
                <li><strong>For Everyone:</strong> User-friendly interface, secure authentication, real-time updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Lottie animation for the landing page
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_sSF6EG.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie.st_lottie(lottie_json, height=400)
        
        # Login/Sign up prompt
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <h3>Ready to start your journey?</h3>
            <p>Sign in with Clerk to access all features</p>
        </div>
        """, unsafe_allow_html=True)
