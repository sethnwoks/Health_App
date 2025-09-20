import React, { useState } from 'react';
import './App.css';

const HERB_DATABASE = {
  ginger: "Anti-inflammatory, aids digestion, relieves nausea, boosts immunity.",
  turmeric: "Contains curcumin, powerful anti-inflammatory and antioxidant.",
  garlic: "Supports heart health, boosts immunity, has antibacterial properties.",
  neem: "Antibacterial, antifungal, supports skin and oral health.",
  moringa: "Rich in vitamins, minerals, antioxidants; supports metabolism.",
  bitterleaf: "May help regulate blood sugar, supports liver health.",
  scent_leaf: "Antibacterial, supports digestion, relieves cough.",
  clove: "Antimicrobial, relieves toothache, aids digestion.",
  hibiscus: "Rich in antioxidants, supports heart health, lowers blood pressure.",
  aloe: "Soothes skin, aids digestion, anti-inflammatory.",
};

export default function HerbalFacts() {
  const [herb, setHerb] = useState('');
  const [benefit, setBenefit] = useState('');

  const handleCheck = () => {
    const key = herb.trim().toLowerCase();
    if (HERB_DATABASE[key]) {
      setBenefit(HERB_DATABASE[key]);
    } else {
      setBenefit("No information found for this herb. Please consult the herbalist.");
    }
  };

  return (
    <div className="card" style={{ margin: '40px auto', maxWidth: 600 }}>
      <h2 className="card-title">The Herbal Facts</h2>
      <p style={{ fontStyle: 'italic', color: '#888', marginBottom: 10 }}>
        Curated with insights from Mr. Adebowale, Traditional Nutritionist Expert.
      </p>
      <p>
        Type in an herb name (e.g., <b>ginger</b>, <b>turmeric</b>) to see its health benefit. This feature leverages our team's subject matter expert (the herbalist).
      </p>
      <div style={{ margin: '18px 0' }}>
        <input
          type="text"
          value={herb}
          onChange={e => setHerb(e.target.value)}
          placeholder="Enter herb name..."
          className="food-textarea"
          style={{ width: '70%', marginRight: 8, height: 36 }}
        />
        <button className="parse-btn" onClick={handleCheck}>Check</button>
      </div>
      {benefit && (
        <div className="message" style={{ textAlign: 'left' }}>
          <b>Benefit:</b> {benefit}
        </div>
      )}
      <div style={{ marginTop: 24, textAlign: 'left' }}>
        <b>Popular Herbs & Benefits:</b>
        <ul>
          {Object.entries(HERB_DATABASE).map(([herb, benefit]) => (
            <li key={herb}><b>{herb}</b>: {benefit}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}