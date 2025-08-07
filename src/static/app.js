// 4-Gram Finder Application
class FourGramFinder {
    constructor() {
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        // Input elements
        this.sentenceInput = document.getElementById('sentence-input');
        this.extractBtn = document.getElementById('extract-btn');
        this.clearBtn = document.getElementById('clear-btn');

        // Results elements
        this.resultsSection = document.getElementById('results-section');
        this.loadingSection = document.getElementById('loading-section');
        this.errorSection = document.getElementById('error-section');
        this.errorText = document.getElementById('error-text');
        this.originalSentence = document.getElementById('original-sentence');
        this.totalGrams = document.getElementById('total-grams');
        this.fourGramsContainer = document.getElementById('four-grams-container');
    }

    bindEvents() {
        this.extractBtn.addEventListener('click', () => this.extractFourGrams());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        
        // Allow Enter key to trigger extraction
        this.sentenceInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.extractFourGrams();
            }
        });

        // Auto-resize textarea
        this.sentenceInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
    }

    autoResizeTextarea() {
        this.sentenceInput.style.height = 'auto';
        this.sentenceInput.style.height = this.sentenceInput.scrollHeight + 'px';
    }

    async extractFourGrams() {
        const sentence = this.sentenceInput.value.trim();
        
        if (!sentence) {
            this.showError('Please enter a sentence to extract 4-grams.');
            return;
        }

        if (sentence.split(' ').length < 4) {
            this.showError('The sentence must contain at least 4 words to extract 4-grams.');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const response = await fetch('/extract-four-grams', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sentence: sentence })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to extract 4-grams');
            }

            const data = await response.json();
            this.displayResults(data);
        } catch (error) {
            console.error('Error extracting 4-grams:', error);
            this.showError(error.message || 'An error occurred while extracting 4-grams.');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(data) {
        // Display original sentence
        this.originalSentence.textContent = data.sentence;
        
        // Update total count
        this.totalGrams.textContent = data.total_grams;
        
        // Clear and populate 4-grams
        this.fourGramsContainer.innerHTML = '';
        
        if (data.four_grams.length === 0) {
            this.fourGramsContainer.innerHTML = `
                <div class="gram-item" style="grid-column: 1 / -1; text-align: center; color: #6c757d;">
                    <i class="fas fa-info-circle"></i>
                    No 4-grams found in this sentence.
                </div>
            `;
        } else {
            data.four_grams.forEach((gram, index) => {
                const gramElement = document.createElement('div');
                gramElement.className = 'gram-item';
                gramElement.innerHTML = `
                    <span style="font-weight: 600; color: #667eea; margin-right: 10px;">#${index + 1}</span>
                    ${gram}
                `;
                this.fourGramsContainer.appendChild(gramElement);
            });
        }

        this.showResults();
        
        // Smooth scroll to results
        this.resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    clearAll() {
        this.sentenceInput.value = '';
        this.hideResults();
        this.hideError();
        this.autoResizeTextarea();
        this.sentenceInput.focus();
    }

    showLoading() {
        this.loadingSection.style.display = 'flex';
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
    }

    showResults() {
        this.resultsSection.style.display = 'block';
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorSection.style.display = 'block';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        this.errorSection.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FourGramFinder();
    
    // Add some example sentences for quick testing
    const exampleSentences = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Natural language processing helps computers understand human language",
        "Data science combines statistics programming and domain expertise"
    ];
    
    // Add example button functionality
    const addExampleButton = () => {
        const exampleBtn = document.createElement('button');
        exampleBtn.className = 'clear-btn';
        exampleBtn.innerHTML = '<i class="fas fa-lightbulb"></i> Try Example';
        exampleBtn.style.marginTop = '10px';
        exampleBtn.addEventListener('click', () => {
            const randomExample = exampleSentences[Math.floor(Math.random() * exampleSentences.length)];
            document.getElementById('sentence-input').value = randomExample;
            document.getElementById('sentence-input').dispatchEvent(new Event('input'));
        });
        
        const inputActions = document.querySelector('.input-actions');
        inputActions.appendChild(exampleBtn);
    };
    
    addExampleButton();
});
