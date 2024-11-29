'use client';

import "~/styles/globals.css";
import { useState } from "react";

// Define the data structure for the post
interface PostData {
  title: string;
  content: string;
  access_level: number; // Maps to visibility options
  tags: string[];
  user_id: string; // Include user_id
}

export default function CreatePostPage() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState(""); // Renamed from "description"
  const [accessLevel, setAccessLevel] = useState(4); // Default to "Public"
  const [tags, setTags] = useState<string[]>([]);
  const [userId, setUserId] = useState("123"); // Assuming user_id is fetched or hardcoded for now
  const [error, setError] = useState<string | null>(null); // Error handling state

  // Submit the post to the backend
  const handlePostSubmit = async () => {
    // Prepare the post data
    const postData: PostData = {
      title,
      content,
      access_level: accessLevel,
      tags,
      user_id: userId, // Include the user_id
    };

    try {
      const response = await fetch('http://localhost:8000/api/create_blog', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
      });

      if (!response.ok) {
        throw new Error("Failed to submit post");
      }

      const result = await response.json() as PostData;
      console.log("Post submitted successfully:", result);
      alert("Post submitted successfully!");
    } catch (error) {
      console.error("Error submitting post:", error);
      setError("Error submitting post");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#03045E] to-[#0077B6] p-4">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">Create a New Blog Post</h1>

        {/* Title Input */}
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-medium mb-2">
            Title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter a title for your post"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Content Input */}
        <div className="mb-4">
          <label htmlFor="content" className="block text-gray-700 font-medium mb-2">
            Content
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write the content of your post..."
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={5}
          ></textarea>
        </div>

        {/* Tags Input */}
        <div className="mb-4">
          <label htmlFor="tags" className="block text-gray-700 font-medium mb-2">
            Tags
          </label>
          <input
            type="text"
            id="tags"
            value={tags.join(", ")}
            onChange={(e) => setTags(e.target.value.split(",").map(tag => tag.trim()))}
            placeholder="Enter tags separated by commas"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Access Level Toggle */}
        <div className="mb-4">
          <label className="block text-gray-700 font-medium mb-2">Post Visibility</label>
          <div className="flex items-center space-x-6">
            <label>
              <input
                type="radio"
                name="access_level"
                value={3}
                checked={accessLevel === 3}
                onChange={() => setAccessLevel(3)}
                className="mr-2"
              />
              Public
            </label>
            <label>
              <input
                type="radio"
                name="access_level"
                value={2}
                checked={accessLevel === 2}
                onChange={() => setAccessLevel(2)}
                className="mr-2"
              />
              Followers Only
            </label>

            <label>
              <input
                type="radio"
                name="access_level"
                value={1}
                checked={accessLevel === 1}
                onChange={() => setAccessLevel(1)}
                className="mr-2"
              />
              Private
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <button
          className="create-post-submit"
          onClick={handlePostSubmit}
        >
          Submit Post
        </button>

        {/* Display Error if any */}
        {error && <p className="text-red-500 mt-4">{error}</p>}
      </div>
    </main>
  );
}
