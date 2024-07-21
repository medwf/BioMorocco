import React from 'react'
import useWindowSize from '../WindowsSize/windowsSize';

import logo from '../../assets/light.jpg'
import search from '../../assets/search-w.png'
import { FaUser } from "react-icons/fa";
import { MdOutlineLocalGroceryStore } from "react-icons/md";
import { HiBars3BottomLeft } from "react-icons/hi2";

import './Navbar.css'


const Navbar = () => {

  const [width] = useWindowSize();

  return (
    <div className='navbar'>
      {width < 1163 && (
          <HiBars3BottomLeft size="34px" className='left-bar'/>
      )}
      {width > 900 && (
        <img src={logo} alt='logo' className='logo'/>
      )}

      {width > 1250 && (
      <ul>
        <li>Stores</li>
        <li>Products</li>
        <li>About</li>
      </ul>

      )}

      <div className='search-box'>
        <img src={search} alt='icon-search'/>
        <input type='text' placeholder='What are you looking for ?'/>
      </div>

        <div className='user'>
          <FaUser size="32px" className='user-icon'/>
          {width > 814 && (
            <div className='user-info'>
              <p id="user-name">Welcome</p>
              <p id="Account">Sign in / Register</p>
            </div>
          )}
        </div>
      
      <div className='cart'>
        <MdOutlineLocalGroceryStore size="40px" className="cart-icon"/>
        <span className='cart-count'>0</span>
      </div>
    </div>
  )
}

export default Navbar;
