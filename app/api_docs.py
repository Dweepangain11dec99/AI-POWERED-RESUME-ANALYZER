"""
Custom OpenAPI documentation
"""
from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    """Generate custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI-Powered Resume Analyzer",
        version="1.0.0",
        description="Resume analysis and ATS scoring platform",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema
