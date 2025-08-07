"""
4-Gram Extraction App

A FastAPI application that extracts 4-grams (sequences of 4 consecutive words) 
from input sentences. Provides both web interface and API endpoints.
"""

from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import re
from typing import List, Dict
import string

app = FastAPI(
    title="4-Gram Extraction App",
    description="Extract 4-grams from sentences",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation except spaces and apostrophes
    text = re.sub(r'[^\w\s\']', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()

def extract_fourgrams(sentence: str) -> List[str]:
    """
    Extract all 4-grams from a given sentence.
    
    Args:
        sentence (str): Input sentence
        
    Returns:
        List[str]: List of 4-grams found in the sentence
    """
    if not sentence or not sentence.strip():
        return []
    
    # Clean the text
    cleaned_text = clean_text(sentence)
    
    # Split into words
    words = cleaned_text.split()
    
    # If we have fewer than 4 words, no 4-grams possible
    if len(words) < 4:
        return []
    
    # Extract 4-grams
    fourgrams = []
    for i in range(len(words) - 3):
        fourgram = ' '.join(words[i:i+4])
        fourgrams.append(fourgram)
    
    return fourgrams

def get_fourgram_stats(sentence: str) -> Dict:
    """
    Get detailed statistics about 4-grams in the sentence.
    
    Args:
        sentence (str): Input sentence
        
    Returns:
        Dict: Statistics including count, unique count, and frequency
    """
    fourgrams = extract_fourgrams(sentence)
    
    # Count frequency of each 4-gram
    frequency = {}
    for fg in fourgrams:
        frequency[fg] = frequency.get(fg, 0) + 1
    
    return {
        "original_sentence": sentence,
        "cleaned_sentence": clean_text(sentence),
        "word_count": len(clean_text(sentence).split()),
        "fourgrams": fourgrams,
        "total_fourgrams": len(fourgrams),
        "unique_fourgrams": len(set(fourgrams)),
        "frequency": frequency
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract", response_class=JSONResponse)
async def extract_fourgrams_api(sentence: str = Form(...)):
    """
    API endpoint to extract 4-grams from a sentence.
    
    Args:
        sentence (str): Input sentence
        
    Returns:
        JSON response with 4-grams and statistics
    """
    try:
        if not sentence or not sentence.strip():
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        stats = get_fourgram_stats(sentence)
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sentence: {str(e)}")

@app.get("/api/extract/{sentence}")
async def extract_fourgrams_get(sentence: str):
    """
    GET API endpoint to extract 4-grams from a sentence.
    
    Args:
        sentence (str): Input sentence (URL encoded)
        
    Returns:
        JSON response with 4-grams and statistics
    """
    try:
        if not sentence or not sentence.strip():
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        stats = get_fourgram_stats(sentence)
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sentence: {str(e)}")

@app.post("/api/extract")
async def extract_fourgrams_post(data: dict):
    """
    POST API endpoint to extract 4-grams from a sentence.
    
    Args:
        data (dict): JSON data containing 'sentence' key
        
    Returns:
        JSON response with 4-grams and statistics
    """
    try:
        sentence = data.get("sentence", "")
        if not sentence or not sentence.strip():
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        stats = get_fourgram_stats(sentence)
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sentence: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "4-Gram extraction app is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)