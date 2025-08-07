"""
4-Gram Finder API

A FastAPI application that extracts 4-grams (4-word sequences) from input sentences.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os
from pathlib import Path
import re

app = FastAPI(title="4-Gram Finder API",
              description="API for extracting 4-grams from sentences")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

class SentenceRequest(BaseModel):
    sentence: str

class FourGramResponse(BaseModel):
    sentence: str
    four_grams: list[str]
    total_grams: int

def extract_four_grams(sentence: str) -> list[str]:
    """
    Extract all 4-grams from a given sentence.
    
    Args:
        sentence: Input sentence as string
        
    Returns:
        List of 4-grams found in the sentence
    """
    # Clean and tokenize the sentence
    # Remove extra whitespace and split into words
    words = re.findall(r'\b\w+\b', sentence.lower())
    
    # Extract 4-grams
    four_grams = []
    for i in range(len(words) - 3):
        gram = ' '.join(words[i:i+4])
        four_grams.append(gram)
    
    return four_grams

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.post("/extract-four-grams", response_model=FourGramResponse)
def extract_four_grams_endpoint(request: SentenceRequest):
    """
    Extract 4-grams from the provided sentence.
    
    Args:
        request: SentenceRequest containing the input sentence
        
    Returns:
        FourGramResponse with the sentence, extracted 4-grams, and count
    """
    if not request.sentence.strip():
        raise HTTPException(status_code=400, detail="Sentence cannot be empty")
    
    # Check if sentence has at least 4 words
    words = re.findall(r'\b\w+\b', request.sentence.lower())
    if len(words) < 4:
        raise HTTPException(status_code=400, detail="Sentence must contain at least 4 words to extract 4-grams")
    
    four_grams = extract_four_grams(request.sentence)
    
    return FourGramResponse(
        sentence=request.sentence,
        four_grams=four_grams,
        total_grams=len(four_grams)
    )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "4-Gram Finder API is running"}
