import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import './App.css';

const originalCsvFilePath = `${process.env.PUBLIC_URL}/Original_sortedWooparooData.csv`;
const luckyCsvFilePath = `${process.env.PUBLIC_URL}/Lucky_sortedWooparooData.csv`;

function App() {
  const [data, setData] = useState([]);
  const [left, setLeft] = useState('');
  const [right, setRight] = useState('');
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState('');
  const [isLucky, setIsLucky] = useState(false);

  useEffect(() => {
    const csvFilePath = isLucky ? luckyCsvFilePath : originalCsvFilePath;
    fetch(csvFilePath)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        return response.text();
      })
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (result) => {
            setData(result.data);
          }
        });
      })
      .catch(error => {
        console.error('Error fetching the CSV file:', error);
      });
  }, [isLucky]);

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
        filteredResults.sort((a, b) => parseFloat(b.Probability) - parseFloat(a.Probability));
        setResults(filteredResults);
        setMessage('');
        console.log('정상 입력되었습니다.');
      } else {
        setMessage('에러: CSV 파일에 해당 조합이 없습니다.');
        setResults([]);
        console.error('에러: CSV 파일에 해당 조합이 없습니다.');
      }
    }
  };

  const toggleLucky = () => {
    setIsLucky(!isLucky);
    setResults([]);
    setMessage('');
  };

  return (
    <div className="App">
      <div className="header">
        <h1>우파루 크로스 확률 검색기</h1>
        <div className="made-by">made by jeok K</div>
      </div>
      <div>
        <p>현재 상태: {isLucky ? 'Lucky' : 'Original'}</p>
        <button onClick={toggleLucky}>
          {isLucky ? 'Switch to Original' : 'Switch to Lucky'}
        </button>
      </div>
      <div>
        <label>
          왼쪽 우파루  
          <input type="text" value={left} onChange={(e) => setLeft(e.target.value)} />
        </label>
        <label>
          오른쪽 우파루
          <input type="text" value={right} onChange={(e) => setRight(e.target.value)} />
        </label>
        <button onClick={handleSearch}>Search</button>
      </div>
      <div>
        {message && <p>{message}</p>}
        {results.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>결과 우파루</th>
                <th>확률(%)</th>
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
