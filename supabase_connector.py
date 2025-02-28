import streamlit as st
from supabase import create_client, Client
from typing import Dict, List, Any, Optional, Union
import logging

class SupabaseConnector:
    """Class to handle Supabase database operations for the job portal."""
    
    def __init__(self):
        """Initialize the Supabase client."""
        try:
            self.supabase_url = st.secrets.get("SUPABASE_URL", "")
            self.supabase_key = st.secrets.get("SUPABASE_KEY", "")
            
            if not self.supabase_url or not self.supabase_key:
                st.warning("Supabase credentials not found in secrets. Using mock data.")
                self.client = None
            else:
                self.client = create_client(self.supabase_url, self.supabase_key)
                
        except Exception as e:
            logging.error(f"Error initializing Supabase client: {str(e)}")
            st.error(f"Error connecting to database. Using mock data instead.")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if connected to Supabase."""
        return self.client is not None
    
    # User operations
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a user's profile from the database.
        
        Args:
            user_id: The user's ID
            
        Returns:
            The user profile or None if not found
        """
        if not self.is_connected():
            # Return mock data
            return {
                "user_id": user_id,
                "first_name": "Demo",
                "last_name": "User",
                "email": "demo@example.com",
                "phone": "+1 555-123-4567",
                "city": "New York",
                "country": "USA",
                "about": "This is a demo profile as the database connection is not available.",
                "website": "https://example.com",
                "role": "jobseeker"
            }
            
        try:
            response = self.client.table("profiles").select("*").eq("user_id", user_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            logging.error(f"Error fetching user profile: {str(e)}")
            return None
    
    def create_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        Create a new user profile.
        
        Args:
            profile_data: The profile data to insert
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            # Simulate success for demo
            return True
            
        try:
            self.client.table("profiles").insert(profile_data).execute()
            return True
        except Exception as e:
            logging.error(f"Error creating user profile: {str(e)}")
            return False
    
    # Job operations
    def get_jobs(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get jobs with optional filtering.
        
        Args:
            filters: Optional dictionary of filters
            limit: Maximum number of jobs to return
            
        Returns:
            List of jobs
        """
        if not self.is_connected():
            # Return mock data
            return [
                {
                    "id": "1",
                    "title": "Senior Full Stack Developer", 
                    "company": "TechNova Inc.",
                    "location": "Remote",
                    "job_type": "Full-time",
                    "salary": "$120K - $150K",
                    "posted": "2 days ago",
                    "description": "Join our team to build innovative solutions for enterprise clients using React, Node.js, and AWS."
                },
                {
                    "id": "2",
                    "title": "UX/UI Designer", 
                    "company": "CreativeMinds",
                    "location": "New York, USA",
                    "job_type": "Full-time",
                    "salary": "$90K - $110K",
                    "posted": "5 days ago",
                    "description": "We're looking for a talented designer to create beautiful interfaces. Experience with Figma and design systems required."
                },
                {
                    "id": "3",
                    "title": "Data Scientist", 
                    "company": "DataFlow Analytics",
                    "location": "San Francisco, USA",
                    "job_type": "Full-time",
                    "salary": "$130K - $160K",
                    "posted": "1 week ago",
                    "description": "Build ML models and analyze large datasets to extract valuable insights. Strong Python and statistics skills required."
                },
                {
                    "id": "4",
                    "title": "DevOps Engineer", 
                    "company": "CloudSphere",
                    "location": "Remote",
                    "job_type": "Contract",
                    "salary": "$100K - $130K",
                    "posted": "2 weeks ago",
                    "description": "Improve our cloud infrastructure and implement CI/CD pipelines. Experience with Kubernetes and AWS required."
                },
                {
                    "id": "5",
                    "title": "Product Manager", 
                    "company": "InnovateCorp",
                    "location": "Chicago, USA",
                    "job_type": "Full-time",
                    "salary": "$110K - $140K",
                    "posted": "3 days ago",
                    "description": "Lead product development from concept to launch. Strong communication and analytical skills required."
                }
            ]
            
        try:
            query = self.client.table("jobs").select("*").limit(limit)
            
            if filters:
                # Apply filters
                if "search" in filters and filters["search"]:
                    query = query.ilike("title", f"%{filters['search']}%")
                
                if "location" in filters and filters["location"] and filters["location"] != "Any Location":
                    query = query.eq("location", filters["location"])
                
                if "job_type" in filters and filters["job_type"] and filters["job_type"] != "Any Type":
                    query = query.eq("job_type", filters["job_type"])
                
                if "experience" in filters and filters["experience"] and filters["experience"] != "Any Level":
                    query = query.eq("experience_level", filters["experience"])
                
                if "salary" in filters and filters["salary"] and filters["salary"] != "Any Range":
                    # Handle salary range filtering (simplified)
                    if filters["salary"] == "Under $50K":
                        query = query.lt("salary_max", 50000)
                    elif filters["salary"] == "$50K - $100K":
                        query = query.gte("salary_min", 50000).lt("salary_max", 100000)
                    elif filters["salary"] == "$100K - $150K":
                        query = query.gte("salary_min", 100000).lt("salary_max", 150000)
                    elif filters["salary"] == "Over $150K":
                        query = query.gte("salary_min", 150000)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching jobs: {str(e)}")
            return []
    
    # Application operations
    def get_applications_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get applications made by a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of applications
        """
        if not self.is_connected():
            # Return mock data
            return [
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
                }
            ]
            
        try:
            response = self.client.table("applications").select("*, jobs(*)").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching applications: {str(e)}")
            return []
    
    # Company operations
    def get_companies(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get companies with optional filtering.
        
        Args:
            filters: Optional dictionary of filters
            limit: Maximum number of companies to return
            
        Returns:
            List of companies
        """
        if not self.is_connected():
            # Return mock data
            return [
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
                }
            ]
            
        try:
            query = self.client.table("companies").select("*").limit(limit)
            
            if filters:
                # Apply filters
                if "search" in filters and filters["search"]:
                    query = query.ilike("name", f"%{filters['search']}%")
                
                if "industry" in filters and filters["industry"] and filters["industry"] != "All Industries":
                    query = query.eq("industry", filters["industry"])
                
                if "size" in filters and filters["size"] and filters["size"] != "Any Size":
                    query = query.eq("company_size", filters["size"])
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching companies: {str(e)}")
            return []
