'use client';

import "~/styles/globals.css";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Article {
  id: number;
  title: string;
  author: string;
}

interface User {
  name: string;
  email: string;
  first_name: string;
  last_name: string;
  bio: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const [userName, setUserName] = useState<string>("");
  const [userEmail, setUserEmail] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [bio, setBio] = useState<string>("");
  const [editMode, setEditMode] = useState<boolean>(false);
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  // Fetch user information and articles from the API
  const fetchProfileData = async (): Promise<void> => {
    try {
      const userResponse = await fetch("http://127.0.0.1:8000/api/profile/<int:pk>"); // API endpoint to get user data
      if (!userResponse.ok) {
        throw new Error("Failed to fetch user data");
      }
      const userData: User = await userResponse.json() as User;
      setUserName(userData.name);
      setUserEmail(userData.email);
      setFirstName(userData.first_name);
      setLastName(userData.last_name);
      setBio(userData.bio);

      const articlesResponse = await fetch(`http://127.0.0.1:8000/api/get_blogs?user=${userData.name}`); // API endpoint to get user's articles
      if (!articlesResponse.ok) {
        throw new Error("Failed to fetch articles");
      }
      const articlesData: Article[] = await articlesResponse.json() as Article[];
      setArticles(articlesData);

      setLoading(false); // Set loading to false after data is fetched
    } catch (error: unknown) {
      if (error instanceof Error) {
        setError(error.message); // Set error message to state
      } else {
        setError("An unknown error occurred");
      }
      setLoading(false); // Ensure loading is turned off even if there's an error
    }
  };

  useEffect(() => {
    fetchProfileData().catch((err) => {
      console.error("Error in fetchProfileData:", err);
    });
  }, []);

  // Handle saving profile changes
  const handleSaveSettings = async () => {
    try {
      const response = await fetch("/api/user-profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          bio: bio,
          email: userEmail,
          username: userName,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to save settings");
      }

      setEditMode(false); // Exit edit mode after saving
      console.log("Saved settings:", { firstName, lastName, bio, userEmail, userName });
    } catch (error: unknown) {
      if (error instanceof Error) {
        console.error("Error saving settings:", error.message);
      } else {
        console.error("An unknown error occurred");
      }
      alert("Error saving settings");
    }
  };

  if (loading) {
    return <div>Loading...</div>; // Show loading text while data is being fetched
  }

  if (error) {
    return <div>Error: {error}</div>; // Display any errors that occur during fetch
  }

  return (
    <main className="profile-page min-h-screen p-6 bg-gray-100">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Profile</h1>

        {/* Profile Section */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-2xl font-semibold mb-2">User Info</h2>
          {editMode ? (
            <div>
              <div className="mb-4">
                <label className="block text-gray-700">Name</label>
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700">Email</label>
                <input
                  type="email"
                  value={userEmail}
                  onChange={(e) => setUserEmail(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700">First Name</label>
                <input
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700">Last Name</label>
                <input
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700">Bio</label>
                <textarea
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg"
                />
              </div>
              <button
                onClick={handleSaveSettings}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Save Settings
              </button>
            </div>
          ) : (
            <div>
              <p className="text-gray-600">Name: {userName}</p>
              <p className="text-gray-600">Email: {userEmail}</p>
              <p className="text-gray-600">Bio: {bio}</p>
              <button
                onClick={() => setEditMode(true)}
                className="text-blue-600 hover:underline mt-4"
              >
                Edit Profile
              </button>
            </div>
          )}
        </div>

        {/* Articles Section */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-2xl font-semibold mb-4">Articles</h2>
          <ul className="space-y-4">
            {articles.length === 0 ? (
              <li>No articles available</li>
            ) : (
              articles.map((article) => (
                <li key={article.id}>
                  <h3 className="text-xl font-bold">{article.title}</h3>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </main>
  );
}
