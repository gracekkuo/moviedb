import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:5000/query', {
        query: query,  // ✅ this aligns with request.json.get("query", "")
      });
      setResponse(res.data);  // ✅ response is already a JSON dict
    } catch (err) {
      console.error(err);
      setResponse({ error: "Backend not reachable or error occurred" });
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>🎬 MovieDB Assistant</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Try: List all movies from 2012"
        style={{ width: '60%', marginRight: '10px', padding: '8px' }}
      />
      <button onClick={handleSubmit}>Submit</button>

      {response && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
