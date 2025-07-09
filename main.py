from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from scripts.agents import doctor
from scripts.task import help_patients
from scripts.tools import BloodTestReportTool
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import markdown
from DB.redis import RedisQueue as cache
from DB.pg import DBManager
import asyncio
from processor import main as processor_main

templates = Jinja2Templates(directory="templates")
POST_DIR = "posts"
SELF_URL = os.environ.get('SELF_URL', 'http://localhost:8000')
app = FastAPI(title="Blood Test Report Analyser")
port = int(os.environ.get("PORT", 8000))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        q = cache('reports')
        fileContent = await BloodTestReportTool.read_data_tool(file_path)

        q.enqueue({ 'slug': file_id, 'query': query.strip(), 'fileContent': fileContent })

        return {
            "status": "success",
            "file_processing": file.filename,
            "file_id": file_id,
            "response": "Your PDF is being processed by our medical team. You will receive a detailed report shortly.",
            "post_url": f"{SELF_URL}/report/{file_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.get("/report/{slug}", response_class=HTMLResponse)
async def read_blog(request: Request, slug: str):
    reportData = None
    template = None
    loadingState = False
    try:
        db = DBManager()
        reportData = await db.fetch_by_slug(slug)
    except Exception as e:
        pass
    if not reportData:
        md_content = "Your PDF is being processed by our medical team. You will receive a detailed report shortly."
        template = "loading.html"
        loadingState = True
    else:
        md_content = reportData.text
        template = "base.html"
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])
    return templates.TemplateResponse(template, {
        "request": request,
        "title": 'Report',
        "content": html_content,
        "loading": loadingState
    })

@app.on_event("startup")
async def start_background_processor():
    print("Starting background processor...")
    asyncio.create_task(processor_main())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)