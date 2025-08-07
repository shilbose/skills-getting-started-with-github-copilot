# 4-Gram Extraction App

A modern web application built with FastAPI that extracts 4-grams (sequences of 4 consecutive words) from input sentences. The app provides both a beautiful web interface and REST API endpoints for programmatic access.

## Features

- ✨ **Modern Web Interface**: Clean, responsive design with real-time results
- 🔍 **4-Gram Extraction**: Efficiently extracts all 4-word sequences from input text
- 📊 **Statistical Analysis**: Shows word count, total 4-grams, and unique 4-grams
- 📈 **Frequency Analysis**: Identifies and displays repeated 4-grams with counts
- 🚀 **REST API**: Multiple endpoints for integration with other applications
- 🧹 **Text Preprocessing**: Automatic text cleaning and normalization
- 💡 **Example Sentences**: Built-in examples to get started quickly

## What are 4-Grams?

4-grams (also called 4-grams or quadrigrams) are sequences of 4 consecutive words from a text. They are commonly used in:
- Natural Language Processing (NLP)
- Text analysis and linguistics
- Language modeling
- Plagiarism detection
- Text similarity analysis

### Example:
For the sentence: "The quick brown fox jumps over the lazy dog"
The 4-grams would be:
- "the quick brown fox"
- "quick brown fox jumps"
- "brown fox jumps over"
- "fox jumps over the"
- "jumps over the lazy"
- "over the lazy dog"

## Installation

1. **Clone or download the files**:
   ```bash
   # Make sure you have the following files:
   # - fourgram_app.py
   # - templates/index.html
   # - fourgram_requirements.txt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r fourgram_requirements.txt
   ```

3. **Run the application**:
   ```bash
   python fourgram_app.py
   ```

4. **Access the app**:
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

### Web Interface

1. Open your browser and go to http://localhost:8000
2. Enter a sentence in the text area
3. Click "Extract 4-Grams" or use Ctrl+Enter
4. View the results including:
   - Statistics (word count, total 4-grams, unique 4-grams)
   - List of all 4-grams found
   - Frequency analysis (if duplicates exist)

### API Endpoints

#### 1. Web Form Submission
```http
POST /extract
Content-Type: application/x-www-form-urlencoded

sentence=The quick brown fox jumps over the lazy dog
```

#### 2. GET Request (URL Parameter)
```http
GET /api/extract/The%20quick%20brown%20fox%20jumps%20over%20the%20lazy%20dog
```

#### 3. POST Request (JSON)
```http
POST /api/extract
Content-Type: application/json

{
  "sentence": "The quick brown fox jumps over the lazy dog"
}
```

#### 4. Health Check
```http
GET /health
```

### Example API Response

```json
{
  "original_sentence": "The quick brown fox jumps over the lazy dog",
  "cleaned_sentence": "the quick brown fox jumps over the lazy dog",
  "word_count": 9,
  "fourgrams": [
    "the quick brown fox",
    "quick brown fox jumps",
    "brown fox jumps over",
    "fox jumps over the",
    "jumps over the lazy",
    "over the lazy dog"
  ],
  "total_fourgrams": 6,
  "unique_fourgrams": 6,
  "frequency": {
    "the quick brown fox": 1,
    "quick brown fox jumps": 1,
    "brown fox jumps over": 1,
    "fox jumps over the": 1,
    "jumps over the lazy": 1,
    "over the lazy dog": 1
  }
}
```

## Text Processing

The app automatically processes input text by:

1. **Converting to lowercase** for consistency
2. **Removing punctuation** (except apostrophes in contractions)
3. **Normalizing whitespace** (multiple spaces become single spaces)
4. **Trimming** leading and trailing whitespace

## API Integration Examples

### Python (using requests)
```python
import requests

# Using POST with JSON
response = requests.post('http://localhost:8000/api/extract', 
                        json={'sentence': 'Your sentence here'})
data = response.json()
print(f"Found {data['total_fourgrams']} 4-grams")
```

### curl
```bash
# GET request
curl "http://localhost:8000/api/extract/The%20quick%20brown%20fox%20jumps%20over%20the%20lazy%20dog"

# POST request
curl -X POST "http://localhost:8000/api/extract" \
     -H "Content-Type: application/json" \
     -d '{"sentence": "The quick brown fox jumps over the lazy dog"}'
```

### JavaScript (fetch)
```javascript
// Using fetch API
const response = await fetch('/api/extract', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sentence: 'Your sentence here'})
});
const data = await response.json();
console.log(`Found ${data.total_fourgrams} 4-grams`);
```

## Error Handling

The app handles various error conditions:

- **Empty input**: Returns 400 Bad Request
- **Insufficient words**: Returns empty 4-grams list (not an error)
- **Server errors**: Returns 500 Internal Server Error with details

## Technical Details

- **Framework**: FastAPI 0.104.1
- **Template Engine**: Jinja2 3.1.2
- **Server**: Uvicorn 0.24.0
- **Frontend**: Pure HTML, CSS, and JavaScript (no external dependencies)
- **Text Processing**: Python's built-in `re` module

## Browser Compatibility

The web interface works on all modern browsers:
- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance

- **Fast processing**: Optimized for real-time extraction
- **Memory efficient**: Processes text in-place without large intermediate structures
- **Scalable**: Can handle sentences with hundreds of words
- **Responsive**: Web interface provides immediate feedback

## Use Cases

1. **Educational**: Learn about n-grams and text analysis
2. **Research**: Analyze text patterns in documents
3. **Development**: Integrate 4-gram extraction into larger NLP pipelines
4. **Content Analysis**: Identify repeated phrases in text
5. **Language Learning**: Study word patterns in different languages

## Contributing

Feel free to enhance the app by:
- Adding support for different n-gram sizes
- Implementing text file upload
- Adding export functionality (CSV, JSON)
- Improving the UI/UX
- Adding more language support

## License

This project is open source and available under the MIT License.