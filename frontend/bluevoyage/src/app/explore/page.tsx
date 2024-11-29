'use client';
import "~/styles/globals.css";
import { useState, useEffect } from 'react';
import Image from 'next/image';

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

const ExplorePage = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalResults: 0,
    hasNext: false,
    hasPrevious: false,
  });

  // Function to fetch posts from the backend
  const fetchPosts = async (page: number) => {
    setLoading(true);
    setError(null);
    try {
      // Instead of getting the token from localStorage, rely on the cookie
      const response = await fetch(`http://127.0.0.1:8000/api/get_blogs?page=${page}`, {
        method: 'GET',
        headers: {
          // No need to manually set Authorization header since the cookie will be sent automatically
        },
        credentials: 'include', // Ensure cookies (including JWT) are sent with the request
      });

      if (response.ok) {
        const data = await response.json() as { blogs: Post[]; pagination: { currentPage: number; totalPages: number; totalResults: number; hasNext: boolean; hasPrevious: boolean } };
        setPosts(data.blogs);
        setPagination(data.pagination);
      } else {
        setError('Error fetching posts');
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
      setError('An error occurred while fetching posts');
    } finally {
      setLoading(false);
    }
  };

  // Fetch posts on component mount and when the page changes
  useEffect(() => {
    fetchPosts(pagination.currentPage).catch((error) => console.error('Failed to load posts', error));
  }, [pagination.currentPage]);

  return (
    <div className="explore-container pt-16 min-h-screen bg-gradient-to-b from-[#03045E] to-[#0077B6]">
      {/* Loading Animation */}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}

      {/* Error Message */}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Posts List */}
      {!loading && posts.length > 0 ? (
        <div className="posts-list">
          {posts.map((post) => (
            <div key={post.id} className="post-card">
              <h2>{post.title}</h2>
              <p>{post.content}</p>
              <p><strong>By: </strong>{post.creator_name}</p>
              <p><strong>Created on: </strong>{post.created_at}</p>
              <p><strong>Tags: </strong>{post.tags.join(', ')}</p>
              <p><strong>Likes: </strong>{post.likes} | <strong>Comments: </strong>{post.comments}</p>

              {post.image && <Image src={post.image} alt={post.title} width={200} height={200} />}

              <div className="post-actions">
                <button onClick={() => console.log('Like')} className="like-button">Like</button>
                <button onClick={() => console.log('Bookmark')} className="bookmark-button">
                  {post.bookmarked ? 'Unbookmark' : 'Bookmark'}
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        !loading && <p>No posts available.</p>
      )}

      {/* Pagination Controls */}
      <div className="pagination-controls">
        <button
          onClick={() => setPagination((prev) => ({ ...prev, currentPage: prev.currentPage - 1 }))}
          disabled={!pagination.hasPrevious || loading}
        >
          Previous
        </button>
        <span>
          Page {pagination.currentPage} of {pagination.totalPages}
        </span>
        <button
          onClick={() => setPagination((prev) => ({ ...prev, currentPage: prev.currentPage + 1 }))}
          disabled={!pagination.hasNext || loading}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default ExplorePage;
