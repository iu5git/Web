# Методические указания по Short Polling


### Пример Short Polling на React
```JavaScript
import React from 'react';

import { useEffect, useState } from 'react';

export default function App() {
  let [jokes, setJokes] = useState('Initial');

  async function fetchJokes() {
    let a = await fetch('https://api.chucknorris.io/jokes/random');
    let b = await a.json();
    setJokes(b.value);
  }

// Below function works like compomentWillUnmount and hence it clears the timeout
  useEffect(() => {
    let id = setTimeout(fetchJokes, 2000);
    return () => clearTimeout(id);
  });

  return <div>{jokes}</div>;
}
```
