import '../styles/search-results.css';

export default function SearchResults({recipes, targetItem, handleClickRecipe}) {
  return (
    <div className='search-results'>
      {recipes.length === 0 ?
        <div className='no-recipes'>
          No recipes found for {targetItem}
        </div>
      : recipes.map((recipe) =>
        <div key={recipe.name} className='search-result' onClick={() => handleClickRecipe(recipe.name)}>
          <span className='recipe-name'>{recipe.name}</span>
          <span className='ingredients'>Ingredients: {recipe.ingredients}</span>
          <span className='products'>Products: {recipe.products}</span>
        </div>
      )}
    </div>
  )
}