import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import './App.css';

const csvFilePath = '/Sorted_Wooparoo_Data.csv';

function App() {
  const [data, setData] = useState([]);
  const [left, setLeft] = useState('');
  const [right, setRight] = useState('');
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch and parse the CSV file
    fetch(csvFilePath)
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (result) => {
            setData(result.data);
          }
        });
      });
  }, []);

  const handleSearch = () => {
    console.log('버튼이 클릭되었습니다.');

    const leftExists = data.some(row => row.Left === left);
    const rightExists = data.some(row => row.Right === right);

    if (!leftExists && !rightExists) {
      setMessage('에러: Left와 Right 값이 모두 없습니다.');
      setResults([]);
      console.error('에러: Left와 Right 값이 모두 없습니다.');
    } else if (!leftExists) {
      setMessage('에러: Left 값이 없습니다.');
      setResults([]);
      console.error('에러: Left 값이 없습니다.');
    } else if (!rightExists) {
      setMessage('에러: Right 값이 없습니다.');
      setResults([]);
      console.error('에러: Right 값이 없습니다.');
    } else {
      const filteredResults = data.filter(row => row.Left === left && row.Right === right);
      if (filteredResults.length > 0) {
        setResults(filteredResults);
        setMessage('정상 입력되었습니다.');
        console.log('정상 입력되었습니다.');
      } else {
        setMessage('에러: CSV 파일에 해당 조합이 없습니다.');
        setResults([]);
        console.error('에러: CSV 파일에 해당 조합이 없습니다.');
      }
    }
  };

  return (
    <div className="App">
      <h1>Wooparoo Probability Finder</h1>
      <div>
        <label>
          Left:
          <input type="text" value={left} onChange={(e) => setLeft(e.target.value)} />
        </label>
        <label>
          Right:
          <input type="text" value={right} onChange={(e) => setRight(e.target.value)} />
        </label>
        <button onClick={handleSearch}>Search</button>
      </div>
      <div>
        <h2>Results</h2>
        {message && <p>{message}</p>}
        {results.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Wooparoo</th>
                <th>Probability</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, index) => (
                <tr key={index}>
                  <td>{result.Wooparoo}</td>
                  <td>{result.Probability}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;
