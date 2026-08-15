import '../styles/App.css'
import api from '../src/api.js';
import HeaderBar from '../components/header-bar.jsx';
import SearchResults from '../components/search-results.jsx';
import Sidebar from '../components/sidebar.jsx';
import { useState } from 'react';

function App() {
  const [recipes, setRecipes] = useState([]);
  const [targetItem, setTargetItem] = useState('')
  const [renderSearchResults, setRenderSearchResults] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState('')
  const [inputs, setInputs] = useState([])
  const [page, setPage] = useState('Settings')

  async function fetchSolution() {
    try {
      const res = await api.post('/solve', {
        target_item: targetItem,
        final_recipe: selectedRecipe,
        inputs: inputs
      });
      return res.data;
    } catch (e) {
      console.error('Error fetching solution', e);
    }
  }

  function solve() {
    const solution = fetchSolution().then((data) => {
      console.log(data);
    });
  }

  return (
    <>
      <HeaderBar setRecipes={setRecipes} setTargetItem={setTargetItem} setRenderSearchResults={setRenderSearchResults} />
      {page === 'Settings' ?
        <main className='settings-main'>
          <Sidebar inputs={inputs} setInputs={setInputs} solve={solve} />
          {renderSearchResults &&
            <SearchResults recipes={recipes} targetItem={targetItem} selectedRecipe={selectedRecipe} setSelectedRecipe={setSelectedRecipe} />
          }
        </main>
      :
        <main className='solution-main'>
        </main>
      }
    </>
  )
}

export default App
