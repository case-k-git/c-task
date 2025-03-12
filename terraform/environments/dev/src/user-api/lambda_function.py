import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    シンプルなエコーバック関数
    """
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from User API',
            'event': event
        })
    } 
