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
  const [loading, setLoading] = useState(false); // Track loading state
  const [error, setError] = useState<string | null>(null); // Track error state

  // Fetch posts from the backend
  const fetchPosts = async () => {
    setLoading(true); // Set loading to true when fetching
    setError(null); // Reset error before fetching
    try {
      const response = await fetch('http://localhost:8000/api/get_blogs');
      if (response.ok) {
        const data = await response.json() as Post[];
        setPosts(data);
      } else {
        setError('Error fetching posts');
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
      setError('An error occurred while fetching posts');
    } finally {
      setLoading(false); // Set loading to false after fetch completes
    }
  };

  useEffect(() => {
    fetchPosts().catch((error) => console.error('Failed to load posts', error));
  }, []);

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
    </div>
  );
};

export default ExplorePage;
