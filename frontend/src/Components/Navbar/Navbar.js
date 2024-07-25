import React, {useState } from 'react'
import { Link } from 'react-router-dom';
import useWindowSize from '../WindowsSize/windowsSize';
import Sidebar from '../SideBar/SideBar';

import logo from '../../assets/download.png'
import search from '../../assets/search-w.png'
import { FaUser } from "react-icons/fa";
import { MdOutlineLocalGroceryStore } from "react-icons/md";
import { HiBars3BottomLeft } from "react-icons/hi2";

import './Navbar.css'


const Navbar = () => {

  const [width] = useWindowSize();

  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  return (
    <div className='navbar'>
      {width < 1163 && (
        <>
          <Sidebar isOpen={isSidebarOpen} onClose={handleSidebarClose} />
          <HiBars3BottomLeft size="34px" className='left-bar' onClick={toggleSidebar}/>
        </>)}

      {width > 900 && (
        <Link to="/">
          <img src={logo} alt='logo' className='logo'/>
        </Link>
      )}

      {width > 1250 && (
        <nav>
          <ul>
              <Link to="/products" >Products</Link>
              <Link to="/about" >About</Link>
          </ul>
        </nav>)}

      <div className='search-box'>
        <img src={search} alt='icon-search'/>
        <input type='text' placeholder='What are you looking for ?'/>
      </div>

        <Link to="/authentication">
            {width > 814 && (
          <div className='user'>
            <FaUser className='user-icon'/>
              <div className='user-info'>
                <p id="user-name">Welcome</p>
                <p id="Account">Sign in / Register</p>
              </div>
          </div>
            )}
        </Link>
      
      <Link to="not_yet">
        <div className='cart'>
          <MdOutlineLocalGroceryStore className="cart-icon"/>
          <span className='cart-count'>0</span>
        </div>
    </Link>
      </div>
  )
}

export default Navbar;
