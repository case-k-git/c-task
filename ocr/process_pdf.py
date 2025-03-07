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
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# AWS configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_KEY = os.getenv('S3_PDF_KEY')

def get_pdf_from_s3():
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

def register_reading_unit(pdf_path):
    """Register reading unit with PDF file"""
    url = f'{BASE_URL}/wf/api/standard/v2/workflows/{WORKFLOW_ID}/units'
    
    files = {
        'file': ('document.pdf', open(pdf_path, 'rb'), 'application/pdf')
    }
    
    headers = {'Authorization': HEADERS['Authorization']}
    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    
    unit_id = response.json()['id']
    logger.info(f"Registered reading unit (ID: {unit_id})")
    return unit_id

def get_reading_unit_status(unit_id):
    """Get reading unit status"""
    url = f'{BASE_URL}/wf/api/standard/v2/reading-units/{unit_id}'
    
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    data = response.json()
    status = data.get('status')
    logger.info(f"Reading unit status: {status}")
    return data

def download_result(unit_id):
    """Download result as CSV file"""
    url = f'{BASE_URL}/wf/api/standard/v2/reading-units/{unit_id}/download'
    
    headers = {
        'Authorization': HEADERS['Authorization'],
        'Accept': 'text/csv'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    with open('result.csv', 'wb') as f:
        f.write(response.content)
    
    logger.info("Saved results to result.csv")

def main():
    logger.info("Starting process")
    
    # Get PDF from S3
    pdf_path = get_pdf_from_s3()
    
    # Register reading unit
    unit_id = register_reading_unit(pdf_path)
    
    # Wait for process completion
    while True:
        status_data = get_reading_unit_status(unit_id)
        status = status_data.get('status')
        
        if status == 'completed':
            logger.info("Process completed")
            break
        elif status == 'failed':
            logger.error("Process failed")
            break
        
        logger.info("Processing...")
        time.sleep(10)
    
    # Download results
    if status == 'completed':
        download_result(unit_id)
    
    # Clean up temporary file
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        logger.info("Removed temporary file")

if __name__ == '__main__':
    main() 
