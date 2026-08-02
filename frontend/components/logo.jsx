import '../styles/logo.css';
import logo_src from '../src/assets/satisfactory_logo.png';

export default function Logo() {
  return (
    <div className='logo'>
      <img src={logo_src} width='25%' />
      <h1 style={{margin: 0}}>Planner</h1>
    </div>
  );
}