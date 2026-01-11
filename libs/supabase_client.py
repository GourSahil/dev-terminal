import supabase
import logging

logger = logging.getLogger(__name__)

def create_client(supabase_url=None, supabase_key=None):
    if (supabase_url is None) or (supabase_key is None):
        logger.error("Supabase URL or Key not provided.")
        raise ValueError("Supabase URL and Key must be provided to create the client.")
    Supabase = supabase.create_client(
        supabase_url,
        supabase_key
    )
    logger.info("Supabase client created successfully.")
    return Supabase
