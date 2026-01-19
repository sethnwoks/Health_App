import React, { useState, useEffect } from 'react';
import './App.css';

export default function App() {
    // --- Station 3: State Management (The Wallet) ---
    const [token, setToken] = useState(localStorage.getItem('token') || null);
    const [user, setUser] = useState(null);
    const [isRegistering, setIsRegistering] = useState(false);
    const [authData, setAuthData] = useState({ username: '', password: '' });

    const [foodLog, setFoodLog] = useState('');
    const [message, setMessage] = useState('');
    const [calories, setCalories] = useState(null);
    const [parsedItems, setParsedItems] = useState([]);
    const [loading, setLoading] = useState(false);

    // --- Check for returning users ---
    useEffect(() => {
        if (token) {
            fetchUser();
        }
    }, [token]);

    const fetchUser = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setUser(data.username);
            } else {
                handleLogout(); // Token expired or invalid
            }
        } catch (err) {
            handleLogout();
        }
    };

    // --- Station 2: Talking to the Ticket Office (Login/Signup) ---
    const handleAuth = async (e) => {
        e.preventDefault();
        setMessage('');
        const endpoint = isRegistering ? '/register' : '/api/token/';
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(authData),
            });
            const data = await response.json();

            if (response.ok) {
                const jwt = data.access; // SimpleJWT returns 'access' token
                localStorage.setItem('token', jwt);
                setToken(jwt);
                setUser(data.username || authData.username);
            } else {
                setMessage(data.error || data.detail || 'Authentication failed. Please check your credentials.');
            }
        } catch (err) {
            setMessage('Cannot connect to the security server.');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setParsedItems([]);
        setCalories(null);
    };

    // --- The Calculator Logic (Now with added security) ---
    const handleParse = async () => {
        setMessage('');
        setCalories(null);
        setParsedItems([]);
        setLoading(true);

        if (foodLog.trim() === '') {
            setMessage('The food log is empty. Tell me what you ate!');
            setLoading(false);
            return;
        }
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/parse-log`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Flashing the wristband
                },
                body: JSON.stringify({ foodLog: foodLog }),
            });
            const data = await response.json();
            if (!response.ok) {
                setMessage(data.error || 'The bouncer blocked the request. Try logging in again.');
            } else {
                setParsedItems(data.parsed_items);
                setCalories(data.total_calories);
                setMessage('Successfully calculated!');
            }
        } catch (err) {
            setMessage('Connection lost. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    // --- Rendering Logic (The Checkpoint) ---

    // 1. SHOW LOGIN/SIGNUP IF NO TOKEN
    if (!token) {
        return (
            <div className="main-bg">
                <header className="header">
                    <span className="logo">NaijaCal</span>
                </header>
                <main className="main-content">
                    <div className="card">
                        <h1 className="card-title">{isRegistering ? 'Join NaijaCal' : 'Security Check'}</h1>
                        <p style={{ marginBottom: '20px', color: '#666' }}>
                            {isRegistering ? 'Create an account to start tracking your calories.' : 'Please login to access the health calculator.'}
                        </p>
                        <form onSubmit={handleAuth}>
                            <input
                                type="text"
                                placeholder="Username"
                                className="food-textarea"
                                style={{ height: '45px', marginBottom: '12px' }}
                                value={authData.username}
                                onChange={(e) => setAuthData({ ...authData, username: e.target.value })}
                                required
                            />
                            <input
                                type="password"
                                placeholder="Password"
                                className="food-textarea"
                                style={{ height: '45px', marginBottom: '20px' }}
                                value={authData.password}
                                onChange={(e) => setAuthData({ ...authData, password: e.target.value })}
                                required
                            />
                            <button type="submit" className="parse-btn">
                                {isRegistering ? 'Register Now' : 'Enter Application'}
                            </button>
                        </form>
                        <p style={{ marginTop: '20px', color: '#666' }}>
                            {isRegistering ? 'Already a member?' : 'New to the app?'}
                            <span
                                onClick={() => setIsRegistering(!isRegistering)}
                                style={{ color: '#ffa726', cursor: 'pointer', marginLeft: '8px', fontWeight: 'bold' }}
                            >
                                {isRegistering ? 'Login' : 'Sign Up'}
                            </span>
                        </p>
                        {message && <div className="message" style={{ color: '#d32f2f', background: '#ffebee', padding: '10px', borderRadius: '8px', marginTop: '15px' }}>{message}</div>}
                    </div>
                </main>
            </div>
        );
    }

    // 2. SHOW CALCULATOR IF TOKEN EXISTS
    return (
        <div className="main-bg">
            <header className="header">
                <span className="logo">NaijaCal</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <span style={{ color: 'white', fontWeight: '500' }}>Welcome, {user}!</span>
                    <button onClick={handleLogout} className="nav-link" style={{ background: 'rgba(255,255,255,0.15)', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}>
                        Logout
                    </button>
                </div>
            </header>

            <main className="main-content">
                <div className="card">
                    <h1 className="card-title">Calorie Log Parser</h1>
                    <textarea
                        value={foodLog}
                        onChange={(e) => setFoodLog(e.target.value)}
                        className="food-textarea"
                        placeholder="e.g. I had 2 plates of Jollof rice and 1 piece of chicken..."
                        disabled={loading}
                    />
                    <button onClick={handleParse} className="parse-btn" disabled={loading}>
                        {loading ? 'AI is thinking...' : 'Calculate Calories'}
                    </button>

                    {loading && (
                        <div style={{ textAlign: 'center', marginTop: 20 }}>
                            <div className="spinner"></div>
                        </div>
                    )}

                    {message && !loading && <div className="message" style={{ color: '#2e7d32' }}>{message}</div>}

                    {parsedItems.length > 0 && !loading && (
                        <div style={{ marginTop: 24, textAlign: 'left' }}>
                            <strong style={{ color: '#444', display: 'block', marginBottom: '12px' }}>Your Results:</strong>
                            <div className="results-list">
                                {parsedItems.map((item, idx) => (
                                    <div key={idx} className="result-item" style={{ background: '#fff9f0', padding: '12px', borderRadius: '10px', marginBottom: '10px', borderLeft: '4px solid #ffa726' }}>
                                        <div style={{ fontWeight: 'bold', color: '#333' }}>{item.item}</div>
                                        <div style={{ fontSize: '0.9rem', color: '#666' }}>{item.quantity} ➔ <span style={{ color: '#ffa726', fontWeight: 'bold' }}>{item.total_calories} cal</span></div>
                                    </div>
                                ))}
                            </div>
                            <div style={{ marginTop: 20, textAlign: 'center', borderTop: '2px dashed #ffe0b2', paddingTop: '15px' }}>
                                <span style={{ fontSize: '1.4rem', fontWeight: '900', color: '#ff8f00' }}>{calories} Total Calories</span>
                            </div>
                        </div>
                    )}
                </div>
            </main>

            <footer className="footer" style={{ background: 'transparent', color: '#888', boxShadow: 'none' }}>
                © 2025 NaijaCal. Secured with JWT.
            </footer>
        </div>
    );
}
