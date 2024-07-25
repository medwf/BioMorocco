import Navbar from "./Components/Navbar/Navbar";
import { Routes, Route } from "react-router-dom";

import Home from "./Routes/Home/Home";
import Products from "./Routes/Products/Product";
import Authentication from "./Routes/Sign_In_Log/Login_SignUp";
import About from "./Routes/About/About";
import Account from "./Routes/Account/Account";

function App() {

  return (
      <div className='container'>
        <Navbar />
        {/* <hr></hr> */}
          <Routes>
            <Route path="/" element={<Home />}/>
              <Route path="/products" element={<Products />}/>
              <Route path="/authentication" element={<Authentication />}/>
              <Route path="/account" element={<Account />}/>
              {/* <Route path="/carts" element={<Carts />}/> */}
              <Route path="*" element={<About />}/>
          </Routes>
      </div>
  );
}

export default App;
