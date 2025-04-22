import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5001/query', {
        query: query
      });      
      setResponse(res.data);
    } catch (err) {
      setResponse({ error: "Backend not reachable or an error occurred." });
    } finally {
      setLoading(false);
    }
  };

  const renderTable = (data) => {
    if (!data || !Array.isArray(data) || data.length === 0) return <p>No results</p>;

    const headers = Object.keys(data[0]);
    return (
      <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse', marginTop: '1rem' }}>
        <thead>
          <tr>{headers.map(h => <th key={h}>{h}</th>)}</tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {headers.map(h => <td key={h}>{row[h]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderCards = (data) => {
    if (!Array.isArray(data) || data.length === 0) return <p>No documents to display</p>;

    return (
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginTop: '1rem' }}>
        {data.map((doc, idx) => (
          <div key={idx} style={{
            border: '1px solid #ccc',
            padding: '1rem',
            width: '250px',
            borderRadius: '8px',
            boxShadow: '2px 2px 10px #ddd'
          }}>
            {Object.entries(doc).map(([key, val]) => (
              <div key={key}><strong>{key}:</strong> {JSON.stringify(val)}</div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>🎬 MovieDB Assistant</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something like: Show top 5 action movies"
        style={{ width: '60%', marginRight: '10px', padding: '8px' }}
      />
      <button onClick={handleSubmit}>Submit</button>

      {loading && <p style={{ marginTop: '1rem' }}>Loading...</p>}

      {response && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Response:</h3>
          {Array.isArray(response.result)
            ? (response.result[0] && response.result[0]._id
                ? renderCards(response.result)     // NoSQL with _id
                : renderTable(response.result))     // SQL
            : <pre>{JSON.stringify(response, null, 2)}</pre>
          }
        </div>
      )}
    </div>
  );
}

export default App;
