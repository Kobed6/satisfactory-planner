import '../styles/header-bar.css';
import Logo from './logo.jsx';
import Search from './search.jsx';

export default function HeaderBar({setRecipes, setTargetItem, setRenderSearchResults}) {
  return (
    <span className='header-bar'>
      <Logo />
      <Search setRecipes={setRecipes} setTargetItem={setTargetItem} setRenderSearchResults={setRenderSearchResults} />
    </span>
  );
}