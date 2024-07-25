import React from 'react';
import logo from '../../assets/light.jpg'
import { Link } from 'react-router-dom';
import './SideBar.css'; // Make sure to create and link this CSS file

const Sidebar = ({ isOpen, onClose }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <button className="close-btn" onClick={onClose}>×</button>
      <Link to="/">
        <img src={logo} alt='logo' className='logo'/>
      </Link>
      <nav>
          <ul>
              <Link to="/products" >Products</Link>
              <Link to="/about" >About</Link>
          </ul>
        </nav>
    </div>
  );
}

export default Sidebar;
