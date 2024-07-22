import React from 'react';
import logo from '../../assets/light.jpg'
import './SideBar.css'; // Make sure to create and link this CSS file

const Sidebar = ({ isOpen, onClose }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <button className="close-btn" onClick={onClose}>×</button>
      <img src={logo} alt='logo' className='logo'/>
      <ul>
        <li>Stores</li>
        <li>Products</li>
        <li>About</li>
      </ul>
    </div>
  );
}

export default Sidebar;
