import streamlit as st
from supabase import create_client
from typing import Dict, List, Any, Optional, Union

class SupabaseConnector:
    """Class to handle Supabase database operations for the job portal."""
    
    def __init__(self):
        """Initialize the Supabase client."""
        self.supabase_url = st.secrets.get("SUPABASE_URL", "your_supabase_url")
        self.supabase_key = st.secrets.get("SUPABASE_KEY", "your_supabase_key")
        self.client = create_client(self.supabase_url, self.supabase_key)
    
    # User operations
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a user's profile from the database.
        
        Args:
            user_id: The user's ID
            
        Returns:
            The user profile or None if not found
        """
        try:
            response = self.client.table("profiles").select("*").eq("user_id", user_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            st.error(f"Error fetching user profile: {str(e)}")
            return None
    
    def create_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        Create a new user profile.
        
        Args:
            profile_data: The profile data to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("profiles").insert(profile_data).execute()
            return True
        except Exception as e:
            st.error(f"Error creating user profile: {str(e)}")
            return False
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Update a user's profile.
        
        Args:
            user_id: The user's ID
            profile_data: The profile data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("profiles").update(profile_data).eq("user_id", user_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating user profile: {str(e)}")
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
            st.error(f"Error fetching jobs: {str(e)}")
            return []
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a job by its ID.
        
        Args:
            job_id: The job ID
            
        Returns:
            The job data or None if not found
        """
        try:
            response = self.client.table("jobs").select("*").eq("id", job_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            st.error(f"Error fetching job: {str(e)}")
            return None
    
    def create_job(self, job_data: Dict[str, Any]) -> Union[str, bool]:
        """
        Create a new job listing.
        
        Args:
            job_data: The job data to insert
            
        Returns:
            The job ID if successful, False otherwise
        """
        try:
            response = self.client.table("jobs").insert(job_data).execute()
            return response.data[0]["id"] if response.data else False
        except Exception as e:
            st.error(f"Error creating job: {str(e)}")
            return False
    
    def update_job(self, job_id: str, job_data: Dict[str, Any]) -> bool:
        """
        Update a job listing.
        
        Args:
            job_id: The job ID
            job_data: The job data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("jobs").update(job_data).eq("id", job_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating job: {str(e)}")
            return False
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job listing.
        
        Args:
            job_id: The job ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("jobs").delete().eq("id", job_id).execute()
            return True
        except Exception as e:
            st.error(f"Error deleting job: {str(e)}")
            return False
    
    # Application operations
    def get_applications_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get applications made by a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of applications
        """
        try:
            response = self.client.table("applications").select("*, jobs(*)").eq("user_id", user_id).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching applications: {str(e)}")
            return []
    
    def get_applications_by_job(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Get applications for a job.
        
        Args:
            job_id: The job ID
            
        Returns:
            List of applications
        """
        try:
            response = self.client.table("applications").select("*, profiles(*)").eq("job_id", job_id).execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching applications: {str(e)}")
            return []
    
    def create_application(self, application_data: Dict[str, Any]) -> bool:
        """
        Create a job application.
        
        Args:
            application_data: The application data to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("applications").insert(application_data).execute()
            return True
        except Exception as e:
            st.error(f"Error creating application: {str(e)}")
            return False
    
    def update_application_status(self, application_id: str, status: str) -> bool:
        """
        Update the status of an application.
        
        Args:
            application_id: The application ID
            status: The new status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("applications").update({"status": status}).eq("id", application_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating application status: {str(e)}")
            return False
    
    # Company operations
    def get_company_by_id(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a company by its ID.
        
        Args:
            company_id: The company ID
            
        Returns:
            The company data or None if not found
        """
        try:
            response = self.client.table("companies").select("*").eq("id", company_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            st.error(f"Error fetching company: {str(e)}")
            return None
    
    def get_companies(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get companies with optional filtering.
        
        Args:
            filters: Optional dictionary of filters
            limit: Maximum number of companies to return
            
        Returns:
            List of companies
        """
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
            st.error(f"Error fetching companies: {str(e)}")
            return []
    
    def update_company(self, company_id: str, company_data: Dict[str, Any]) -> bool:
        """
        Update a company profile.
        
        Args:
            company_id: The company ID
            company_data: The company data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("companies").update(company_data).eq("id", company_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating company: {str(e)}")
            return False
    
    # Analytics operations
    def get_job_analytics(self, employer_id: str) -> Dict[str, Any]:
        """
        Get analytics data for an employer.
        
        Args:
            employer_id: The employer's ID
            
        Returns:
            Dictionary of analytics data
        """
        try:
            # Count active jobs
            active_jobs_query = self.client.table("jobs").select("id").eq("employer_id", employer_id).eq("status", "Active").execute()
            active_jobs_count = len(active_jobs_query.data) if active_jobs_query.data else 0
            
            # Count applications
            applications_query = (
                self.client.table("applications")
                .select("id, job_id")
                .eq("jobs.employer_id", employer_id)
                .execute()
            )
            applications_count = len(applications_query.data) if applications_query.data else 0
            
            # Count interview scheduled
            interviews_query = (
                self.client.table("applications")
                .select("id")
                .eq("jobs.employer_id", employer_id)
                .eq("status", "Interview Scheduled")
                .execute()
            )
            interviews_count = len(interviews_query.data) if interviews_query.data else 0
            
            # Count jobs filled
            filled_jobs_query = (
                self.client.table("jobs")
                .select("id")
                .eq("employer_id", employer_id)
                .eq("status", "Filled")
                .execute()
            )
            filled_jobs_count = len(filled_jobs_query.data) if filled_jobs_query.data else 0
            
            return {
                "active_jobs": active_jobs_count,
                "applications": applications_count,
                "interviews": interviews_count,
                "jobs_filled": filled_jobs_count
            }
        except Exception as e:
            st.error(f"Error fetching analytics: {str(e)}")
            return {
                "active_jobs": 0,
                "applications": 0,
                "interviews": 0,
                "jobs_filled": 0
            }
