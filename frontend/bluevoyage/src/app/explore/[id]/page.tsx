'use client';

import "~/styles/globals.css";
import { useState } from "react";
import { useRouter } from "next/navigation";
import React from "react";

// Mock article data
const mockArticles = [
  { id: 1, title: "10 Best Places to Visit in 2024", content: "Lorem ipsum...", author: "Alice" },
  { id: 2, title: "How to Pack Like a Pro", content: "Lorem ipsum...", author: "Bob" },
  { id: 3, title: "The Secrets of Hidden Beaches", content: "Lorem ipsum...", author: "Charlie" },
];

export default function ArticlePage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();

  // Unwrap the `params` object with `React.use()`
  const { id } = React.use(params);
  const articleId = parseInt(id);

  // Find the article in mock data
  const article = mockArticles.find((article) => article.id === articleId);

  const [likes, setLikes] = useState(0);
  const [hasLiked, setHasLiked] = useState(false);  // Track whether the user has liked the article
  const [comments, setComments] = useState<string[]>([]);
  const [newComment, setNewComment] = useState("");

  if (!article) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-gray-500">Article not found!</p>
      </main>
    );
  }

  const handleLike = () => {
    if (hasLiked) {
      setLikes(likes - 1);
    } else {
      setLikes(likes + 1);
    }
    setHasLiked(!hasLiked);  // Toggle the like state
  };

  const handleCommentSubmit = () => {
    if (newComment.trim()) {
      setComments((prev) => [...prev, newComment]);
      setNewComment("");
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <button
        onClick={() => router.back()}
        className="text-blue-600 hover:underline mb-4"
      >
        &larr; Back
      </button>

      <article className="bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-4">{article.title}</h1>
        <p className="text-gray-500 mb-2">by {article.author}</p>
        <p className="text-gray-700">{article.content}</p>
      </article>

      {/* Like Button */}
      <div className="mt-6 flex items-center space-x-4">
        <button
          onClick={handleLike}
          className={`${
            hasLiked ? "bg-red-600" : "bg-blue-600"
          } text-white px-4 py-2 rounded hover:bg-blue-700 transition`}
        >
          {hasLiked ? "Unlike" : "Like"} ({likes})
        </button>
      </div>

      {/* Comments Section */}
      <section className="mt-6">
        <h2 className="text-2xl font-bold mb-4">Comments</h2>

        <div className="space-y-4">
          {comments.map((comment, index) => (
            <p key={index} className="bg-gray-200 p-3 rounded">
              {comment}
            </p>
          ))}
        </div>

        <div className="mt-4 flex items-center space-x-4">
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleCommentSubmit}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Comment
          </button>
        </div>
      </section>
    </main>
  );
}
