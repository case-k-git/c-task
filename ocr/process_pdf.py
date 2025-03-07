import os
import time
import boto3
import requests
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Inside.AI API settings
API_KEY = os.getenv('INSIDE_AI_API_KEY')
ACCOUNT_ID = os.getenv('INSIDE_AI_ACCOUNT_ID')
WORKFLOW_ID = os.getenv('INSIDE_AI_WORKFLOW_ID')

# API base URL configuration
BASE_URL = f'https://{ACCOUNT_ID}.dx-suite.com'
# Change authentication header to 'apikey' according to documentation
HEADERS = {
    'apikey': API_KEY,
    'Accept': 'application/json'
}

# AWS configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_KEY = os.getenv('S3_PDF_KEY')

# Create common session
session = requests.Session()
session.headers.update(HEADERS)

def get_pdf_from_s3() -> str:
    """Download PDF file from S3"""
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    
    local_file = '/tmp/temp.pdf'
    s3.download_file(S3_BUCKET, S3_KEY, local_file)
    logger.info(f"Downloaded PDF file from {S3_BUCKET}/{S3_KEY}")
    return local_file

def register_reading_unit(pdf_path: str) -> str:
    """Register reading unit with PDF file"""
    url = f'{BASE_URL}/wf/api/standard/v2/workflows/{WORKFLOW_ID}/units'
    with open(pdf_path, 'rb') as pdf_file:
        # Send with parameter name "files" (supports multiple file uploads)
        files = {
            'files': ('document.pdf', pdf_file, 'application/pdf')
        }
        response = session.post(url, files=files)
    response.raise_for_status()
    # Response returns { "unitId": "xxxx", "unitName": "test" }
    unit_id = response.json()['unitId']
    logger.info(f"Registered reading unit (unitId: {unit_id})")
    return unit_id

def get_reading_unit_status(unit_id: str) -> dict:
    """Get reading unit status"""
    # Modified endpoint according to documentation
    url = f'{BASE_URL}/wf/api/standard/v2/units/status?unitId={unit_id}'
    response = session.get(url)
    response.raise_for_status()
    data = response.json()
    # Use first element from array of multiple unit information (adjust as needed)
    if isinstance(data, list) and len(data) > 0:
        status = data[0].get('dataProcessingStatus')
        logger.info(f"Reading unit status: {status}")
        return data[0]
    logger.info("No status information found")
    return {}

def download_result(unit_id: str) -> None:
    """Download result as CSV file"""
    # Modified to CSV download endpoint according to documentation
    url = f'{BASE_URL}/wf/api/standard/v2/units/{unit_id}/csv'
    csv_headers = session.headers.copy()
    csv_headers['Accept'] = 'text/csv'
    
    response = session.get(url, headers=csv_headers)
    response.raise_for_status()
    
    with open('result.csv', 'wb') as f:
        f.write(response.content)
    
    logger.info("Saved results to result.csv")

def main() -> None:
    logger.info("Starting process")
    pdf_path = None

    try:
        # Get PDF from S3
        pdf_path = get_pdf_from_s3()
        
        # Register reading unit
        unit_id = register_reading_unit(pdf_path)
        
        # Polling until process completion
        while True:
            status_data = get_reading_unit_status(unit_id)
            # Check status according to unit specifications
            status = status_data.get('dataProcessingStatus')
            
            if status == 'completed':
                logger.info("Process completed")
                break
            elif status == 'failed':
                logger.error("Process failed")
                break
            
            logger.info("Processing...")
            time.sleep(10)
        
        # Download results (only when completed)
        if status == 'completed':
            download_result(unit_id)
    
    except Exception as e:
        logger.exception("An error occurred during processing")
    
    finally:
        # Clean up temporary file
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info("Removed temporary file")

if __name__ == '__main__':
    main()
