import os
import time
import boto3
import requests
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv('INSIDE_AI_API_KEY')
ACCOUNT_ID = os.getenv('INSIDE_AI_ACCOUNT_ID')
WORKFLOW_ID = os.getenv('INSIDE_AI_WORKFLOW_ID')

BASE_URL = f'https://{ACCOUNT_ID}.dx-suite.com'
HEADERS = {
    'apikey': API_KEY,
    'Accept': 'application/json'
}

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_KEY = os.getenv('S3_PDF_KEY')

session = requests.Session()
session.headers.update(HEADERS)

def get_pdf_from_s3() -> str:
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
    url = f'{BASE_URL}/wf/api/standard/v2/workflows/{WORKFLOW_ID}/units'
    with open(pdf_path, 'rb') as pdf_file:
        files = {
            'files': ('document.pdf', pdf_file, 'application/pdf')
        }
        response = session.post(url, files=files)
    response.raise_for_status()
    unit_id = response.json()['unitId']
    logger.info(f"Registered reading unit (unitId: {unit_id})")
    return unit_id

def get_reading_unit_status(unit_id: str) -> dict:
    url = f'{BASE_URL}/wf/api/standard/v2/units/status?unitId={unit_id}'
    response = session.get(url)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        status = data[0].get('dataProcessingStatus')
        logger.info(f"Reading unit status: {status}")
        return data[0]
    logger.info("No status information found")
    return {}

def download_result(unit_id: str) -> None:
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
        pdf_path = get_pdf_from_s3()
        unit_id = register_reading_unit(pdf_path)
        
        while True:
            status_data = get_reading_unit_status(unit_id)
            status = status_data.get('dataProcessingStatus')
            
            if status == 'completed':
                logger.info("Process completed")
                break
            elif status == 'failed':
                logger.error("Process failed")
                break
            
            logger.info("Processing...")
            time.sleep(10)
        
        if status == 'completed':
            download_result(unit_id)
    
    except Exception as e:
        logger.exception("An error occurred during processing")
    
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info("Removed temporary file")

if __name__ == '__main__':
    main()
