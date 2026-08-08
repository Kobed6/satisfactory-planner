import '../styles/App.css'
import api from '../src/api.js';
import HeaderBar from '../components/header-bar.jsx';
import SearchResults from '../components/search-results.jsx';
import { useState } from 'react';

function App() {
  const [recipes, setRecipes] = useState([]);
  const [targetItem, setTargetItem] = useState('')
  const [renderSearchResults, setRenderSearchResults] = useState(false);

  async function fetchSolution(targetItem, recipeName) {
    try {
      const res = await api.get('/solve', {
        params: {
          target_item: targetItem,
          final_recipe: recipeName
        }
      });
      return res.data;
    } catch (e) {
      console.error('Error fetching solution', e);
    }
  }

  function handleClickRecipe(clickedRecipe) {
    const solution = fetchSolution(clickedRecipe).then((data) => {
      console.log(data);
    });
  }

  return (
    <>
      <HeaderBar setRecipes={setRecipes} setTargetItem={setTargetItem} setRenderSearchResults={setRenderSearchResults} />
      <main>
        {renderSearchResults &&
          <SearchResults recipes={recipes} targetItem={targetItem} handleClickRecipe={handleClickRecipe} />
        }
      </main>
    </>
  )
}

export default App
