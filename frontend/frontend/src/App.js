import React, { useState } from 'react';
import './App.css';
import HerbalFacts from './HerbalFacts';

// Main App component that renders the entire application.
// This is a functional component, which is a modern way to write React components.
export default function App() {
  const [page, setPage] = useState('CalorieParser');
  const [foodLog, setFoodLog] = useState('');
  const [message, setMessage] = useState('');
  const [calories, setCalories] = useState(null);
  const [parsedItems, setParsedItems] = useState([]);
  const [loading, setLoading] = useState(false); // Add this

  // This function handles the button click event.
  // It takes the text from the textarea and simulates parsing it.
  const handleParse = async () => {
    setMessage('');
    setCalories(null);
    setParsedItems([]);
    setLoading(true); // Start loading
    
    if (foodLog.trim() === '') {
      setMessage('Please paste your food log first.');
      setLoading(false); // Stop loading
      return;
    }
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/parse-log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ foodLog: foodLog }),
      });
      const data = await response.json();
      if (!response.ok) {
        setMessage(data.error || 'Error parsing food log.');
      } else {
        setParsedItems(data.parsed_items);
        setCalories(data.total_calories);
        setMessage('Parsed successfully!');
      }
    } catch (err) {
      setMessage('Could not connect to backend.');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    // The main container for the entire page.
    // Tailwind classes are used here for styling.
    // 'min-h-screen' ensures the container takes up at least the full viewport height.
    <div className="main-bg">

      {/* Header */}
      <header className="header">
        <span className="logo">NaijaCal</span>
        <nav>
          <ul className="nav-list">
            <li>
              <a
                href="#"
                className={`nav-link${page === 'CalorieParser' ? ' nav-link-active' : ''}`}
                onClick={() => setPage('CalorieParser')}
              >
                Calorie Parser
              </a>
            </li>
            <li>
              <a
                href="#"
                className={`nav-link${page === 'HerbalFacts' ? ' nav-link-active' : ''}`}
                onClick={() => setPage('HerbalFacts')}
              >
                Herbal Facts
              </a>
            </li>
          </ul>
        </nav>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {page === 'CalorieParser' && (
          <div className="card">
            <h1 className="card-title">Paste & Parse Food Log</h1>
            <textarea
              value={foodLog}
              onChange={(e) => setFoodLog(e.target.value)}
              className="food-textarea"
              placeholder="Paste your food log here..."
              disabled={loading} // Disable textarea while loading
            />
            <button
              onClick={handleParse}
              className="parse-btn"
              disabled={loading} // Disable button while loading
            >
              {loading ? 'Parsing...' : 'Parse'} {/* Show different text */}
            </button>
            
            {/* Loading Spinner */}
            {loading && (
              <div style={{ textAlign: 'center', marginTop: 16 }}>
                <div className="spinner"></div>
                <p>Processing your food log...</p>
              </div>
            )}
            
            {message && !loading && (
              <div className="message">{message}</div>
            )}
            {parsedItems.length > 0 && !loading && (
              <div style={{ marginTop: 16, textAlign: 'left' }}>
                <strong>Detected foods:</strong>
                <ul>
                  {parsedItems.map((item, idx) => (
                    <li key={idx}>
                      <div>
                        <strong>{item.item}</strong> — {item.quantity}
                      </div>
                      <div>
                        Total Calories: {item.total_calories} | Calories Eaten Today: {item.calories_today}
                      </div>
                    </li>
                  ))}
                </ul>
                <div style={{ marginTop: 8, fontWeight: 'bold' }}>
                  Total Calories (all foods): {calories}
                </div>
              </div>
            )}
          </div>
        )}
        {page === 'HerbalFacts' && <HerbalFacts />}
      </main>

      {/* Footer */}
      <footer className="footer">
        © 2025 NaijaCal. For demo only.
      </footer>
    </div>
  );
}
