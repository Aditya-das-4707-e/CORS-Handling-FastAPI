import React, {useEffect, useState} from 'react'

const App = () => {
  const [data, setdata] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(res => res.json())
      .then(data => setdata(data))
      .catch(err => console.log(err))
  }, [])

  return (
    <div style={{padding: "20px"}}>
      <h1>API Data</h1>
      {
        data ? (
          <p>Message : {data.message}</p>
        ) : (
          <p>Loading</p>
        )
      }
    </div>
  )
}

export default App;