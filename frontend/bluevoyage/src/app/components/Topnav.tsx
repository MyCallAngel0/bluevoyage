'use client';
import Link from "next/link";
import Image from "next/image";
import { useState, useEffect } from "react";
import SearchBar from "./SearchBar";

export default function TopNav() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isUserSignedIn, setIsUserSignedIn] = useState(false); // Track if the user is signed in

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  useEffect(() => {
    // Check if user is signed in (this could be done via an API call or cookie)
    const userStatus = localStorage.getItem("isUserSignedIn");
    if (userStatus === "true") {
      setIsUserSignedIn(true);
    }
  }, []);

  const handleSignOut = () => {
    // Handle user sign-out (for example, clear localStorage or call an API)
    localStorage.removeItem("isUserSignedIn");
    setIsUserSignedIn(false);
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
          {/* Show Profile link only if user is signed in */}
          {isUserSignedIn && (
            <Link href="/profile" className="nav-link">
              Profile
            </Link>
          )}
          <SearchBar />
        </div>
        <div className="right-side">
          {/* Show Sign Up or Profile link based on user sign-in status */}
          {isUserSignedIn ? (
            <button onClick={handleSignOut} className="nav-link">
              Sign Out
            </button>
          ) : (
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
              <Link href="/profile" className="sidebar-link">
                Profile
              </Link>
            )}
            {/* Show Sign Up or Sign Out link based on user sign-in status */}
            {isUserSignedIn ? (
              <button onClick={handleSignOut} className="sidebar-link">
                Sign Out
              </button>
            ) : (
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
