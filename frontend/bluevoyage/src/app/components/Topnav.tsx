'use client';

import Link from "next/link";
import Image from "next/image";
import { useState, useEffect } from "react";
import SearchBar from "./SearchBar";

export default function TopNav() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isUserSignedIn, setIsUserSignedIn] = useState(false); // Track if the user is signed in
  const [userData, setUserData] = useState<any>(null); // Store user data
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // Dropdown menu for profile

  
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  
  // Function to fetch user data from the /user endpoint to check if the user is signed in
  const fetchUserData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/user', {
        method: 'GET',
        credentials: 'include', // Include cookies in the request
      });

      if (response.ok) {
        const data = await response.json() as { id: number, username: string, email: string, first_name: string, last_name: string };
        setIsUserSignedIn(true); // Mark the user as signed in
      } else {
        setIsUserSignedIn(false); // Mark the user as not signed in
        setUserData(null); // Clear user data if not authenticated
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      setIsUserSignedIn(false);
      setUserData(null);
    }
  };

  useEffect(() => {
    // Fetch user data on component mount to check if the user is signed in
    fetchUserData().catch(error => console.error('Failed to fetch user data:', error));
  }, []);

  const handleSignOut = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/logout', {
        method: 'POST',
        credentials: 'include', // Include cookies for logout
      });

      if (response.ok) {
        setIsUserSignedIn(false);
        setUserData(null); // Clear user data on sign out
      } else {
        console.error('Error logging out');
      }
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <nav className={`top-nav ${isSidebarOpen ? "sidebar-open" : ""}`}>
      {/* Desktop Navbar */}
      <div className="desktop-nav">
        <div className="logo">
          <Link href="/">
            <Image src="/images/logo.png" alt="Logo" width={155} height={60} />
          </Link>
        </div>
        <div className="middle-side">
          <Link href="/explore" className="nav-link">
            Explore
          </Link>

          <Link href="/login" className="login-link">
            Login
          </Link> 
          <button onClick={handleSignOut} className="logout-link">
            Logout
          </button>
          {/* Show Profile link only if user is signed in */}
          {isUserSignedIn && (
            <div className="relative">
              <button onClick={toggleDropdown} className="nav-link">
                Profile
              </button>
              {isDropdownOpen && (
                <div className="dropdown-menu absolute bg-white shadow-lg rounded-lg mt-2 p-4">
                  <Link href="/profile" className="block py-2 px-4">
                    View Profile
                  </Link>
                  <button onClick={handleSignOut} className="block py-2 px-4 text-red-600">
                    Logout
                  </button>
                </div>
              )}
            </div>
          )}
          <SearchBar />
        </div>
        <div className="right-side">
          {/* Show Sign Up or Profile link based on user sign-in status */}
          {!isUserSignedIn && (
            <Link href="/signup" className="signup-link">
              Sign Up
            </Link>
          )}
          
        </div>
      </div>

      {/* Mobile Sidebar */}
      <div className="mobile-nav">
        <div className="logo">
          <Link href="/">
            <Image src="/images/logo.png" alt="Logo" width={155} height={60} />
          </Link>
        </div>
        <button onClick={toggleSidebar} className="menu-button">
          ☰
        </button>
        {isSidebarOpen && (
          <div className="sidebar">
            <button className="close-button" onClick={toggleSidebar}>
              ✕
            </button>
            <SearchBar />
            <Link href="/explore" className="sidebar-link">
              Explore
            </Link>
            {/* Show Profile link only if user is signed in */}
            {isUserSignedIn && (
              <div className="relative">
                <button onClick={toggleDropdown} className="sidebar-link">
                  Profile
                </button>
                {isDropdownOpen && (
                  <div className="dropdown-menu absolute bg-white shadow-lg rounded-lg mt-2 p-4">
                    <Link href="/profile" className="block py-2 px-4">
                      View Profile
                    </Link>
                    <button onClick={handleSignOut} className="block py-2 px-4 text-red-600">
                      Logout
                    </button>
                  </div>
                )}
              </div>
            )}
            {/* Show Sign Up link if user is not signed in */}
            {!isUserSignedIn && (
              <Link href="/signup" className="sidebar-link">
                Sign Up
              </Link>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
