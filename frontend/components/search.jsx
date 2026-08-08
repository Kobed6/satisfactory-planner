import '../styles/search.css';
import api from '../src/api.js';
import search_icon from '../src/assets/search_icon.png'
import { useState } from 'react';

export default function Search({setRecipes, setTargetItem, setRenderSearchResults}) {
  const [query, setQuery] = useState('');
  const [items, setItems] = useState([]);
  const [renderItems, setRenderItems] = useState(false);

  async function fetchItems(query) {
    try {
      const res = await api.get('/search-items', {
        params: {
          input: query
        }
      });
      setItems(res.data);
    } catch (e) {
      console.error('Error fetching items', e);
    }
  }

  async function fetchRecipes(clickedItem) {
    try {
      const res = await api.get('/search-recipes', {
        params: {
          item: clickedItem
        }
      });
      setRecipes(res.data);
      return res.data
    } catch (e) {
      console.error('Error fetching recipes', e);
    }
  }

  function handleChange(newQuery) {
    setQuery(newQuery);
    fetchItems(newQuery);
  }

  function handleBlur() {
    setTimeout(() =>
      setRenderItems(false)
    , 200);
  }

  function handleClickItem(clickedItem) {
    setTargetItem(clickedItem)
    const recipeResults = fetchRecipes(clickedItem).then(() => {
      setRenderSearchResults(true)
    });
  }

  return (
    <div className='search-container'>
      <span className='search-bar'>
        <input
          type='text'
          value={query}
          onClick={() => {fetchItems(query); setRenderItems(true)}}
          onChange={(e) => handleChange(e.target.value)}
          placeholder='Search...'
          onBlur={() => handleBlur()}
        />
        <img src={search_icon} />
      </span>
      {renderItems &&
        <ul>
          {items.map((item) =>
            <li key={item} onClick={(e) => handleClickItem(e.target.textContent)}>{item}</li>
          )}
        </ul>
      }
    </div>
  );
}