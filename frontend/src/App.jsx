  import { useState } from 'react';

function App() {
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const generateSummary = async () => {
    setLoading(true);
    setSummary('');
    
    const response = await fetch('http://localhost:5000/stream');
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      setSummary(prev => prev + chunk);
    }
    setLoading(false);
  };
return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h1>Policy Lifecycle Manager</h1>
      <button onClick={generateSummary} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Summary'}
      </button>
      <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '20px' }}>
        {summary || 'Click the button to generate a summary...'}
      </div>
    </div>
  );
}

export default App;
