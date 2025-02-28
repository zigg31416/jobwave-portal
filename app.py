import streamlit as st
import streamlit_lottie as st_lottie
import requests
import json
from streamlit_option_menu import option_menu
from supabase_connector import SupabaseConnector
from streamlit_clerk_auth import authenticate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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

# Connect to database
@st.cache_resource
def init_database():
    return SupabaseConnector()

# Initialize database connector
db = init_database()

# Apply custom CSS
load_css()

# Authenticate user
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
        
        # Tabs for different dashboard sections
        tab1, tab2, tab3 = st.tabs(["Posted Jobs", "Applications", "Candidates"])
        
        with tab1:
            # Sample employer job listings (would be from database in production)
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
                }
            ]
            
            # Add new job button
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
                        st.success("Job posted successfully! (Demo mode)")
                        st.session_state.show_job_form = False
                        st.rerun()
                    
                    if cancel:
                        st.session_state.show_job_form = False
                        st.rerun()
            
            # Display job listings
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
    
    elif selected == "Profile":
        st.markdown("<h1 class='main-title'>My Profile</h1>", unsafe_allow_html=True)
        
        # Get user profile (would be from database in production)
        if db.is_connected():
            profile = db.get_user_profile(st.session_state.user_id)
        else:
            # Mock profile data
            profile = {
                "first_name": st.session_state.user_name.split(" ")[0],
                "last_name": st.session_state.user_name.split(" ")[-1] if len(st.session_state.user_name.split(" ")) > 1 else "",
                "email": st.session_state.user_email,
                "phone": "+1 555-123-4567",
                "city": "New York",
                "country": "USA",
                "role": st.session_state.user_role
            }
        
        # Tabs for different profile sections
        if st.session_state.user_role == "jobseeker":
            tab1, tab2, tab3 = st.tabs(["Personal Info", "Resume", "Job Preferences"])
            
            with tab1:
                # Personal information form
                with st.form("personal_info_form"):
                    st.subheader("Personal Information")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", value=profile.get("first_name", ""))
                        phone = st.text_input("Phone Number", value=profile.get("phone", ""))
                        city = st.text_input("City", value=profile.get("city", ""))
                    
                    with col2:
                        last_name = st.text_input("Last Name", value=profile.get("last_name", ""))
                        website = st.text_input("Website/Portfolio", value=profile.get("website", ""))
                        country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Germany", "Australia"])
                    
                    about_me = st.text_area("About Me", value=profile.get("about", ""))
                    
                    if st.form_submit_button("Save Changes"):
                        st.success("Profile updated successfully! (Demo mode)")
            
            with tab2:
                # Resume section
                st.subheader("Resume/CV")
                
                # Upload resume
                uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
                
                if uploaded_file is not None:
                    st.success("Resume uploaded successfully! (Demo mode)")
                
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
                
                st.button("Save Preferences")
        else:
            # Employer profile
            tab1, tab2 = st.tabs(["Company Profile", "Job Postings"])
            
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
                    
                    company_description = st.text_area("Company Description", value="TechNova is a leading software development company specializing in innovative enterprise solutions.")
                    
                    if st.form_submit_button("Save Company Profile"):
                        st.success("Company profile updated successfully! (Demo mode)")
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
            <p>Please use authentication to sign in or create an account.</p>
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

if __name__ == "__main__":
    # This will run when the script is executed directly
    # Can be used for initialization if needed
    pass
