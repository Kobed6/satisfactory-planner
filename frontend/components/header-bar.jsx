import '../styles/header-bar.css';
import Logo from './logo.jsx';
import Search from './search.jsx';

export default function HeaderBar() {
  return (
    <span className='header-bar'>
      <Logo />
      <Search />
    </span>
  );
}