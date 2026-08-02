import '../styles/search.css';
import api from '../src/api.js';
import search_icon from '../src/assets/search_icon.png'
import { useState } from 'react';

export default function Search() {
  const [query, setQuery] = useState('');
  const [recipes, setRecipes] = useState([]);
  const [renderResults, setRenderResults] = useState(false);

  async function fetchRecipes(query) {
    try {
      const res = await api.get('/search', {
        params: {
          input: query
        }
      });
      setRecipes(res.data);
    } catch (e) {
      console.error('Error fetching recipes', e);
    }
  }

  function handleChange(newQuery) {
    setQuery(newQuery);
    fetchRecipes(newQuery);
  }

  function handleBlur() {
    setTimeout(() =>
      setRenderResults(false)
    , 200);
  }

  function handleClickRecipe(clickedRecipe) {
    console.log(clickedRecipe)
  }

  return (
    <div className='search-container'>
      <span className='search-bar'>
        <input
          type='text'
          value={query}
          onClick={() => {fetchRecipes(query); setRenderResults(true)}}
          onChange={(e) => handleChange(e.target.value)}
          placeholder='Search...'
          onBlur={() => handleBlur()}
        />
        <img src={search_icon} />
      </span>
      {renderResults &&
        <ul>
          {recipes.map((recipe) =>
            <li key={recipe} onClick={(e) => handleClickRecipe(e.target.textContent)}>{recipe}</li>
          )}
        </ul>
      }
    </div>
  );
}