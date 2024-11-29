'use client';

import { useState } from "react";
import Image from "next/image";

interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  creator_name: string;
  tags: string[];
  likes: number;
  comments: number;
  bookmarked: boolean;
  image?: string;
}

interface SearchBarProps {
  onSearchResults: (posts: Post[]) => void; // Callback to send search results to parent
}

export default function SearchBar({ onSearchResults }: SearchBarProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [searchTerm, setSearchTerm] = useState(''); // Track the search term
  const [loading, setLoading] = useState(false); // Track loading state
  const [error, setError] = useState<string | null>(null); // Track error state

  const handleFocus = () => setIsFocused(true);
  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    if (e.target.value === "") {
      setIsFocused(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value); // Update the search term as the user types
  };

  // Search and Fetch Posts Logic
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); // Set loading state when search starts
    setError(null); // Reset any errors
    try {
      const response = await fetch(`http://localhost:8000/api/search_posts?query=${searchTerm}`);
      if (response.ok) {
        const data = await response.json() as Post[];
        onSearchResults(data); // Pass the search results to the parent component
      } else {
        setError('Error fetching posts');
      }
    } catch (error) {
      console.error('Error searching posts:', error);
      setError('An error occurred while fetching posts');
    } finally {
      setLoading(false); // Set loading to false after fetch completes
    }
  };

  return (
    <div className="relative search-bar">
      <form onSubmit={handleSearch} className="flex justify-center items-center">
        {/* Input Field with Dynamic Width */}
        <input
          type="text"
          className={`bg-white h-10 px-5 pr-10 rounded-full text-sm focus:outline-none transition-all duration-300 ease-in-out ${
            isFocused ? "w-64" : "w-12"
          }`}
          placeholder="Search..."
          value={searchTerm}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onChange={handleChange}
        />

        {/* Search Icon */}
        <button type="submit" className="search-bar-icon">
          <Image
            src="/images/search.svg"
            alt="Search Icon"
            width={20}
            height={20}
          />
        </button>
      </form>
    </div>
  );
}
