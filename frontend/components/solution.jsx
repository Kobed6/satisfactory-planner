import '../styles/solution.css'
import backArrow from '../src/assets/arrow_back.svg'
import api from '../src/api.js';
import { useState } from 'react'

export default function Solution({setPage, data, targetItem, selectedRecipe, inputs}) {
  const [tab, setTab] = useState('Recipes');
  const [recipesData, setRecipesData] = useState(data);
  const [itemsData, setItemsData] = useState({});
  const [extrasData, setExtrasData] = useState({});

  async function fetchItemsSolution() {
    try {
      const res = await api.post('/solve/items', {
        target_item: targetItem,
        final_recipe: selectedRecipe,
        inputs: inputs
      });
      setItemsData(res.data);
    } catch (e) {
      console.error('Error fetching items solution', e);
    }
  }

  async function fetchExtrasSolution() {
    try {
      const res = await api.post('/solve/extraneous', {
        target_item: targetItem,
        final_recipe: selectedRecipe,
        inputs: inputs
      });
      setExtrasData(res.data);
    } catch (e) {
      console.error('Error fetching unused outputs solution', e);
    }
  }

  function TabBar({setPage}) {
    return (
      <div className='tab-bar'>
        <img className='arrow tab' src={backArrow} onClick={() => setPage('Settings')}/>
        <span className={tab === 'Recipes' ? 'active tab' : 'tab'} onClick={() => setTab('Recipes')}>Recipes</span>
        <span className={tab === 'Items' ? 'active tab' : 'tab'} onClick={() => {if (Object.keys(itemsData).length === 0) fetchItemsSolution(); setTab('Items')}}>Items</span>
        <span className={tab === 'Unused' ? 'active tab' : 'tab'} onClick={() => {if (Object.keys(extrasData).length === 0) fetchExtrasSolution(); setTab('Unused')}}>Unused Outputs</span>
        <span className={tab === 'Power' ? 'active tab' : 'tab'} onClick={() => setTab('Power')}>Power Consumption</span>
      </div>
    )
  }

  function RecipeCard({recipe, ingredients, products, buildings}) {
    return (
      <span className='card'>
        <span>{recipe}</span>
        {ingredients.map((ingredient, index) => <span key={index}>{ingredient}</span>)}
        {products.map((product, index) => <span key={index}>{product}</span>)}
        <span>{buildings}</span>
      </span>
    )
  }

  function ItemCard({item, amount}) {
    return (
      <span className='card'>
        <span>{item}</span>
        <span>Total production: {amount}</span>
      </span>
    )
  }

  function ExtrasCard({item, amount}) {
    return (
      <span className='card'>
        <span>{item}</span>
        <span>Total unused: {amount}</span>
      </span>
    )
  }

  return (
    <div className='solution'>
      <TabBar setPage={setPage} />
      {tab === 'Recipes' ?
      <div className='cards-div'>
        {recipesData.map(([recipeName, ingredientStrings, productStrings, buildings]) =>
        <RecipeCard key={recipeName} recipe={recipeName} ingredients={ingredientStrings} products={productStrings} buildings={buildings} />)}
      </div>
      : tab === 'Items' ?
      <div className='cards-div'>
        {Object.entries(itemsData).map(([item, amount]) => <ItemCard key={item} item={item} amount={amount} />)}
      </div>
      : tab === 'Unused' ?
      <div className='cards-div'>
        {extrasData ? 'No unused outputs' : Object.entries(extrasData).map(([item, amount]) => <ExtrasCard key={item} item={item} amount={amount} />)}
      </div>
      : tab === 'Power' ?
      <div className='cards-div'>
      </div>
      :
      <div className='not-found'>
        Page not found
      </div>
      }
    </div>
  )
}