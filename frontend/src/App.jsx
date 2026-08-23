import '../styles/App.css'
import api from '../src/api.js';
import HeaderBar from '../components/header-bar.jsx';
import SearchResults from '../components/search-results.jsx';
import Sidebar from '../components/sidebar.jsx';
import Solution from '../components/solution.jsx';
import { useState } from 'react';

function App() {
  const [recipes, setRecipes] = useState([]);
  const [targetItem, setTargetItem] = useState('');
  const [renderSearchResults, setRenderSearchResults] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState('');
  const [inputs, setInputs] = useState([]);
  const [page, setPage] = useState('Settings');
  const [solutionData, setSolutionData] = useState({});

  async function fetchRecipesSolution() {
    try {
      const res = await api.post('/solve/recipes', {
        target_item: targetItem,
        final_recipe: selectedRecipe,
        inputs: inputs
      });
      return res.data;
    } catch (e) {
      console.error('Error fetching solution', e);
    }
  }

  function recipesSolve() {
    if (selectedRecipe === '') {
      alert('Select a recipe');
    }
    else {
      const solution = fetchRecipesSolution().then((data) => {
        setPage('Solution');
        setSolutionData(data);
      });
    }
  }

  return (
    <>
      <HeaderBar setRecipes={setRecipes} setTargetItem={setTargetItem} setRenderSearchResults={setRenderSearchResults} />
      {page === 'Settings' ?
        <main className='settings-main'>
          <Sidebar inputs={inputs} setInputs={setInputs} solve={recipesSolve} />
          {renderSearchResults &&
            <SearchResults recipes={recipes} targetItem={targetItem} selectedRecipe={selectedRecipe} setSelectedRecipe={setSelectedRecipe} />
          }
        </main>
      : page === 'Solution' ?
        <main className='solution-main'>
          <Solution setPage={setPage} data={solutionData} targetItem={targetItem} selectedRecipe={selectedRecipe} inputs={inputs} />
        </main>
      :
        <div className='not-found'>
          Page not found
        </div>
      }
    </>
  )
}

export default App
